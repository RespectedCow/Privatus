# Importing libraries
from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime

# Classes
class showEntry(QtWidgets.QMainWindow):
    
    def __init__(self, entry):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load the ui
        self.setObjectName("MainWindow")
        self.resize(424, 506)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.content = QtWidgets.QTextBrowser(self.centralwidget)
        self.content.setGeometry(QtCore.QRect(10, 70, 401, 381))
        self.content.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.content.setMarkdown("")
        self.content.setObjectName("content")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(20, 20, 391, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(13)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.creationLabel = QtWidgets.QLabel(self.centralwidget)
        self.creationLabel.setGeometry(QtCore.QRect(30, 36, 141, 16))
        self.creationLabel.setObjectName("creationLabel")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 424, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
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
        self.setObjectName("MainWindow")
        self.resize(432, 453)
        self.setMinimumSize(QtCore.QSize(432, 453))
        self.setMaximumSize(QtCore.QSize(432, 453))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("ENTRY TITLE")
        self.contentEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.contentEdit.setGeometry(QtCore.QRect(20, 90, 391, 291))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.contentEdit.setFont(font)
        self.contentEdit.setLineWidth(0)
        self.contentEdit.setMidLineWidth(0)
        self.contentEdit.setObjectName("contentEdit")
        self.contentEdit.setPlaceholderText("Today was a good day")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("CONTENT")
        self.createEntryButton = QtWidgets.QPushButton(self.centralwidget)
        self.createEntryButton.setGeometry(QtCore.QRect(150, 390, 111, 41))
        self.createEntryButton.setObjectName("createEntryButton")
        self.createEntryButton.setText("Create entry")
        self.titleEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleEdit.setGeometry(QtCore.QRect(20, 30, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleEdit.setFont(font)
        self.titleEdit.setAutoFillBackground(False)
        self.titleEdit.setObjectName("titleEdit")
        self.titleEdit.setPlaceholderText("Good day")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 432, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
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
        self.setObjectName("MainWindow")
        self.resize(432, 453)
        self.setMinimumSize(QtCore.QSize(432, 453))
        self.setMaximumSize(QtCore.QSize(432, 453))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("ENTRY TITLE")
        self.contentEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.contentEdit.setGeometry(QtCore.QRect(20, 90, 391, 291))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.contentEdit.setFont(font)
        self.contentEdit.setLineWidth(0)
        self.contentEdit.setMidLineWidth(0)
        self.contentEdit.setObjectName("contentEdit")
        self.contentEdit.setPlaceholderText("Today was a good day")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("CONTENT")
        self.createEntryButton = QtWidgets.QPushButton(self.centralwidget)
        self.createEntryButton.setGeometry(QtCore.QRect(150, 390, 111, 41))
        self.createEntryButton.setObjectName("createEntryButton")
        self.createEntryButton.setText("Create entry")
        self.titleEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleEdit.setGeometry(QtCore.QRect(20, 30, 391, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleEdit.setFont(font)
        self.titleEdit.setAutoFillBackground(False)
        self.titleEdit.setObjectName("titleEdit")
        self.titleEdit.setPlaceholderText("Good day")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 432, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
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
        self.setObjectName("MainWindow")
        self.resize(545, 545)
        self.setMinimumSize(QtCore.QSize(545, 545))
        self.setMaximumSize(QtCore.QSize(545, 545))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.newEntry = QtWidgets.QPushButton(self.centralwidget)
        self.newEntry.setGeometry(QtCore.QRect(434, 30, 91, 41))
        self.newEntry.setObjectName("newEntry")
        self.newEntry.setText("New entry")
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(20, 30, 311, 41))
        self.searchBar.setObjectName("searchBar")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(340, 30, 81, 41))
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        self.entriesWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.entriesWidget.setGeometry(QtCore.QRect(20, 100, 501, 371))
        self.entriesWidget.setIndentation(0)
        self.entriesWidget.setObjectName("entriesWidget")
        self.entriesWidget.header().setDefaultSectionSize(250)
        self.entriesWidget.header().setMinimumSectionSize(0)
        self.entriesWidget.setColumnCount(2)
        self.entriesWidget.setHeaderLabels(["Date", "Title"])
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(430, 480, 91, 31))
        self.editButton.setObjectName("editButton")
        self.editButton.setText("Edit")
        self.showButton = QtWidgets.QPushButton(self.centralwidget)
        self.showButton.setGeometry(QtCore.QRect(330, 480, 91, 31))
        self.showButton.setObjectName("showButton")
        self.showButton.setText("Show")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(230, 480, 91, 31))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setText("Delete")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 545, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        
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
        
        # If an error occurs
        if entries == None or entries == []:
            QtWidgets.QMessageBox.information(self, "Create one!", "You have no entries.", QtWidgets.QMessageBox.Ok)
            
            entries = []
            return

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