# Import libraries
from PyQt5 import QtWidgets, QtCore, QtGui

# Import scripts
from src import login
from src import connecter

# Main
class App(QtWidgets.QSystemTrayIcon):
    
    def __init__(self, app):
        QtWidgets.QSystemTrayIcon.__init__(self)
        
        # Start connection
        self.connection = connecter.ConnectingWindow()
        self.connection.show()
        
        # Adding an icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setIcon(icon)
        
        # Adding item on the menu bar
        self.setVisible(True)
        
        # Creating the options
        self.menu = QtWidgets.QMenu()
        
        self.login = QtWidgets.QAction("Login")
        self.login.triggered.connect(self.openLoginWindow)
        self.menu.addAction(self.login)
        
        # To quit the app
        self.quit = QtWidgets.QAction("Quit")
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)
        
        self.setContextMenu(self.menu)
        
        # Create variables
        self.loginWindow = None
        
    def openLoginWindow(self):
        if self.loginWindow == None:
            self.loginWindow = login.LoginWindow()
            self.loginWindow.show()
        else:
            self.loginWindow.show()
            
    def startConnection(self):
        # Start connection
        self.connection = connecter.ConnectingWindow()
        self.connection.show()