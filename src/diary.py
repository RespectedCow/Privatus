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
    destroyEntryEvent = QtCore.pyqtSignal(int)
    
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
        self.entries = {}
        
        # Set triggers
        self.newEntry.clicked.connect(self.createEntry)
        self.deleteButton.clicked.connect(self.destroyEntry)
        
    def destroyEntry(self):
        currentItem = self.entriesWidget.currentItem()
        
        if currentItem == None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.warning)
            msg.setWindowIcon(self.icon)
            msg.setText("You have not selected an entry")
            msg.setWindowTitle("Error!")
                
            retval = msg.exec_()
            
            return
        
        title = currentItem.text(1)
        datetime = currentItem.text(0)
        
        results = findEntry(self.entries, title, datetime)
        
        if results != None:
            self.destroyEntryEvent.emit(results)
        
    def loadEntries(self, entries):
        # Clear the tree widget
        self.entriesWidget.clear()
        self.entries.clear()

        # Load the entries
        sortedEntries = sorted(entries, key=lambda t: datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S'))
        
        for entry in sortedEntries:
            self.entries[entry[0]] = (entry[2], entry[4])
            newEntry = QtWidgets.QTreeWidgetItem(self.entriesWidget, [entry[4], entry[2]])
        
    def createEntry(self):
        if self.createEntryWindow == None:
            self.createEntryWindow = createEntry()
            self.createEntryWindow.createEntryEvent.connect(self.createEntryEvent.emit)
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()
        else:
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()
            
            
# Functions
def findEntry(entries, title, datetime):
    
    for id, data in entries.items():
        if data[0] == title and data[1] == datetime:
            return id
        
    return None