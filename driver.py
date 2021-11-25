#!/usr/bin/python
# Author: Hoang Truong

try:
    # try importing pygame and pyqt5 to see if they are installed or not
    # if not, then install required libraries
    import pygame
    import PyQt5
except:
    from install_lib.install_lib import install_required_libraries
    install_required_libraries()

import sys
from os import path
from sorting_visualizer import SortingVisualizer
from pathfinding_visualizer import PathfindingVisualizer
from home_window import HomeWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

    




def _visualize(root_win: 'HomeWindow', option: int) -> None:
    '''
    run the chosen visualizer
    args:
        root_win: the main window
        option: the chosen type of visualizer
    '''
    root_win.hide()         # hide menu
    # run visualizer
    if option == 1:
        PathfindingVisualizer()
    elif option == 2:
        SortingVisualizer()

    root_win.show()         # show menu again when visualizer is closed





def main():
    app = QApplication(sys.argv)

    frame = HomeWindow()
    frame.show()
    frame.pushButton.clicked.connect(lambda:_visualize(frame, 1))
    frame.pushButton_2.clicked.connect(lambda:_visualize(frame, 2))

    icon_path = './images/algo_icon.ico'
    if path.exists(icon_path):
        frame.setWindowIcon(QtGui.QIcon(icon_path))

    app.exec_()


if __name__ == "__main__":
    main()




#>>>>>>>>>>>>> end of driver.py <<<<<<<<<<<<<