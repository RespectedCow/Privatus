# Importing libraries
from operator import index
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from datetime import datetime
from Crypto.Cipher import AES
from Crypto import Random
import hashlib, base64

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


class diaryLogin(QtWidgets.QMainWindow):
    
    showMainDiary = QtCore.pyqtSignal(str)
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        
        # Load the ui
        uic.loadUi("lib/uis/diaryLogin.ui", self)
        
        # Set window attributes
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Diary login")
        
        # Class variables
        self.stopLoop = False
        
        # Set triggers
        self.loginButton.clicked.connect(self.loginButtonClicked)
        
        # Call functions
        self.show()
        
    def loginButtonClicked(self):
        passphrase = self.passwordEdit.toPlainText()
        
        if passphrase == "" or passphrase == None:
            QtWidgets.QMessageBox.warning(self, "Error!", "You cannot leave the passphrase field blank!", QtWidgets.QMessageBox.Ok)
            
            return
        
        self.showMainDiary.emit(passphrase)
        self.close()


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
        
        self.setFields(entry[2], entry[3])
        
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
    
    def __init__(self, connection):
        QtWidgets.QMainWindow.__init__(self)
        
        # Get encryption passphrase
        self.diaryLoginWindow = diaryLogin()
        self.diaryLoginWindow.show()
        
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
        self.connection = connection
        self.passphrase = None
        self.entries = {}
        
        # Set triggers
        self.newEntry.clicked.connect(self.createEntry)
        self.deleteButton.clicked.connect(self.destroyEntry)
        self.searchButton.clicked.connect(self.searchEntries)
        self.showButton.clicked.connect(self.showEntryBroadcast)
        self.editButton.clicked.connect(self.openEditWindow)
        
        self.diaryLoginWindow.showMainDiary.connect(self.open)
        
    def open(self, passphrase):
        passphrase = passphrase.encode()
        self.passphrase = AESCipher(passphrase)
        
        self.loadEntries()
        self.show()
        
    def searchEntries(self):
        potential_entries = []
        searchterm = self.searchBar.text()
        
        for entry in self.entries:
            if searchterm in entry[2]:
                potential_entries.append(entry)
                
        self.loadEntries(potential_entries)
        
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
            self.editEntryWindow = editEntry(findEntryWithID(self.entries, results), results)
            self.editEntryWindow.editEntryEvent.connect(self.editEntryFunc)
            self.editEntryWindow.show()
        
    def editEntryFunc(self, title, content, id):
        title = self.passphrase.encrypt(title)
        content = self.passphrase.encrypt(content)
        
        title = title.decode()
        content = content.decode()
        
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
        
    def loadEntries(self, entries=None):
        
        if entries == None:
            entries = self.connection.connection.sendInput('getEntries',{})
            entries = self.decryptEntries(entries)
            self.entries = entries
        
        # Clear the tree widget
        self.entriesWidget.clear()

        # Load the entries
        sortedEntries = sorted(entries, key=lambda t: datetime.strptime(t[4], '%Y-%m-%d %H:%M:%S'), reverse=True)

        for entry in sortedEntries:
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
        
        # Decrypt the entry
        entry[2] = self.passphrase.decrypt(entry[2])
        entry[3] = self.passphrase.decrypt(entry[3])
        
        self.showEntryWindow = showEntry(entry)
        self.showEntryWindow.show()
        
    def createEntry(self):
        if self.createEntryWindow == None:
            self.createEntryWindow = createEntry()
            self.createEntryWindow.createEntryEvent.connect(self.createEntryClicked)
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()
        else:
            self.createEntryWindow.resetFields()
            self.createEntryWindow.show()
            
    def decryptEntries(self, entries):
        index = 0
        for entry in entries:
            entries[index][2] = self.passphrase.decrypt(entry[2])
            entries[index][3] = self.passphrase.decrypt(entry[3])
                
            index += 1
        
        return entries
            
    def createEntryClicked(self, title, content):
        title = self.passphrase.encrypt(title)
        content = self.passphrase.encrypt(content)
        
        title = title.decode()
        content = content.decode()
        
        self.createEntryEvent.emit(title, content)
            
            
# Functions
def findEntry(entries, title, datetime):
    
    for entry in entries:
        if entry[2] == title and entry[4] == datetime:
            return entry[0]
        
    return None

def findEntryWithID(entries, id):
    
    for entry in entries:
        if entry[0] == id:
            return entry
    
    return None