# Import libraries
from re import S
import socket
from multiprocessing.connection import Listener
import threading
import json
from time import sleep

# Import scripts
from src import database
from src import interpreter
from src import commons
from src import console as c

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
        
    def console_interpreter(self, command_array):
        isMatched = False
        
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
                    message = client.recv(4096).decode()
                    print(message)
                    if message != None:
                        message = json.loads(message)
                        self.console.print(message)
                        
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
                except:
                    self.console.print(f"User {username} disconnected.")
                    client.close()
                    self.onlineUsers.pop(username)
                    break
            
            client.send(json.dumps("Server closing").encode())
            self.console.print("Server closing")
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