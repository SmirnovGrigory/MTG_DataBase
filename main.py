# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from loginFrame import LoginFrame
from dataFrames import *
from tkinter import *


def app():

    root = Tk()
    root.title("Our database")

    loggin_f = LoginFrame(root)
    loggin_f.pack()

    view_f = ViewFrame(root)
    set_f = SetFrame(root)

    loggin_f.set_changer(view_f)

    set_f.set_changer(loggin_f)
    set_f.set_new_changer(view_f)

    view_f.set_changer(loggin_f)
    view_f.set_new_changer(set_f)

    root.mainloop()


if __name__ == '__main__':
    app()
