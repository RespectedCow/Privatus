# Importing libraries
import platform
import socket
import threading

# Import scripts
from src import server
from src import backupSystem
from src import init

# Variables
init_functions = [
    init.init,
    backupSystem.init
]

valid_os = [
    "Windows",
    "Linux"
]

# Functions
def main():
    # Check if os is valid
    if valid_os.index(platform.system()):
       return
    
    # Initialization
    for fnc in init_functions:
        fnc = fnc()
        
        if fnc.check_init():
            fnc.run() # Will return any potential errors
        else:
            continue
            
    print("Program initialized")
    
    port = 2222
    address = socket.gethostbyname(socket.getfqdn())
    
    serverObject = server.Server(address, port)
    threading.Thread(target=serverObject.run).start()
    
# Main
if __name__ == "__main__":
    main()