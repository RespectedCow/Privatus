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
        '''
        Checks if required tables exists otherwise create them
        '''
        
        # Check if required tables exist
        print("Checking if required tables exists.")
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
        
        if self.cursor.fetchone()[0] == 1 :
            print("User table exists.")
        else: 
            print("User table does not exists! Creating one now.")
            
            # Create the table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (NAME           TEXT    NOT NULL,
            PASSWORD       CHAR(30)    NOT NULL,
            SYSTEM         TEXT)''')
            
            print("User table created.")
        
        self.database.commit()
        print("Changes commited.")
        
    def create_user(self, name, password, systeminfo):
        '''
        Creates a new user
        '''
        command = f'''INSERT INTO users (NAME, PASSWORD, SYSTEM) VALUES ({name}, {password}, {systeminfo})'''
        print(command)
        
        self.cursor.execute(command) # Execute
        self.database.commit() # Commit changes
        print(f"User {name} successfully created.")
            
    def check_if_exist(self, table, key, value):
        '''
        Check if table's row has the passed key
        '''
        rows = self.database.execute(f"SELECT * FROM {table}")
        
        for row in rows:
            if row[key] == value:
                return True
            
        return False
    
    def close(self):
        '''
        Closes the database
        '''
        self.database.close() # Close the database