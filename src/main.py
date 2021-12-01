# Import libraries
from PyQt5 import QtWidgets, QtCore, QtGui
import yaml
import io

# Import scripts
from src import login
from src import connecter
from src import diary

# Other windows

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
        
        self.createDiary = QtWidgets.QAction("Create new diary/entry")
        self.createDiary.triggered.connect(self.diaryFunc)
        self.featuresmenu.addAction(self.createDiary)
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
        self.diaryWindow = None
        self.app = app
        
    def diaryFunc(self):
        if self.diaryWindow == None and self.connection.isConnected:
            self.diaryWindow = diary.Main()
            self.diaryWindow.loadEntries(self.connection.connection.sendInput('getEntries',{}))
            self.diaryWindow.createEntryEvent.connect(self.createEntryFunc)
            self.diaryWindow.destroyEntryEvent.connect(self.destroyEntry)
            self.diaryWindow.show()
        elif self.connection.isConnected:
            self.diaryWindow.loadEntries(self.connection.connection.sendInput('getEntries',{}))
            self.diaryWindow.show()
        else:
            print("You are not connected to the server")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowIcon(self.icon)
            msg.setText("You are not connected to the server")
            msg.setWindowTitle("Not connected")
            
            msg.exec_()
            
    def createEntryFunc(self, title, content):
        # Send the title and content to the server
        self.connection.connection.sendInput("createEntry", {
            'title': title,
            'content': content
        })
        
        self.diaryWindow.loadEntries(self.connection.connection.sendInput('getEntries', {}))
        
    def destroyEntry(self, id):
        self.connection.connection.sendInput('deleteEntry', {
            'id': id
        })
        
        self.diaryWindow.loadEntries(self.connection.connection.sendInput('getEntries', {}))
    
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