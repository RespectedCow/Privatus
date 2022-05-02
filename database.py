# Importing scripts
from src import server as s
    
# Required functions
def get_type():
    return "session"
    
# Classes
class Session:
    
    def __init__(self, server):
        self.database = server.database
        
    def execute_command(self, parameters):
        if parameters[0] == "user":
            if len(parameters) >= 2:
                if parameters[1] == "create":
                    if len(parameters) >= 5:
                        name = parameters[2]
                        password = parameters[3]
                        isadmin = parameters[4]
                        
                        if isadmin == "true" or isadmin == "false":
                            res = self.database.create_user(name, password, bool(isadmin))
                            
                            if res:
                                return "Created user " + name
                            else:
                                return "User exists!"
                        else:
                            return "Invalid parameter(isadmin)"
                    else:
                        return "Please give more parameters"
                if parameters[1] == "delete":
                    if len(parameters) >= 3:
                        name = parameters[2].strip()

                        self.database.destroyUser(name)
                        return "Deleted user " + name
            else:
                return "Please give more a parameter"