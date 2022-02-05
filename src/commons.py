'''
This file contains commonly used functions 
'''

# Importing libraries
import platform
import os

# Functions
def get_appdatafolder():
    currentOs = platform.system()
    
    if currentOs == "Windows":
        return os.getenv('APPDATA') + "/project-oasis"
    if currentOs == "Linux":
        return os.path.expanduser('~') +  + "/project-oasis"

def check_array(array, value):
    for i in array:
        if i == value:
            return True
        
    return False

def check_dict(dict, key, value):
    for x, y in dict.items():
        if x == key:
            if y == value:
                return True
            
            
    return False