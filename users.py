# Importing scripts
from src import commons

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
        if parameters[1] == "kick":
            has_matched = True
            if len(parameters) >= 3:
                username = parameters[2]
                user = server.onlineUsers[username]
                
                user.close()
                if server.onlineUsers.__contains__(username):
                    server.onlineUsers.pop(username)
                    server.threadCount -= 1
                    
                message = f"User {username} kicked."
            else:
                message = "No user given."
        if parameters[1] == "ban":
            has_matched = True
            if len(parameters) >= 3:
                username = parameters[2]
                user = server.onlineUsers[username]
                
                # Banning process
                # Get the app data folder first
                appDataFolder = commons.get_appdatafolder()
                
                # Open banned file and write on to it.
                with open(appDataFolder + "/data/banned_users.txt", 'w') as f:
                    f.write(username + "\n")
                
                user.close()
                if server.onlineUsers.__contains__(username):
                    server.onlineUsers.pop(username)
                    server.threadCount -= 1
                    
                message = f"User {username} banned."
                
        if parameters[1] == "unban":
            has_matched = True
            
            if len(parameters) >= 3:
                username = parameters[2]
                user = server.onlineUsers[username]
                
                # Banning process
                # Get the app data folder first
                appDataFolder = commons.get_appdatafolder()
                
                # Open banned file and write on to it.
                with open(appDataFolder + "/data/banned_users.txt", 'w+') as f:
                    list = f.readlines()
                    new_list = list.replace(username, '')
                    
                    f.write(new_list)
                
                user.close()
                if server.onlineUsers.__contains__(username):
                    server.onlineUsers.pop(username)
                    server.threadCount -= 1
                    
                message = f"User {username} unbanned."
    
    if has_matched == False:
        if len(parameters) >= 2:
            message =  parameters[1] + " is not a valid command."
        else:
            message = "No commands given"
    
    return message
