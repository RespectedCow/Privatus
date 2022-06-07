# Import libraries
import struct
import socket, os, threading, json
import base64, hashlib, os
from time import sleep
import importlib.machinery
from inspect import getmembers, isclass, isfunction
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

# Import scripts
from src import database
from src import interpreter
from src import commons
from src import console as c

# TYPES
REQ_TYPE_DATABASE = "database"

# Functions
def send_msg(sock, msg, public_key=None):
    # Prefix each message with a 4-byte length (network byte order)
    if type(msg) != bytes:
        msg = json.dumps(msg)
        msg = msg.encode()
    
    if public_key:
        if type(public_key) == PKCS1_OAEP.PKCS1OAEP_Cipher:
            msg = public_key.encrypt(msg)
        if type(public_key) == AESCipher:
            msg = msg.decode()
            msg = public_key.encrypt(msg)
    
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock, private_key=None):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    message = recvall(sock, msglen)
    if message != None:
        if private_key:
            message = private_key.decrypt(message)
        else:
            message = message.decode()
            
        try:
            message = message.decode()
        except:
            pass
        
        if type(message) != bytes:
            message = json.loads(message)
        
    return message

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# Classes
class AESCipher(object):
    
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Server:
    
    def __init__(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.bind((address, port))
        
        sock.listen()
        
        # Class variables
        self.address = address
        self.port = port
        self.sock = sock
        self.shouldRun = False
        self.sessionAdapter = None
        self.sessionAdapterName = None
        self.threadCount = 0
        self.threads = {}
        self.private_key = None
        self.c_public_key = None
        self.aes_key = None
        
        self.onlineUsers = {}
        
        # Initialize console
        print("Initializing the server console")
        
        self.console = c.Console(self.stop)
        self.console.connect_interpreter(self.console_interpreter)
        
        threading.Thread(target=self.console.run).start()
    
        print("Console intialized.")
        
        self.console.print("Hosting server on " + self.address + " The port is " + str(self.port))
        
        # Init database
        sleep(1)
        self.database = database.Database(commons.get_appdatafolder() + "/database.sqlite", self.console)
        self.database.setup()
        
        # Console messages
        self.console.print("Server started \n")
        
    def run(self):
        self.shouldRun = True
        
        while self.shouldRun:
            try:
                client, address = self.sock.accept()
                self.console.print("Client from " + address[0] + " is connecting to the server")
                try:
                    threading.Thread(target=self.client_thread, args=(client,)).start()
                except Exception as error:
                    print(error)
                    self.console.print("User " + self.threadCount + " disconnected.")
                    client.close()
                    self.threadCount -= 1
                
                self.threadCount += 1
            except:
                
                if self.shouldRun == False:
                    break
                
                continue
            
        self.sock.close()
        
    def stop(self):
        print("Stopping the server")
        self.shouldRun = False
        
        exit()
        
    def adapter_request(self, req_type):
        
        # Manage request types here
        if req_type == REQ_TYPE_DATABASE:
            return self.database

    def adapter_check(self, adapterFolder=commons.get_appdatafolder() + "/adapters", file=None):
        ''''
        Checks if the adapter has required functions or classes
        '''
        
        if file == None:
            return
        
        # Values
        loader = importlib.machinery.SourceFileLoader('adapters', adapterFolder + "/" + file)
        adapter = loader.load_module('adapters')
        functions_list = getmembers(adapter, isfunction)
        
        adapter_required_func = [
            "get_type"
        ]
                    
        # Filter returned list
        class_list = []
        
        for i in getmembers(adapter, isclass):
            class_list.append(i[0])
        
        # Checks          
        for required in adapter_required_func:
            hasRequired = False
            
            for func in functions_list:
                if func[0] == required:
                    hasRequired = True
                    
            if hasRequired == False:
                return
            
        adapter_type = adapter.get_type()
        
        if adapter_type == "quick":
            hasFunc = False
            
            for func in functions_list:
                if func[0] == "run":
                    hasFunc = True
                    
            if hasFunc == False:
                return
        elif adapter_type == "session":
            if class_list.__contains__("Session") == False:
                return
            
        # If adapter passes all tests
        return True
        
    def console_interpreter(self, command_array):
        """
            After being done with it's own job, the console will pass the commands to the server object for jobs
        such as database handling, server administration, plugins, adapters etc.
        
        Adapters are scripts that are ran when the user inputs a command that corrensponds to the adapter's name.
        
        There are two types of adapters: session and quick
        session adapters are adapters that will last longer than just one command. Commands after an adapter of this type is ran will be 
        immediately passed to the adapter upon command execution.
        
        quick adapters are adapters that will only last one command. Normal commands basically.
        
        Required functions or classes:
        quick adapters: run(func) get_type(func)
        session_adapters: get_type(func) Session(class)
        
        """
        
        # Adapter session
        if self.sessionAdapter != None:
            if command_array[0] == "exit":
                self.sessionAdapter = None
                return "Exited adapter session"
            
            res = self.sessionAdapter.execute_command(command_array)
            if res == None:
                res = "Adapter returned none"
            return self.sessionAdapterName + " > " + res
        
        isMatched = False
        
        # Adapter
        adapterFolder = commons.get_appdatafolder() + "/adapters"
        
        for subdir, dirs, files in os.walk(adapterFolder): # To have a little modularity
            for file in files:
                file_info = os.path.splitext(file)
                
                if file_info[1] == ".py" and self.adapter_check(adapterFolder, file):
                    # Check if adapter has the required functions first
                    loader = importlib.machinery.SourceFileLoader('adapters', adapterFolder + "/" + file)
                    adapter = loader.load_module('adapters')
                    
                    # If adapter has required functions
                    name = file_info[0]

                    if command_array[0] == name:
                        script_type = adapter.get_type()
                        
                        if script_type == "quick":
                            results = adapter.run(self, command_array)
                            return results
                        elif script_type == "session":
                            self.sessionAdapterName = name
                            self.sessionAdapter = adapter.Session(self)
                            return self.sessionAdapterName + " > Entered adapter session"
                        else:
                            continue
                        
                else:
                    continue
        
        if isMatched == False:
            return
        
    def client_thread(self, client):
        # Generate public and private keys
        random_generator = Random.new().read
        self.private_key = RSA.generate(1024, random_generator)
        public_key = self.private_key.publickey()
        self.private_key = PKCS1_OAEP.new(self.private_key)
        
        # Confirm connection
        self.c_public_key = recv_msg(client)
        self.c_public_key = RSA.importKey(self.c_public_key)
        self.c_public_key = PKCS1_OAEP.new(self.c_public_key)
        
        # Send public and private keys
        if self.c_public_key:
            send_msg(client, public_key.exportKey().decode())
        
        # Identification
        identification = recv_msg(client, self.private_key)
        username = identification['username']
        password = identification['password']
        self.console.print("Client trying to log in as " + username)
        
        # Check if user was banned
        with open(commons.get_appdatafolder() + "/data/banned_users.txt", "r") as f:
            banned_users = f.readlines()
            for banned_user in banned_users:
                banned_user = banned_user.strip()
                
                if banned_user == username:
                    send_msg(client, "You are banned.", self.c_public_key)
                    self.console.print(f"User {username} was banned.")
                    client.close()
                    if self.onlineUsers.__contains__(username):
                        self.onlineUsers.pop(username)
                    self.threadCount -= 1
                    
                    return
        
        # Check if returned data is valid
        if username == None or password == None:
            send_msg(client, "Incorrect", self.c_public_key)
            client.close()
            
        # Init the interpreter
        clientInterpreter = interpreter.ClientInterpreter(self.database, username, client)
        
        if self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True) == False:
            self.console.print(f"User {username} logged in.")
            send_msg(client, "Success", self.c_public_key)
            
            # Generate key because we wish to use it from now on and send it to the client
            aes_key = os.urandom(128)[:10]
            self.aes_key = AESCipher(aes_key)
            
            send_msg(client, aes_key, self.c_public_key)
            
            # Add user to online user list
            self.onlineUsers[username] = client
            
            while True:
                
                if self.shouldRun == False:
                    break
                
                try:
                    message = recv_msg(client, self.aes_key)
                    if message != None:
                            
                        try:
                            return_message = clientInterpreter.check_message(message)
                            send_msg(client, return_message, self.aes_key)
                        except socket.error:
                            self.console.print(f"User {username} disconnected.")
                            client.close()
                            self.threadCount -= 1
                            if self.onlineUsers.__contains__(username):
                                self.onlineUsers.pop(username)
                            break                 
                except Exception as e:
                    self.console.print(f"User {username} disconnected.")
                    client.close()
                    if self.onlineUsers.__contains__(username):
                        self.onlineUsers.pop(username)
                    self.threadCount -= 1
                    break
                
            client.close()
                    
        elif self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True):
            send_msg(client, "Same user already logged in.", self.c_public_key)
            self.console.print(f"User {username} disconnected.")
            client.close()
            if self.onlineUsers.__contains__(username):
                self.onlineUsers.pop(username)
            self.threadCount -= 1
        else:
            send_msg(client, "Incorrect username or password", self.c_public_key)
            self.console.print(f"User {username} disconnected.")
            client.close()
            if self.onlineUsers.__contains__(username):
                self.onlineUsers.pop(username)
            self.threadCount -= 1