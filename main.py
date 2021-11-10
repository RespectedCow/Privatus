# Importing libraries
import socket

# Import scripts
from src import server

# Functions
def main():
    port = 3333
    address = "192.168.0.165"
    
    serverObject = server.Server(address, port)
    serverObject.run()
    
# Main
if __name__ == "__main__":
    main()