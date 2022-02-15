# Importing libraries
import curses
import sys

# Importing scripts

# Functions
def filter(input):
        
    if input == curses.KEY_UP:
        return curses.KEY_UP
    if input == curses.KEY_DOWN:
        return curses.KEY_DOWN
    if input == curses.KEY_RIGHT:
        return curses.KEY_RIGHT
    if input == curses.KEY_LEFT:
        return curses.KEY_LEFT
    if input == 8 or input == 127 or input == curses.KEY_BACKSPACE:
        return curses.KEY_BACKSPACE
    
    if input == -1:
        return None
    else:
        return chr(input)

# Classes
class Console:
    
    def __init__(self, stopEvent): # The interpreter argument needs to be a function
        self.screen = curses.initscr()
        curses.start_color()
        
        # Settings
        curses.noecho()
        curses.cbreak()
        
        self.screen.nodelay(1)
        self.screen.keypad(True)
        
        # Values
        self.y, self.x = self.screen.getmaxyx()
        
        self.running = False
        self.interpreter = None
        self.stopEvent = stopEvent
        self.displaywinScroll_y = 0
        
        self.displayWindowSize_y = self.y + 100
        self.displayWindowSize_x = self.x
        
        # Display window
        self.displayWindow = curses.newpad(self.displayWindowSize_y, self.displayWindowSize_x)  
        
        # Create header
        header_text = "PROJECT OASIS"
        extender = " " * (self.x - len(header_text))
        
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
        self.screen.addstr(0, 0, header_text + extender, curses.color_pair(1))
        
        # Create textbox
        self.textbox_str = ""
        self.textbox_y = self.y - 1
        self.textbox_x = 1
        
        self.screen.addstr(self.textbox_y, self.textbox_x, "> ")
        
        # Initialization
        self.update()
        
        self.print("Project Oasis Server Console Version [0.1] \n")
        
    def run(self):
        self.running = True

        while True:
            
            if self.running == False:
                break
            
            # Get user input
            input = filter(self.screen.getch())
            
            if input == curses.KEY_UP:
                if self.displaywinScroll_y != 0:
                    self.displaywinScroll_y -= 1
                    self.update()
            elif input == curses.KEY_DOWN:
                if self.displaywinScroll_y != self.displayWindowSize_y - 1:
                    self.displaywinScroll_y += 1
                    self.update()
            elif input == curses.KEY_BACKSPACE:
                if self.textbox_str != "":
                    self.textbox_str = self.textbox_str[:-1]
                    self.screen.addstr("\b \b")
                    self.update()
            
            if type(input) == str:
                self.key_pressed(input)
            
    def end(self):
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(0)
        self.screen.nodelay(0)
        self.screen.keypad(True)
        curses.endwin()
        
        self.running = False
        
        if self.stopEvent != None:
            self.stopEvent()
        
    def print(self, str):
        self.displayWindow.addstr(str + "\n")
        self.update()
        
    def update(self):
        self.displayWindow.refresh(self.displaywinScroll_y, 0, 1, 0, self.y - 2, self.x - 1)
        self.screen.refresh()
        
    def interprete_command(self):
        command_array = self.textbox_str.split()
        isMatched = False
        
        if command_array[0] == "exit":
            isMatched = True
            self.end()
            
        # Passes the command issued by the console to the server object if it is not matched
        if self.interpreter != None:
            results = self.interpreter(command_array)
            
            if results:
                isMatched = True
                self.print(results)
            
        if isMatched == False:
            return "Invalid command"
        
    def connect_interpreter(self, interpreter_func):
        self.interpreter = interpreter_func
            
    def key_pressed(self, key):
        if key == "\t":
            self.textbox_str = self.textbox_str + (" " * 5)
            self.screen.addstr(key)
            self.update()
            
            return
        
        if key != "\n":
            self.textbox_str = self.textbox_str + key
            self.screen.addstr(key)
            self.update()
            
            return
        elif self.textbox_str != "":
            # Process the textbox data
            results = self.interprete_command()
            
            if results != None:
                self.print(results)
            
            # Clear the textbox
            self.screen.addstr("\b \b" * len(self.textbox_str))
            self.textbox_str = ""
            
            self.update()
        
# Main event function
def main():
    def stopEvent():
        pass
    
    console = Console(stopEvent)
    console.run()

if __name__ == "__main__":
    main()