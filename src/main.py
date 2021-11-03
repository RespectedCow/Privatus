# Import libraries
from PyQt5 import QtWidgets, QtCore, QtGui

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
        
        # Creating the options
        self.menu = QtWidgets.QMenu()
        
        # To quit the app
        self.quit = QtWidgets.QAction("Quit")
        self.quit.triggered.connect(app.quit)
        self.menu.addAction(self.quit)
        
        self.setContextMenu(self.menu)
        