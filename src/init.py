# Importing libraries
import os

# Importing scripts
from src import commons

# Functions
class init:
    
    __identifier__ = "server_init"
    appDataFolder = commons.get_appdatafolder()
    
    directories = [
        "logs", "backupFolder"
    ]
    
    def run(self):
        print("Initializing the application")
    
        # Create the app data folder
        try:
            print("Creating app data folder.")
            os.mkdir(self.appDataFolder)
        except:
            pass
        
        for directory in self.directories:
            print("Creating " + directory + " folder")
            path = os.path.join(self.appDataFolder, directory)
            os.makedirs(path, exist_ok=True)
        
        print("Done!")
        
    def check_init(self):
        if os.path.isdir(self.appDataFolder) == False: # check main directory
            return True
        
        # Check if sub directories exists
        for directory in self.directories:
            if os.path.isdir(self.appDataFolder + "/" + directory) == False:
                return True
        
        # If they exists
        return False