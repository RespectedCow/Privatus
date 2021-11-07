'''
Helps the program connect to the server.
'''

# Importing libraries
import socket
import time
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import yaml
from src import login

# Classes
class ConnectingWindow(QtWidgets.QMainWindow):
    messageReceived = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal()
    connected = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load UI
        uic.loadUi("./lib/uis/connectToServer.ui", self)
        
        # Set icon and title
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        
        self.setWindowTitle("Connecting to server")
        
        # Start Thread
        self.connection = ConnectToServer()
        
        # Connect to signals
        self.connection.setProgress.connect(self.progress)
        self.connection.finishedProgress.connect(self.hide)
        self.connection.connectionLost.connect(self.connectionRefused)
        self.connection.setLabel.connect(self.label.setText)
        
        # Start thread
        self.connection.start()
        
    def progress(self, int):
        self.progressBar.setValue(int)
        
    def connectionRefused(self, int):
        if int == 1:
            self.label.setText("Connection refused. Server might be down.")
        elif int == 2:
            self.label.setText("You may not be connected to the internet.")
        else:
            self.label.setText("Unexplained error.")     
        
        
class ConnectToServer(QtCore.QThread):
    setProgress = QtCore.pyqtSignal(int)
    finishedProgress = QtCore.pyqtSignal()
    setLabel = QtCore.pyqtSignal(str)
    messageReceived = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal(int)
    connected = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.server = "192.168.0.191"
        self.port = 3333

    def run(self):
        self.setProgress.emit(0)
        self.setLabel.emit("Connecting to server")
        
        # For visual effects
        for i in range(26):
            self.setProgress.emit(i)
            time.sleep(0.005)
            
        # Check if user entered login credentials
        with open("./data/login.yaml", 'r') as stream:
            loginCres = yaml.safe_load(stream)
            
        if not loginCres['username'] and not loginCres['password']:
            if self.loginWindow == None:
                self.loginWindow = login.LoginWindow()
                self.loginWindow.show()
            else:
                self.loginWindow.show()
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                self.socket.connect((self.server, self.port))
            except ConnectionRefusedError:
                self.connectionLost.emit(1)
            except OSError:
                self.connectionLost.emit(2)
            finally:
                time.sleep(3)
                # Attempt a reconnect
                self.setLabel.emit("Reconnecting")
                time.sleep(2)
                self.run()
            
        # If successfully connected, send identification
        