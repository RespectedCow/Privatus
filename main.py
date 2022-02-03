# Importing libraries
import re
import socket

# Import scripts
from src import server
from src import backupSystem
from src import init

# Variables
init_functions = [
    backupSystem.init,
    init.init
]

valid_os = [
    "Windows",
    "Linux",
    "Raspbian"
]

# Functions
def check_init(identifier): # Check if function was initialized
    print(identifier)
    
    return True

def main():
    # Initialization
    for fnc in init_functions:
        results = check_init(fnc.__identifier__)
        
        if results:
            fnc()
        else:
            print(results)
            
        print("Functions initialized")
    
    port = 3333
    address = socket.gethostbyname(socket.getfqdn())
    
    serverObject = server.Server(address, port)
    serverObject.run()
    
    
    
# Main
if __name__ == "__main__":
    main()