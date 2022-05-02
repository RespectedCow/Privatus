'''
Helps the program connect to the server.
'''

# Importing libraries
import socket, time, yaml, json, struct
from PyQt5 import QtWidgets, QtGui, QtCore, uic
import threading

# Scripts
from src import login

# Functions
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = json.dumps(msg).encode()
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    message = recvall(sock, msglen)
    if message != None:
        message = json.loads(message)
    return message

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# Classes
class ConnectingWindow(QtWidgets.QMainWindow):
    messageReceived = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal()
    connected = QtCore.pyqtSignal()
    appClose = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load UI
        uic.loadUi("./lib/uis/connectToServer.ui", self)
        
        # Set icon and title
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(icon)
        
        self.setWindowTitle("Connecting to server")
        
        # Class variables
        self.loginWindow = login.LoginWindow()
        self.isConnected = False
        
        # Start Thread
        self.connection = ConnectToServer()
        
        # Connect to signals
        self.connection.setProgress.connect(self.progressBar.setValue)
        self.connection.connected.connect(self.connected)
        self.connection.finishedProgress.connect(self.hide)
        self.connection.connectionLost.connect(self.connectionRefused)
        self.connection.createLoginWindow.connect(self.login)
        self.connection.hide.connect(self.hide)
        self.connection.show.connect(self.show)
        self.connection.setLabel.connect(self.label.setText)
        
        # Start thread
        self.connection.start()
        
    def connectionRefused(self, int):
        if int == 1:
            self.label.setText("Connection refused. Server might be down.")
        elif int == 2:
            self.label.setText("You may not be connected to the internet.")
        elif int == 3:
            self.label.setText("Connected reset.")
        else:
            self.label.setText("Unexplained error.")     
            
        self.isConnected = False
            
    def login(self):
        if self.loginWindow == None:
            self.loginWindow = login.LoginWindow()
            self.loginWindow.logEvent.connect(self.loggedIn)
            self.loginWindow.appClose.connect(self.appClose.emit)
            self.loginWindow.show()
        else:
            self.loginWindow.logEvent.connect(self.loggedIn)
            self.loginWindow.appClose.connect(self.appClose.emit)
            self.loginWindow.show()
            
    def loggedIn(self):
        self.loginWindow.hide()
        self.connection.start()
        
    def connected(self):
        self.isConnected = True
        
    def close(self):
        self.isConnected = False
        self.connection.close()
        
        
class ConnectToServer(QtCore.QThread):
    setProgress = QtCore.pyqtSignal(int)
    finishedProgress = QtCore.pyqtSignal()
    setLabel = QtCore.pyqtSignal(str)
    messageReceived = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal(int)
    connected = QtCore.pyqtSignal()
    createLoginWindow = QtCore.pyqtSignal()
    hide = QtCore.pyqtSignal()
    show = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.server = "192.168.56.1"
        self.port = 2222
        
        self.isConnected = False
        
    def reconnect(self):
        time.sleep(3)
        # Attempt a reconnect
        self.setLabel.emit("Reconnecting")
        time.sleep(2)
        self.run()

    def run(self):
        self.show.emit()
        self.setProgress.emit(0)
        self.setLabel.emit("Connecting to server")
        
        # For visual effects
        for i in range(26):
            self.setProgress.emit(i)
            time.sleep(0.005)
            
        # Check if user entered login credentials
        with open("./data/login.yaml", 'r') as stream:
            loginCres = yaml.safe_load(stream)
        
        if loginCres == None or loginCres['username'] == None or loginCres['password'] == None:
            self.setLabel.emit("User needs to enter login credentials")
            time.sleep(2)
            self.hide.emit()
            self.createLoginWindow.emit()
        else:
            self.socket = None
            
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server, self.port))
            except ConnectionRefusedError:
                self.connectionLost.emit(1)
                
                self.reconnect()
                return
            except OSError:
                self.connectionLost.emit(2)
                
                self.reconnect()
                return
            except:
                self.reconnect()
                return
            
            # If successfully connected, send identification
            username = loginCres['username'] # Get it
            password = loginCres['password']
            
            send_msg(self.socket, { 
                'username': username,
                'password': password
            })
            
            # Get results
            results = recv_msg(self.socket)
            print(results)
            
            if results == "Success":
                self.setProgress.emit(100)
                self.setLabel.emit("Connected")
                time.sleep(1)
                self.hide.emit()
                
                self.connected.emit()
                self.isConnected = True
            else:
                self.setLabel.emit(results)
                time.sleep(1)
                self.hide.emit()
                self.createLoginWindow.emit()
                
            threading.Thread(target=self.check_status).start()
                
    def close(self):
        self.socket.close()
        
    def check_status(self):
        while True:
            if not self.isConnected:
                break
            
            # Check status
            try:
                response = self.sendInput('checkStatus', {})
                
                if response != "OK":
                    # Error handling
                    pass
            except Exception as e:
                self.show.emit()
                self.run()
                break
            
            time.sleep(5)
                
    def sendInput(self, action, params):
        '''
        Format:
        input = {
            'status': 0,
            'message': {
                'action': action,
                'params': params
            }
        }
        '''
        
        input = {
            'status': 0,
            'message': {
                'action': action,
                'params': params
            }
        }
        
        if self.isConnected:
            try:
                send_msg(self.socket, input)

                response = recv_msg(self.socket)

                return response
            except Exception as e:
                self.show.emit()
                self.run()