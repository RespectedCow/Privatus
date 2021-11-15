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
    appClose = QtCore.pyqtSignal()
    
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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        
        # Mess with ui
        self.warning.hide()
        self.stackUnder(self.label_4)
        self.closeButton.setStyleSheet("""
                                       #closeButton {
                                           color: black; 
                                           background: transparent;
                                       }
                                       
                                       #closeButton:Hover {
                                           background-color: rgb(214,0,0);
                                           border: none;
                                       }
                                       """)
        
        self.minimiseButton.setStyleSheet("""
                                          #minimiseButton {
                                            color: black; 
                                            background: transparent;
                                          }
                                          
                                          #minimiseButton:Hover {
                                              background-color: grey;
                                              border: none;
                                          }
                                          """)
        
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.closeButton.setGraphicsEffect(opacity_effect)
        self.minimiseButton.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(0.5)
        
        # Set triggers
        self.loginButton.clicked.connect(self.login)
        self.closeButton.clicked.connect(self.appClose.emit)
        self.minimiseButton.clicked.connect(self.showMinimized)
        
        # Class variables
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False
        
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
        
    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.width(),
                                self.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        
    def login(self):
        username = self.username.toPlainText()
        password = self.password.toPlainText()
        
        # Check if username and password is valid
        if username == "" or password == "":
            self.warning.show()
            self.warning.setText("Username or password fields cannot be blank!")
            return
        
        # Write to the file.
        with io.open('./data/login.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump({
                'username': username,
                'password': password
            }, outfile)
            
        # Emit signal
        self.logEvent.emit()