# Import libraries
import sqlite3, datetime

# Importing scripts

# Classes
class Database:
    
    def __init__(self, database, console):
        
        self.console = console
        
        seperator = "*" * 20
        self.console.print(seperator)
        
        self.database = sqlite3.connect(database, check_same_thread=False)
        self.console.print("Initializing database.")
        self.console.print("Database successfully opened.")
        
        # Get cursor
        self.cursor = self.database.cursor()
        
    def setup(self):
        '''
        Checks if required tables exists otherwise create them
        '''
        
        # Check if required tables exist
        self.console.print("Checking if required tables exists.")
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
        
        if self.cursor.fetchone()[0] == 1 :
            self.console.print("User table exists.")
        else: 
            self.console.print("User table does not exists! Creating one now.")
            
            # Create the table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (NAME           TEXT    NOT NULL,
            PASSWORD       TEXT    NOT NULL,
            isAdmin        BOOLEAN  NOT NULL,
            DATETIME         TEXT);''')
            
            self.console.print("User table created.")
            
        # Entry table
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='entry' ''')
        
        if self.cursor.fetchone()[0] == 1 :
            self.console.print("Entry table exists.")
        else: 
            self.console.print("Entry table does not exists! Creating one now.")
            
            # Create the table
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS entry
            (ID             INT NOT NULL,
            OWNER           TEXT    NOT NULL,
            TITLE       TEXT    NOT NULL,
            BODY         TEXT NOT NULL,
            DATETIME       TEXT     NOT NULL);''')
            
            self.console.print("Entry table created.")
        
        self.database.commit()
        self.console.print("Done")
        self.console.print("Changes commited.")
        
        seperator = "*" * 20
        self.console.print(seperator)
        
        self.console.print("")
        
    def create_user(self, name, password ,isadmin):
        '''
        Creates a new user
        '''
        
        # Check if user exists
        if self.check_if_exist("users", "NAME", name):
            return "User exists! Please select another username"
        
        command = f'''INSERT INTO users (NAME, PASSWORD, DATETIME, isAdmin) VALUES (?, ? , ?, ?);'''
        self.console.print(command)
        
        # Get the datetime
        dt = datetime.datetime.now()
        
        # This is going to remove the milliseconds
        x = dt.replace(microsecond=0)
        
        self.cursor.execute(command, (name, password, x, isadmin)) # Execute
        self.database.commit() # Commit changes
        self.console.print(f"User {name} successfully created.")
    
    def create_entry(self, user, title, body):
        # Check if user is an existing user
        if self.get_user("users", user) == None: # If user does not exist
            return 0
        
        # Insert the entry
        command = f'''INSERT INTO entry (ID, OWNER, TITLE, BODY, DATETIME) VALUES (?, ?, ? , ?, ?);'''
        self.console.print(command)
        
        # Get the datetime
        dt = datetime.datetime.now()
        
        # This is going to remove the milliseconds
        time = dt.replace(microsecond=0)
        
        # Get id
        id = self.get_user_total_entries(user) + 1
        
        self.cursor.execute(command, (id, user, title, body, time)) # Execute
        self.database.commit() # Commit changes
        self.console.print(f"Entry successfully created.")
        
        return "Success"
    
    def edit_entry(self, id, user, title, body):
        '''
        Makes changes to entry with specified id with the given parameters
        '''
        # Get rows
        rows = self.database.execute(f"SELECT * FROM entry")

        for row in rows:
            
            if row[0] == id and row[1] == user:
                self.database.execute(f'UPDATE entry SET ID = ?, OWNER = ?, TITLE = ?, BODY = ?, DATETIME = ? WHERE ID = {id}', (id, user, title, body, row[4]))
        
        self.database.commit()
        return f"Edited entry id {id}"
        
    def check_if_exist(self, table, column, value):
        '''
        Check if table's rows's columns is the passed value
        '''
        rows = self.database.execute(f"SELECT * FROM {table}")
        
        for row in rows:
            if row[column] == value:
                return True
            
        return False
    
    def check_row_column(self, row, column, value):
        '''
        Check if the row's column is the value provided.
        '''
        
        if row[column] == value:
            return True
            
        return False
    
    def search_entries(self, searchterm, user):
        '''
        Return a list of entries with the search term in it's title
        '''
        
        rows = self.database.execute("SELECT * FROM entry")
        return_results = []
        
        for row in rows:
            title = row[2].lower()
            
            if searchterm in title and row[1] == user:
                return_results.append(row)
                
        return return_results
    
    def get_entries(self, username):
        '''
        Gets the entries that the user created.
        '''
        rows = self.database.execute(f"SELECT * FROM entry")
        return_results = []
        
        for row in rows:
            if row[1] == username:
                return_results.append(row)
                
        return return_results
    
    def get_entry(self, id, user):
        '''
        Gets the entry with the id provided.
        '''
        rows = self.database.execute(f"SELECT * FROM entry")
        
        for row in rows:
            if row[1] == user and row[0] == id:
                return row
            
        return None     
    
    def get_user(self, table, username):
        '''
        Gets the user with the provided username
        '''
        
        rows = self.database.execute(f"SELECT * FROM {table}")
        
        for row in rows:
            if row[0] == username:
                return row
            
        return None
    
    def get_user_total_entries(self, username):
        '''
        Gets the total entries that the user has
        '''
        rows = self.database.execute(f"SELECT * FROM entry")
        results = 0
        
        for row in rows:
            if row[1] == username:
                results += 1
                
        return results
    
    def destroyEntry(self, id, user):
        '''
        Destroys the entries with the given id
        '''
    
        self.database.execute(f"DELETE from entry WHERE ID={id}")
        print(f"DELETE from entry WHERE ID={id}")
        
        # Update entries above the current id
        rows = self.database.execute(f"SELECT * FROM entry")

        for row in rows:
            
            if row[0] > id and row[1] == user:
                rowid = row[0]
                self.database.execute(f'UPDATE entry SET ID = ?, OWNER = ?, TITLE = ?, BODY = ?, DATETIME = ? WHERE ID = {rowid}', (rowid - 1, row[1], row[2], row[3], row[4]))
        
        self.database.commit()
        return "Successful"
    
    def close(self):
        '''
        Closes the database
        '''
        self.database.close() # Close the database