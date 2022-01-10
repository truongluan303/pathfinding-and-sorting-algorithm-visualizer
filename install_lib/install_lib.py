# Author: Hoang Truong

##################################################################
###  a script to automatically upgrade pip and install pygame  ###
##################################################################

import sys
import os
import subprocess


def __install(package: str):
    # install package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])




def __clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')




def install_required_libraries():

    print(">>> Installing Dependencies...\n\n")
    
    try:
        # install pygame
        __install('pygame')
    except:
        if sys.platform == 'win32' or sys.platform == 'darwin':
            os.system(sys.executable + " " + os.getcwd() + "/install_lib/get_pip.py")
        else:
            os.system('sudo apt-get update')
            os.system('sudo apt-get install python3-pip')
        __install('pygame')

    # clear screen and inform that the process is finished
    __clear_screen()
    print("--- FINISHED INSTALLATIONS ---")
