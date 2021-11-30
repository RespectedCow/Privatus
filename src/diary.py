# Importing libraries
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from datetime import datetime
# Classes
class createEntry(QtWidgets.QMainWindow):
    
    createEntryEvent = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load ui
        uic.loadUi("./lib/uis/createEntry.ui", self)
        
        # Set window attributes
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Create an entry")
        
        # Set triggers
        self.createEntryButton.clicked.connect(self.createEntry)
        
    def createEntry(self):
        title = self.titleEdit.text()
        content = self.contentEdit.toPlainText()
        
        # Check the contents
        if title == "" or content == "":
            QtWidgets.QMessageBox.warning(self, "Error!", "You cannot create an entry with an empty title or body", QtWidgets.QMessageBox.Ok)
            
            return

        self.createEntryEvent.emit(title, content)
        self.close()
        
    def resetFields(self):
        self.titleEdit.setText("")
        self.contentEdit.setText("")

class Main(QtWidgets.QMainWindow):
    
    createEntryEvent = QtCore.pyqtSignal(str, str)
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load ui
        uic.loadUi("./lib/uis/diaryWindow.ui", self)
        
        # Set window attributes
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Your diary")
        
        # Class variables
        self.createEntryWindow = None
        
        # Set triggers
        self.newEntry.clicked.connect(self.createEntry)
        
    def loadEntries(self, entries):
        # Clear the tree widget
        self.entriesWidget.clear()

        # Load the entries
        sortedEntries = sorted(entries, key=lambda t: datetime.strptime(t[3], '%Y-%m-%d %H:%M:%S'))
        
        for entry in sortedEntries:
            newEntry = QtWidgets.QTreeWidgetItem(self.entriesWidget, [entry[3], entry[1]])
        
    def createEntry(self):
        if self.createEntryWindow == None:
            self.createEntryWindow = createEntry()
            self.createEntryWindow.createEntryEvent.connect(self.createEntryEvent.emit)
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()
        else:
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()