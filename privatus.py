from http import client
import shutil, ctypes, io
import subprocess, os, sys, zipfile, requests, yaml
from elevate import elevate
from PyQt5 import QtWidgets, QtGui

# Importing scripts
from src import init
from src import commons

realpath = os.path.realpath(__file__)
dir_path = os.path.dirname(realpath)

# Variables
init_functions = [
    init.init
]

# Functions
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

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
            
def updateApplication(app_path):
    
    # Check if app_path contains necessary files
    files = os.listdir(app_path)
    
    if files == None or files == [] or not files.__contains__("privatus"):
        return "Install the application"
    else:
        app_path = app_path + "/privatus"
    
    # Checking for updates
    try:
        with open(app_path + "/version.yaml", 'r') as stream:
            data = yaml.safe_load(stream)
    except Exception as e:
        print(e)
        input("error")
    
    l_version_f = getVerFromTag(data['version']) 
    
    try:
        releases = requests.get("https://api.github.com/repos/RespectedCow/Project-Oasis/releases")
        
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
                icon.addPixmap(QtGui.QPixmap(dir_path + "/cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
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
                link = latest_update[1]["assets"][0]["browser_download_url"]
                save_to = commons.move_back(app_path) + "/" + latest_update[1]["assets"][0]["name"]
                
                print("Downloading newest version")
                response = requests.get(link, allow_redirects=True)
                print("Newest version downloaded")

                with open(save_to, "wb") as f:
                    f.write(response.content)
                        
                if os.path.exists(app_path):
                    os.rename(app_path, commons.move_back(app_path) + "/old-version")
            
                if os.path.exists(save_to):
                    with zipfile.ZipFile(save_to, "r") as f:
                        f.extractall(commons.move_back(app_path))
                        shutil.rmtree(commons.move_back(app_path) + "/old-version")
                        
                        f.close()
                        
                print("Exiting")
                return
            else:
                return "No version"
        else:
            print("Unable to retrieve information here.")
            return       
    except requests.ConnectionError as e:
        e = str(e)
        
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(dir_path + "cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(f"There was an error connecting to the github api! (Error: {e})")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        msg.exec_()
        
        return
    except Exception as e:
        print(e)
        input("error2")
    
def installApplication(app_path, overwrite=False):
    try:
        releases = requests.get("https://api.github.com/repos/RespectedCow/Project-Oasis/releases")
    except requests.ConnectionError as e:
        e = str(e)
        
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(dir_path + "cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(f"There was an error connecting to the github api! (Error: {e})")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        
        msg.exec_()
        
        return

    if releases.status_code == 200:  
        releases = releases.json()
        installs = []
        for release in releases:
            branch = release["target_commitish"]
            r_version = release["tag_name"]
                
            if branch == "main":
                installs.append((r_version, release))
                        
        latest_version = getLastestVersion(installs)
        latest_install = getUpdateWithVersion(latest_version, installs)
            
        # Check if user wants to update
        if latest_install != None: 
            msg = QtWidgets.QMessageBox()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(dir_path + "/cowicon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(f"Do you wish to install privatus? (version: {latest_version})")
            msg.setWindowTitle("Hey there!") 
            yesButton = msg.addButton('Yes', QtWidgets.QMessageBox.YesRole)
            noButton = msg.addButton('No', QtWidgets.QMessageBox.NoRole)

            msg.exec_()
                            
            if msg.clickedButton() == yesButton:
                # Install the application
                pass
            elif msg.clickedButton() == noButton:
                sys.exit()
                
            # Here is the actual updating occurs
            link = latest_install[1]["assets"][0]["browser_download_url"]
            save_to = commons.flip_slashes(app_path) + "/" + latest_install[1]["assets"][0]["name"]
                
            if os.path.exists(save_to) == False:
                print("Downloading newest version")
                response = requests.get(link, allow_redirects=True)
                print("Newest version downloaded")

                with open(save_to, "wb") as f:
                    f.write(response.content)
            
                if os.path.exists(save_to):
                    with zipfile.ZipFile(save_to, "r") as f:
                        f.extractall(app_path)
                        
                # Configure config.yaml
                if overwrite:
                    with io.open(commons.get_appdatafolder() + '/config.yaml', 'w') as f:
                        default_config_data = init.write_to_file('/config.yaml', dir_path + "/overwrite")
                        print(default_config_data, type(default_config_data))
                        
                        default_config_data["client"]["client_path"] = app_path + "/privatus"
                        
                        yaml.dump(default_config_data, f)
                        
                print("Exiting")
                return
            else:
                return "No version"
    else:
        print("Unable to retrieve information here.")
        return 
        
        
if __name__ == "__main__":
    
    for fnc in init_functions:
        fnc = fnc()
        
        if fnc.check_init():
            fnc.run(dir_path) # Will return any potential errors
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
    
    # Do stuff
    with open(commons.get_appdatafolder() + '\config.yaml', 'r') as f:
        config_data = yaml.safe_load(f)

        client_path = config_data["client"]["client_path"]
    
    if is_admin():
        
        if client_path != "":
            re_msg = updateApplication(client_path)
            
            if re_msg == None:
                print("Update complete!")
                print("Running privatus now")
                try:
                    subprocess.call([client_path + "/privatus/privatus"], shell=True)
                except Exception as e:
                    print(e)
                    print(client_path + "/privatus")
                    input("error")
                sys.exit()
            elif re_msg == "No version":
                subprocess.call([client_path + "/privatus/privatus"], shell=True)
            elif re_msg == "Install the application":
                installApplication(client_path)
                    
                if os.path.exists(client_path):
                    try:
                        subprocess.call([client_path + "/privatus/privatus"], shell=True)
                    except Exception as e:
                        print(e)
                        input("error")
                    sys.exit()
        else:
            app_path = commons.get_program_path()
            installApplication(app_path, True)
                
            if os.path.exists(app_path):
                subprocess.call([app_path + "/privatus/privatus"], shell=True)
                sys.exit()
    else:
        # Re-run the program with admin rights
        elevate(True, True)