# Import libraries
from operator import truediv
import struct
import socket, os, threading, json
from time import sleep
import importlib.machinery
from inspect import getmembers, isclass, isfunction

# Import scripts
from src import database
from src import interpreter
from src import commons
from src import console as c

# TYPES
REQ_TYPE_DATABASE = "database"

# Functions
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = json.dumps(msg).encode()
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    message = recvall(sock, msglen)
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
        # Identification
        identification = recv_msg(client)
        username = identification['username']
        password = identification['password']
        self.console.print("Client trying to log in as " + username)
        
        # Check if user was banned
        with open(commons.get_appdatafolder() + "/data/banned_users.txt", "r") as f:
            banned_users = f.readlines()
            for banned_user in banned_users:
                banned_user = banned_user.strip()
                print(banned_user)
                
                if banned_user == username:
                    send_msg(client, "You are banned.")
                    self.console.print(f"User {username} was banned.")
                    client.close()
                    if self.onlineUsers.__contains__(username):
                        self.onlineUsers.pop(username)
                    self.threadCount -= 1
                    
                    return
        
        # Check if returned data is valid
        if username == None or password == None:
            send_msg(client, "Incorrect")
            client.close()
            
        # Init the interpreter
        clientInterpreter = interpreter.ClientInterpreter(self.database, username, client)
        
        if self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True) == False:
            self.console.print(f"User {username} logged in.")
            send_msg(client, "Success")
            
            # Add user to online user list
            self.onlineUsers[username] = client
            
            while True:
                
                if self.shouldRun == False:
                    break
                
                try:
                    message = recv_msg(client)
                    if message != None:
                            
                        try:
                            return_message = clientInterpreter.check_message(message)
                            send_msg(client, return_message)
                        except socket.error:
                            self.console.print(f"User {username} disconnected.")
                            client.close()
                            self.threadCount -= 1
                            if self.onlineUsers.__contains__(username):
                                self.onlineUsers.pop(username)
                            break                 
                except Exception as e:
                    print(str(e))
                    print(self.onlineUsers)
                    self.console.print(f"User {username} disconnected.")
                    client.close()
                    if self.onlineUsers.__contains__(username):
                        self.onlineUsers.pop(username)
                    self.threadCount -= 1
                    break
                
            client.close()
                    
        elif self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True):
            send_msg(client, "Same user already logged in.")
            self.console.print(f"User {username} disconnected.")
            client.close()
            if self.onlineUsers.__contains__(username):
                self.onlineUsers.pop(username)
            self.threadCount -= 1
        else:
            send_msg(client, "Incorrect username or password")
            self.console.print(f"User {username} disconnected.")
            client.close()
            if self.onlineUsers.__contains__(username):
                self.onlineUsers.pop(username)
            self.threadCount -= 1