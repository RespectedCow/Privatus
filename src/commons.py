'''
This file contains commonly used functions 
'''

# Functions
def check_array(array, value):
    for i in array:
        if i == value:
            return True
        
    return False