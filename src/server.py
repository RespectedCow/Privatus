# Import libraries
from multiprocessing.connection import Connection
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
                self.console.print("Client from " + address[0] + " is connected to the server")
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
        
    def console_interpreter(self, command_array):
        """
            After being done with it's own job, the console will pass the commands to the server object for things
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
        
        adapter_required_func = (
            "get_type"
        )
        
        for subdir, dirs, files in os.walk(adapterFolder): # To have a little modularity
            for file in files:
                file_info = os.path.splitext(file)
                
                if file_info[1] == ".py":
                    # Check if adapter has the required functions first
                    loader = importlib.machinery.SourceFileLoader('adapters', adapterFolder + "/" + file)
                    adapter = loader.load_module('adapters')
                    functions_list = getmembers(adapter, isfunction)
                    
                    # Filter returned list
                    class_list = []
                    
                    for i in getmembers(adapter, isclass):
                        class_list.append(i[0])
                        
                    for required in adapter_required_func:
                        if functions_list.__contains__(required) == False:
                            continue
                    
                    # If adapter has required functions
                    name = file_info[0]

                    if command_array[0] == name:
                        script_type = adapter.get_type()
                        
                        if script_type == "quick" and functions_list.__contains__("run"):
                            results = adapter.run(self, command_array)
                            return results
                        elif script_type == "session":
                            if class_list.__contains__("Session"):
                                self.sessionAdapterName = name
                                self.sessionAdapter = adapter.Session(self)
                                return self.sessionAdapterName + " > Entered adapter session"
                            else:
                                continue
                        else:
                            continue
                        
                else:
                    continue
        
        if isMatched == False:
            return
        
    def client_thread(self, client):
        # Identification
        identification = json.loads(client.recv(4096).decode())
        username = identification['username']
        password = identification['password']
        self.console.print("Client trying to log in as " + username)
        
        # Check if returned data is valid
        if username == None or password == None:
            client.send(json.dumps("Incorrect").encode())
            client.close()
            
        # Init the interpreter
        clientInterpreter = interpreter.ClientInterpreter(self.database, username, client)
        
        if self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True) == False:
            self.console.print(f"User {username} logged in.")
            client.send(json.dumps("Success").encode())
            
            # Add user to online user list
            self.onlineUsers[username] = True
            
            while True:
                
                if self.shouldRun == False:
                    break
                
                try:
                    message = client.recv(6096).decode()
                    if message != None:
                        message = json.loads(message)
                        self.console.print(str(message))
                            
                        try:
                            return_message = clientInterpreter.check_message(message)
                            self.console.print(return_message)
                            client.send(json.dumps(return_message).encode())
                        except socket.error:
                            self.console.print(f"User {username} disconnected.")
                            client.close()
                            self.threadCount -= 1
                            self.onlineUsers.pop(username)
                            break                 
                except Exception as e:
                    print(e)
                    self.console.print(f"User {username} disconnected.")
                    client.close()
                    self.onlineUsers.pop(username)
                    break
                
            client.close()
                    
        elif self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_dict(self.onlineUsers, username, True):
            client.send(json.dumps("Same user already logged in.").encode())
            self.console.print(f"User {username} disconnected.")
            client.close()
            self.threadCount -= 1
        else:
            client.send(json.dumps("Incorrect username or password.").encode())
            self.console.print(f"User {username} disconnected.")
            client.close()
            self.threadCount -= 1