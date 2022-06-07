'''
This will take care of signing up and logging in
'''

# Importing libraries
from PyQt5 import QtWidgets, QtGui, QtCore
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
        self.resize(500, 320)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(-10, -10, 521, 341))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("farm.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setGeometry(QtCore.QRect(200, 220, 91, 41))
        self.loginButton.setObjectName("loginButton")
        self.loginButton.setText("Login")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 80, 47, 13))
        self.label.setObjectName("label")
        self.label.setText("Username")
        self.username = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(170, 100, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.username.setFont(font)
        self.username.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.username.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.username.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.username.setPlainText("")
        self.username.setTabStopWidth(30)
        self.username.setObjectName("username")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 140, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Password")
        self.password = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(170, 160, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.password.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.password.setObjectName("password")
        self.password.setPlaceholderText("password321")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 41, 41))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("cowicon.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.warning = QtWidgets.QLabel(self.centralwidget)
        self.warning.setEnabled(False)
        self.warning.setGeometry(QtCore.QRect(80, 19, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.warning.setFont(font)
        self.warning.setStyleSheet("color: red;")
        self.warning.setAlignment(QtCore.Qt.AlignCenter)
        self.warning.setWordWrap(True)
        self.warning.setObjectName("warning")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(460, 2, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.closeButton.setFont(font)
        self.closeButton.setStyleSheet("color: black; background: transparent;")
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setText("X")
        self.minimiseButton = QtWidgets.QPushButton(self.centralwidget)
        self.minimiseButton.setGeometry(QtCore.QRect(430, 2, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.minimiseButton.setFont(font)
        self.minimiseButton.setStyleSheet("color: black; background: transparent;")
        self.minimiseButton.setObjectName("minimiseButton")
        self.minimiseButton.setText("_")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
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