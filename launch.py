"""
This script will basically act as the launcher for the application.

The purpose of this application is to be able to manage the user's computer and automate tasks.
"""
# Importing libraries
from PyQt5 import QtCore, QtWidgets, QtGui
import sys

# Import scripts
from src import main as maingui

# Starting up
def main():
    app = QtWidgets.QApplication.instance()

    # check apps
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Another instance of the application is running!")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes)

        retval = msg.exec_()

    app.setQuitOnLastWindowClosed(False)
    app.setStyle("Windows")
    window = maingui.App(app)
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()