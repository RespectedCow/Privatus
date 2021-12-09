# Importing libraries

# Importing scripts

# Classes
class Interpreter:
    
    def __init__(self, database, user, connection):
        
        # Declare class variables
        self.database = database
        self.user = user
        self.connection = connection
    
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
            
            return "Unknown action given"
        elif message['status'] == 1:
            self.connection.close()
            return "EXITED"
            
            
        return "Unknown status code"