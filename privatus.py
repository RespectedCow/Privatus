"""
This script will basically act as the launcher for the application.

The purpose of this application is to be able to manage the user's computer and automate tasks.
"""
# Importing libraries
from PyQt5 import QtCore, QtWidgets, QtGui
import yaml, sys, requests, webbrowser

# Import scripts
from src import main as maingui
from src import init

# Variables
init_functions = [
    init.init
]

# Starting up
def main():
    # Initialize pre-launch functions
    for fnc in init_functions:
        fnc = fnc()
        
        if fnc.check_init():
            fnc.run() # Will return any potential errors
        else:
            continue
    
    app = QtWidgets.QApplication.instance()

    # check apps
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText("Another instance of the application is running!")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes)
        
    updateApplication()
    
    # Startup the application
    app.setQuitOnLastWindowClosed(False)
    window = maingui.App(app)
    sys.exit(app.exec_())
    
# Functions
def getVerFromTag(tag):
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    
    version = ""
    for character in tag:
        if numbers.__contains__(character):
            version += character
        if character == "c" or character == "s":
            break
            
    return float(version)

def getUpdateWithVersion(version, updates_array):
    for update in updates_array:
        up_version = getVerFromTag(update[0])
        
        if up_version == version:
            return update

def getLastestVersion(array):
    """
    This function basically finds the highest number in an array
    """
    
    latest = 0
    for version, release in array:
        version = getVerFromTag(version)
        
        if version > latest:
            latest = version
            
    return latest

def updateApplication():
    
    # Checking for updates
    with open("version.yaml", 'r') as stream:
        data = yaml.safe_load(stream)
    
    l_version_f = getVerFromTag(data['version']) 
    
    try:
        releases = requests.get("https://api.github.com/repos/RespectedCow/Project-Oasis/releases")
    except requests.ConnectionError as e:
        e = str(e)
        
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(f"There was an error connecting to the github api! (Error: {e})")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        msg.exec_()
        
        return
      
    if releases.status_code == 200:  
        releases = releases.json()
        updates = []
        for release in releases:
            branch = release["target_commitish"]
            r_version = release["tag_name"]
            r_version_f = getVerFromTag(r_version)
            
            if branch == "main":
                # Check if r_version is higher than l_version if so then notify the userk
                if r_version_f > l_version_f:
                    updates.append((r_version, release))
                    
        latest_version = getLastestVersion(updates)
        latest_update = getUpdateWithVersion(latest_version, updates)
        
        # Check if user wants to update
        if latest_update != None: 
            msg = QtWidgets.QMessageBox()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"There's a new update availabel! \nDo you want to download it? (Version: {latest_update[0]})")
            msg.setWindowTitle("There's a update!") 
            yesButton = msg.addButton('Yes', QtWidgets.QMessageBox.YesRole)
            noButton = msg.addButton('No', QtWidgets.QMessageBox.NoRole)

            msg.exec_()
                        
            if msg.clickedButton() == yesButton:
                # Update the application
                pass
            elif msg.clickedButton() == noButton:
                return
            
            # Here is the actual updating occurs
            link = latest_update[1]["html_url"]
            webbrowser.open(link)
            
            sys.exit()
        
    elif release.status_code == 404:
        print("No updates here." )
        return
    else:
        print("Unable to retrieve information here.")
        return
    

if __name__ == "__main__":
    main()