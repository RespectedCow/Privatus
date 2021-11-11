'''
This will take care of signing up and logging in
'''

# Importing libraries
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import yaml
import io

# Import scripts
from src import connecter

# Main login window
class LoginWindow(QtWidgets.QMainWindow):
    logEvent = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load UI
        uic.loadUi("./lib/uis/loginWindow.ui", self)
        
        # Add icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        
        # Set title
        self.setWindowTitle("Login")
        
        # Set triggers
        self.loginButton.clicked.connect(self.login)
        
    def login(self):
        username = self.username.toPlainText()
        password = self.password.toPlainText()
        
        # Write to the file.
        with io.open('./data/login.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump({
                'username': username,
                'password': password
            }, outfile)
            
        # Emit signal
        self.logEvent.emit()