# Import libraries
import socket
import threading
import pickle

# Import scripts
from src import database

# Classes
class Server:
    
    def __init__(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(address, port)
        
        # Class variables
        self.address = address
        self.port = port
        self.sock = sock
        self.shouldRun = False
        self.threadCount = 0
        
        # Init database
        self.database = database.Database("Cowmanager")
        self.database.setup()
        
    def run(self):
        self.shouldRun = True
        
        while self.shouldRun:
            client, address = self.sock.accept()
            print("Connection from " + address)
            threading.Thread(target=self.client_thread(client)).start()
            self.threadCount += 1
            
        self.sock.close()
        
    def stop(self):
        self.shouldRun = False
        
    def client_thread(self, client):
        # Identification
        identification = pickle.loads(client.recv(2048)) 
        
        if self.database.check_if_exist("USERS", identification['username']):
            # If user exists
            pass