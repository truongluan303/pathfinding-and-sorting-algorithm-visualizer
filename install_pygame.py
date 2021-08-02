#!/usr/bin/python

##################################################################
###  a script to automatically upgrade pip and install pygame  ###
##################################################################

import sys
import os
import subprocess

def install(package):
    # upgrade pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    # install package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == "__main__":
    install('pygame')
    clear_screen()
    print("---FINISHED---")
    _ = input("Press Enter to continue...")
    sys.exit(0)
