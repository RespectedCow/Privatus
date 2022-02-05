# Importing libraries
import zlib
import sys
import os

# Importing scripts
from src import commons

# Variables

# Functions
def check_init(): # Functions checks if the init function has been called before
    return False

def getUserUS(username): # US stands for user status
    pass

def compressFile(filename):
        with open(filename, mode="rb") as fin, open(filename, mode="wb") as fout:
            data = fin.read()
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            print(f"Original size: {sys.getsizeof(data)}")
            print(f"Compressed size: {sys.getsizeof(compressed_data)}")

            fout.write(compressed_data)
            
def decompressFile(filename):
    with open(filename, mode="rb") as fin:
        data = fin.read()
        decompressed_data = zlib.decompress(data)
        print(f"Compressed size: {sys.getsizeof(data)}")
        # Compressed size: 1024
        print(f"Decompressed size: {sys.getsizeof(decompressed_data)}")
        # Decompressed size: 1000033
        
# Classes
class init:
    
    __identifier__ = "backup"
    appDataFolder = commons.get_appdatafolder()
    
    def run(self):
        pass
        
    def check_init(self):
        return True