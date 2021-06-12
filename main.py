# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from loginFrame import LoginFrame
from dataFrames import *
from insertFrame import *
from DBFrame import *
from tkinter import *
from TablesFrame import *


def app():
    root = Tk()
    root.title("Authorization")
    # tl = Menu(root)
    # tl.add_command(label="One")
    # tl.add_command(label="Two")
    # root.config(menu=tl)

    login_f = LoginFrame(root)
    login_f.widgetName = 'LoginFrame'
    login_f.pack()

    db_f = DBFrame(root)
    db_f.widgetName = 'DBFrame'
    tbl_f = TablesFrame(root)
    tbl_f.widgetName = 'tablesFrame'
    view_f = ViewFrame(root)
    view_f.widgetName = 'CardFrame'
    set_f = SetFrame(root)
    set_f.widgetName = 'SetFrame'
    insert_f = InsertFrame(root)
    insert_f.widgetName = 'InsertFrame'

    db_f.table.table.bind("<<TreeviewSelect>>", db_f.table.generation(tbl_f))
    tbl_f.table.table.bind("<<TreeviewSelect>>", tbl_f.table.next_generation(view_f))

    db_f.insert_changer(insert_f)

    login_f.set_changer(db_f)
    #insert_f.cancelInsert(view_f)
    #insert_f.commitRow(view_f)

    set_f.set_changer(login_f)
    set_f.set_new_changer(view_f)
    set_f.set_insert_changer(insert_f)

    view_f.set_changer(login_f)
    view_f.set_new_changer(set_f)
    view_f.set_insert_changer(insert_f)

    root.mainloop()


if __name__ == '__main__':
    app()
