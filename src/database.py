# Import libraries
import sqlite3
import json

# Classes
class Database:
    
    def __init__(self, database):
        self.database = sqlite3.connect(database)
        print("Database successfully opened.")
        
        # Get cursor
        self.cursor = self.database.cursor()
        
    def setup(self):
        # Check if required tables exist
        print("Checking if required tables exists.")
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='user' ''')
        
        if self.cursor.fetchone()[0] == 1 :
            print("User table exists.")
        else: 
            print("User table does not exists! Creating one now.")
            
            # Create the table
            self.database.execute('''CREATE TABLE USERS
            NAME           TEXT    NOT NULL,
            PASSWORD       CHAR(30)    NOT NULL,
            SYSTEM         TEXT;''')
            
            print("User table created.")
            
    def check_User(self, user, password):
        