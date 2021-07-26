import sys
from sorting_visualizer import SortingVisualizer
from pathfinding_visualizer import PathfindingVisualizer
from tkinter import Tk, Label, Button, messagebox


def _on_closing():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        sys.exit(0)

def _choose_pathfinding(root):
    root.wm_withdraw()          # hide menu
    PathfindingVisualizer()     # run visualizer
    root.deiconify()            # show menu again when visualizer is closed

def _choose_sorting(root):
    root.wm_withdraw()          # hide menu
    SortingVisualizer()         # run visualizer
    root.deiconify()            # show menu again when visualizer is closed


###########################
########### MAIN ##########
#-------------------------#
if __name__ == "__main__":
    # create the menu GUI
    root = Tk()
    root.geometry('600x370')
    root.title('Pathfinding and Sorting Algorithms Visualizer')
    root.protocol("WM_DELETE_WINDOW", _on_closing)

    text = Label(root, text='Please choose the type of visualizer:',
                 font='Courier 15 bold', pady='30')
    text.pack()

    pathfinding = Button(root, text='Path Finding Algorithms',
                         command=lambda:_choose_pathfinding(root))
    pathfinding.config(height=3, width=30, font='Courier 13 bold', fg='white', bg='brown')
    pathfinding.pack()

    Label(root, height=1).pack()

    sorting = Button(root, text='Sorting Algorithms',
                         command=lambda:_choose_sorting(root))
    sorting.config(height=3, width=30, font='Courier 13 bold', fg='white', bg='brown')
    sorting.pack()

    Label(root, height=1).pack()

    exit_button = Button(root, text='Exit', command=lambda:sys.exit(0))
    exit_button.config(height=2, width=10, font='Courier 13 bold', fg='white', bg='brown')
    exit_button.pack()

    root.mainloop()