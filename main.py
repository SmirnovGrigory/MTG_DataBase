# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from loginFrame import LoginFrame
from dataFrames import *
from insertFrame import *
from tkinter import *


def app():
    root = Tk()
    root.title("MTG database")

    login_f = LoginFrame(root)
    login_f.pack()

    view_f = ViewFrame(root)
    set_f = SetFrame(root)
    insert_f = InsertFrame(root)
    login_f.set_changer(view_f)
    insert_f.cancelInsert(view_f)

    set_f.set_changer(login_f)
    set_f.set_new_changer(view_f)

    view_f.set_changer(login_f)
    view_f.set_new_changer(set_f)
    view_f.set_insert_changer(insert_f)

    root.mainloop()


if __name__ == '__main__':
    app()
