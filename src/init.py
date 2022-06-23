# Importing libraries
import os, yaml

# Importing scripts
from src import commons

# Functions
def write_to_file(file, overwrite_dir):
    """
    Returns text data to be used for writing to a file if
    it matches a file in the local database otherwise will return empty strings
    """
        
    database_directory = overwrite_dir
    database = os.listdir(database_directory)
        
    data = ""
        
    if database.__contains__(file.strip("/")):
        with open(database_directory + file, "r") as f:
            f_extension = commons.get_file_extension(file)
                
            if f_extension == "yaml":
                data = yaml.safe_load(f)
            else:
                data = f.read()
                    
    return data

class init:
    
    __identifier__ = "server_init"
    appDataFolder = commons.get_appdatafolder()
    
    directories = [
        "data"
    ]
    
    files = [
        "/config.yaml"
    ]
    
    def run(self, dir_path):
        print("Initializing the application")
        
        # Values
        self.dir_path = dir_path
    
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
            
        for file in self.files:
            with open(self.appDataFolder + file, 'w') as f:
                data = write_to_file(file, self.dir_path + "/overwrite")
                
                if commons.get_file_extension(file) == "yaml":
                    yaml.dump(data, f)
                else:
                    f.write(data)
        
        print("Done!")
        
    def check_init(self):
        if os.path.isdir(self.appDataFolder) == False: # check main directory
            return True
        
        # Check if sub directories exists
        for directory in self.directories:
            if os.path.isdir(self.appDataFolder + "/" + directory) == False:
                return True
            
        for file in self.files:
            if os.path.isfile(self.appDataFolder + "/" + file) == False:
                return True
        
        # If they exists
        return False