# Importing scripts
from src import server as s
    
# Required functions
def get_type():
    return "quick"
    
def run(server, parameters):
    message = ""
    has_matched = False
    
    if len(parameters) >= 2:
        if parameters[1] == "list":
            has_matched = True
            
            if len(server.onlineUsers) >= 1:
            
                message += "Users online are:"
                
                for user in server.onlineUsers:
                    message += "\n" + user
                    
            else:
                message = "No users are connected to the server."
    
    if has_matched == False:
        if len(parameters) >= 2:
            message =  parameters[1] + " is not a valid command."
        else:
            message = "No commands given"
    
    return message
