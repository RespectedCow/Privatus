# Importing libraries

# Importing scripts

# Classes
class Commander:
    
    def __init__(self, database):
        
        # Declare class variables
        self.database = database
    
    def check_message(self, message, user):
        '''
        Filters passed parameters and executes actions based on parameters given.
        
        Status codes:
        0 for OK
        1 for Error
        '''
        
        # Check if valid format
        if message['status'] == 0:
            message = message['message'] # Reassign it to make it make more sense
            print(message)
            
            if message['action'] == "createEntry":
                # Filter message param
                if not 'title' in message or not 'content' in message:
                    return "Invalid entry format."

                if type(message['title']) != str or type(message['content']) != str:
                    return "Invalid types"
                
                # Create the entry
                print(user)
                print(self.database.create_entry(user, message['title'], message['body']))
                return "Entry created successfully"
            
            
        return "Unknown status code"