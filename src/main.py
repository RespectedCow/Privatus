# Import libraries
from PyQt5 import QtWidgets, QtCore, QtGui
import yaml
import io

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
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setIcon(self.icon)
        
        # Adding item on the menu bar
        self.setVisible(True)
        
        # Load connecter
        self.connection = connecter.ConnectingWindow()
        self.connection.appClose.connect(app.quit)
        self.connection.show()
        
        # Creating the options/submenu
        self.menu = QtWidgets.QMenu()
        
        self.featuresmenu = QtWidgets.QMenu("Features")
        
        self.createProject = QtWidgets.QAction("Create new dairy/entry")
        self.createProject.triggered.connect(self.createProjectFunc)
        self.featuresmenu.addAction(self.createProject)
        self.menu.addMenu(self.featuresmenu)
        self.menu.addSeparator()

        self.logoutAction = QtWidgets.QAction("Logout")
        self.logoutAction.triggered.connect(self.logout)
        self.menu.addAction(self.logoutAction)
        
        self.quit = QtWidgets.QAction("Quit")
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)
        
        self.setContextMenu(self.menu)
        
        # Create variables
        self.loginWindow = None
        self.app = app
        
    def createProjectFunc(self):
        pass
    
    def logout(self):
        # Check if connection exists
        if self.connection != None:
            if self.connection.isConnected:
                self.connection.close()
                
                # Clear yaml file
                with io.open('./data/login.yaml', 'w', encoding='utf8') as outfile:
                    yaml.dump(None, outfile)
                    
                # Create login screen
                self.connection = None
                self.connection = connecter.ConnectingWindow()
                self.connection.appClose.connect(self.app.quit)
                self.connection.show()
            else:
                print("You are not connected to the server")
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowIcon(self.icon)
                msg.setText("You are not connected to the server")
                msg.setWindowTitle("Not connected")
                
                retval = msg.exec_()
            
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