# Import libraries
from PyQt5 import QtWidgets, QtCore, QtGui

# Import scripts
from src import login
from src import connecter

# Other windows
class createProjectApp(QtWidgets.QMainWindow):
    
    def __init__(self):
        pass

# Main
class App(QtWidgets.QSystemTrayIcon):
    
    def __init__(self, app):
        QtWidgets.QSystemTrayIcon.__init__(self)
        
        # Adding an icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setIcon(icon)
        
        # Adding item on the menu bar
        self.setVisible(True)
        
        # Load connecter
        self.connection = connecter.ConnectingWindow()
        self.connection.appClose.connect(app.quit)
        self.connection.show()
        
        # Creating the options
        self.menu = QtWidgets.QMenu()
        
        self.createProject = QtWidgets.QAction("Create project")
        self.createProject.triggered.connect(self.createProjectFunc)
        self.menu.addAction(self.createProject)
        
        self.quit = QtWidgets.QAction("Quit")
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)
        
        self.setContextMenu(self.menu)
        
        # Create variables
        self.loginWindow = None
        
    def createProjectFunc(self):
        pass
            
    def startConnection(self):
        # Start connection
        if self.connection != None:
            self.connection.close()
            self.connection == None
            self.connection = connecter.ConnectingWindow()
            self.connection.show()
        else:
            self.connection = connecter.ConnectingWindow()
            self.connection.show()