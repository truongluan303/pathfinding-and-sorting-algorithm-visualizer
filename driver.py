#!/usr/bin/python
# Author: Hoang Truong

try:
    # try importing pygame to see if it is installed or not
    # if not, then install the required library
    import pygame
except:
    from install_lib.install_lib import install_required_libraries
    install_required_libraries()

from home_window import HomeWindow



if __name__ == "__main__":
    while True:
        HomeWindow()




#>>>>>>>>>>>>> end of driver.py <<<<<<<<<<<<<