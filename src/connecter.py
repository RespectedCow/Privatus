'''
Helps the program connect to the server.
'''

# Importing libraries
import socket, time, yaml, json, struct, sys, os, base64, hashlib
from PyQt5 import QtWidgets, QtGui, QtCore
import threading
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

# Scripts
from src import login

# Functions
def send_msg(sock, msg, public_key=None):
    # Prefix each message with a 4-byte length (network byte order)
    if type(msg) != bytes:
        msg = json.dumps(msg)
        msg = msg.encode()
    
    if public_key:
        if type(public_key) == PKCS1_OAEP.PKCS1OAEP_Cipher:
            msg = public_key.encrypt(msg)
        if type(public_key) == AESCipher:
            msg = msg.decode()
            msg = public_key.encrypt(msg)
    
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock, private_key=None):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    message = recvall(sock, msglen)
    if message != None:
        if private_key:
            message = private_key.decrypt(message)
        else:
            message = message.decode()
            
        try:
            message = message.decode()
        except:
            pass
        
        if type(message) != bytes:
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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Classes
class AESCipher(object):
    
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class ConnectingWindow(QtWidgets.QMainWindow):
    messageReceived = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal()
    connected = QtCore.pyqtSignal()
    appClose = QtCore.pyqtSignal()
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load UI
        # uic.loadUi("./lib/uis/connectToServer.ui", self)
        self.resize(428, 116)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 50, 351, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 30, 271, 16))
        self.label.setObjectName("label")
        self.setCentralWidget(self.centralwidget)
        
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
        self.private_key = None
        self.s_public_key = None
        self.aes_key = None
        
        with open("package.yaml", 'r') as stream:
            data = yaml.safe_load(stream)
            
        if 'server' in data:
            self.server = data["server"]
            
        print(self.server)
        
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
            
            # If successfully connected, send public key
            random_generator = Random.new().read
            self.private_key = RSA.generate(1024, random_generator)
            public_key = self.private_key.publickey()
            self.private_key = PKCS1_OAEP.new(self.private_key)
            
            send_msg(self.socket, public_key.exportKey().decode())
            print("Sent server our public key")
            
            # After receiving the server's public key, send our encrypted login credentials
            self.s_public_key = recv_msg(self.socket)
            self.s_public_key = RSA.importKey(self.s_public_key)
            self.s_public_key = PKCS1_OAEP.new(self.s_public_key)
            
            if self.s_public_key:
                username = loginCres['username'] # Get it
                password = loginCres['password']
                
                send_msg(self.socket, { 
                    'username': username,
                    'password': password
                }, self.s_public_key)
            
            # Get results
            results = recv_msg(self.socket, self.private_key)
            print(results)
            
            if results == "Success":
                self.setProgress.emit(100)
                self.setLabel.emit("Connected")
                time.sleep(1)
                self.hide.emit()
                
                self.connected.emit()
                self.isConnected = True
                
                # Receive aes key
                self.aes_key = recv_msg(self.socket, self.private_key)
                self.aes_key = AESCipher(self.aes_key)
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
                print(str(e) + "e")
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
                send_msg(self.socket, input, self.aes_key)

                response = recv_msg(self.socket, self.aes_key)

                return response
            except Exception as e:
                print(e)
                self.show.emit()
                self.run()