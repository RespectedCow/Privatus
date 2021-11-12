# Import libraries
import socket
import threading
import pickle

# Import scripts
from src import database
from src import commander
from src import commons

# Classes
class Server:
    
    def __init__(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        
        sock.listen(5)
        
        # Class variables
        self.address = address
        self.port = port
        self.sock = sock
        self.shouldRun = False
        self.threadCount = 0
        
        self.onlineUsers = {}
        
        # Init database
        self.database = database.Database("./Cowmanager.sqlite")
        self.database.setup()
        
    def run(self):
        self.shouldRun = True
        
        while self.shouldRun:
            client, address = self.sock.accept()
            print("Connection from " + address[0])
            threading.Thread(target=self.client_thread(client)).start()
            self.threadCount += 1
            
        self.sock.close()
        
    def stop(self):
        self.shouldRun = False
        
    def client_thread(self, client):
        # Identification
        identification = pickle.loads(client.recv(2048))
        username = identification['username']
        password = identification['password']
        
        # Check if returned data is valid
        if username == None or password == None:
            client.close()
            
        # Init the commander
        commandIssuer = commander.Commander()
        
        if self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_array(self.onlineUsers, username) == False:
            print(f"User {username} logged in.")
            client.send(pickle.dumps("Success"))
            
            # Add user to online user list
            self.onlineUsers[username] = True
            
            while True:
                try:
                    client.send(pickle.dumps(commandIssuer.get_command()))
                except socket.error:
                    client.close()
                    self.onlineUsers.remove(username)

                response = pickle.loads(client.recv(2048))
                print(response)
                if not response:
                    client.close()
                    self.onlineUsers.remove(username)
                    
        elif self.database.check_if_exist("users", 0, username) and self.database.check_row_column(self.database.get_user("users", username), 1, password) and commons.check_array(self.onlineUsers, username):
            client.send(pickle.dumps("Same user already logged in."))
            client.close()
        else:
            client.send(pickle.dumps("Incorrect"))
            client.close()