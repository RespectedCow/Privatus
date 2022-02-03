# Importing libraries
import os
import zlib
import sys

# Importing scripts
from src import backupSystem

# Classes
class Interpreter:
    
    def __init__(self, database, user, connection):
        
        # Declare class variables
        self.database = database
        self.user = user
        self.connection = connection
        
        # Track user commands
        self.user_session_commands = []
    
    def check_message(self, message):
        '''
        Filters passed parameters and executes actions based on parameters given.
        
        Status codes:
        0 for OK
        1 for Error
        '''
        
        # Check if valid format
        if message['status'] == 0:
            message = message['message'] # Reassign it to make it make more sense
            params = message['params']
            
            if message['action'] == "createEntry":
                # Filter message param
                if not 'title' in params or not 'content' in params:
                    return "Invalid entry format."

                if type(params['title']) != str or type(params['content']) != str:
                    return "Invalid types"
                
                # Create the entry
                self.database.create_entry(self.user, params['title'], params['content'])
                return "Entry created successfully"
            if message['action'] == "getEntries":
                print("Fetching user entries...")
                return self.database.get_entries(self.user)
            if message['action'] == "searchEntries":
                # Check if search term is given
                if not 'searchterm' in params:
                    return "No search term given."
                
                return self.database.search_entries(params['searchterm'], self.user)
            if message['action'] == "deleteEntry":
                # Check if id is given
                if not 'id' in params:
                    return "Id not given"
                
                self.database.destroyEntry(params['id'], self.user)
                
                return "Successfuly destroyed entry"
            if message['action'] == "showEntry":
                # Check if id is given
                if not 'id' in params:
                    return "Id not given"
                
                return self.database.get_entry(params['id'], self.user)
            if message['action'] == "editEntry":
                if not 'id' in params or not 'title' in params or not 'content' in params:
                    return "Required parameter not given"
                
                return self.database.edit_entry(params['id'], self.user, params['title'], params['content'])
            if message['action'] == "checkStatus":
                return "OK"
            if message['action'] == "checkBackupStatus":
                # Get the data
                usedStorage = backupSystem.getUserUS(self.user)
            
            if message['action'] == "backupFile":
                # Checks
                if not 'filename' in message['params'] or not 'filesize' in message['params']:
                    return "Required parameter not given"
                
                # Values
                filename = message['params']['filename']
                filesize = message['params']['filesize']
                
                filename = os.path.basename(filename)
                # convert to integer
                filesize = int(filesize)
                # start receiving the file from the socket
                with open(filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = self.connection.recv()
                        if not bytes_read:    
                            # nothing is received file transmitting is done
                            break
                        # write to the file the bytes we just received
                        f.write(bytes_read)
                        
                        # Compress the files
                        self.compressFile(filename)
                        
                        return "Backed up"
                
                return "Message error"
            
            return "Unknown action given"
        elif message['status'] == 1:
            self.connection.close()
            return "EXITED"
            
            
        return "Unknown status code"