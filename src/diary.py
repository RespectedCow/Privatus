# Importing libraries
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from datetime import datetime
# Classes
class showEntry(QtWidgets.QMainWindow):
    
    def __init__(self, entry):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load the ui
        uic.loadUi('./lib/uis/showEntry.ui', self)
        self.loadValues(entry)
        
        # Set window attributes
        self.setWindowTitle(entry[2])
        
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        
        self.setWindowIcon(self.icon)
        
    def loadValues(self, entry):
        self.titleLabel.setText(entry[2])
        self.creationLabel.setText(entry[4])
        self.content.setText(entry[3])


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
        

class editEntry(QtWidgets.QMainWindow):
    
    editEntryEvent = QtCore.pyqtSignal(str, str, int)
    
    def __init__(self, entry, id):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load ui
        uic.loadUi("./lib/uis/createEntry.ui", self)
        self.setFields(entry[0], entry[2])
        
        # Set window attributes
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Edit an entry")
        
        self.createEntryButton.setText("Edit entry")
        
        # Class variables
        self.id = id
        
        # Set triggers
        self.createEntryButton.clicked.connect(self.editEntry)
        
    def editEntry(self):
        title = self.titleEdit.text()
        content = self.contentEdit.toPlainText()
        
        # Check the contents
        if title == "" or content == "":
            QtWidgets.QMessageBox.warning(self, "Error!", "You cannot edit an entry with an empty title or body", QtWidgets.QMessageBox.Ok)
            
            return

        self.editEntryEvent.emit(title, content, self.id)
        self.close()
        
    def setFields(self, title, content):
        self.titleEdit.setText(title)
        self.contentEdit.setText(content)


class Main(QtWidgets.QMainWindow):
    
    createEntryEvent = QtCore.pyqtSignal(str, str)
    destroyEntryEvent = QtCore.pyqtSignal(int)
    searchEntriesEvent = QtCore.pyqtSignal(str)
    showEntryEvent = QtCore.pyqtSignal(int)
    editEntryEvent = QtCore.pyqtSignal(str, str, int)
    
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
        self.showEntryWindow = None
        self.editEntryWindow = None
        self.entries = {}
        
        # Set triggers
        self.newEntry.clicked.connect(self.createEntry)
        self.deleteButton.clicked.connect(self.destroyEntry)
        self.searchButton.clicked.connect(self.searchEntries)
        self.showButton.clicked.connect(self.showEntryBroadcast)
        self.editButton.clicked.connect(self.openEditWindow)
        
    def searchEntries(self):
        self.searchEntriesEvent.emit(self.searchBar.text())
        
    def openEditWindow(self):
        # Get current selected item
        currentItem = self.entriesWidget.currentItem()
        
        if currentItem == None:
            QtWidgets.QMessageBox.warning(self, "Error!", "You have not selected an entry", QtWidgets.QMessageBox.Ok)
            
            return
        
        title = currentItem.text(1)
        datetime = currentItem.text(0)
        
        results = findEntry(self.entries, title, datetime)
        
        if results != None:
            self.editEntryWindow = editEntry(self.entries[results], results)
            self.editEntryWindow.editEntryEvent.connect(self.editEntryFunc)
            self.editEntryWindow.show()
        
    def editEntryFunc(self, title, content, id):
        self.editEntryEvent.emit(title, content, id)
        
    def destroyEntry(self):
        currentItem = self.entriesWidget.currentItem()
        
        if currentItem == None:
            QtWidgets.QMessageBox.warning(self, "Error!", "You have not selected an entry", QtWidgets.QMessageBox.Ok)
            
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
        sortedEntries = sorted(entries, key=lambda t: datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S'), reverse=True)
        
        for entry in sortedEntries:
            self.entries[entry[0]] = (entry[2], entry[4], entry[3])
            newEntry = QtWidgets.QTreeWidgetItem(self.entriesWidget, [entry[4], entry[2]])
            
    def showEntryBroadcast(self):
        currentItem = self.entriesWidget.currentItem()
        
        if currentItem == None:
            QtWidgets.QMessageBox.warning(self, "Error!", "You have not selected an entry", QtWidgets.QMessageBox.Ok)
            
            return
        
        title = currentItem.text(1)
        datetime = currentItem.text(0)
        
        results = findEntry(self.entries, title, datetime)
        
        if results != None:
            self.showEntryEvent.emit(results)
            
    def show_entry(self, entry):
        self.showEntryWindow = showEntry(entry)
        self.showEntryWindow.show()
        
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