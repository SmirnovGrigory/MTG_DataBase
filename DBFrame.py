from tkinter import *
from collections import OrderedDict

from sqlalchemy.engine import Inspector
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from dataClasses import *
from insertFrame import commitFrameChanger, insertFrameChanger
from table import Table

def createDB(session):
    def changer(event):
        window = Tk()
        main_f = Frame(window)


    return changer


def deleteDB(session):
    def changer(event):
        pass

    return changer

def DBInsertChanger(forget, show):
    def changer(event):
        show.entry_sheet = Frame(show)
        one_frame = Frame(show.entry_sheet)
        # sec_frame = Frame(show.entry_sheet)
        # thr_frame = Frame(show.entry_sheet)
        # four_frame = Frame(show.entry_sheet)
        # fif_frame = Frame(show.entry_sheet)
        # six_frame = Frame(show.entry_sheet)

        show.entryName = Entry(one_frame, width=50, text='Name')
        nameLabel = Label(one_frame, text='Database name')
        # show.entrySet = Entry(sec_frame, width=50, text='Color')
        # SetLabel = Label(sec_frame, text='Set code')
        # show.entryDate = Entry(thr_frame, width=46, text='ManaValue')
        # DateLabel = Label(thr_frame, text='Release date')
        # show.entrySize = Entry(four_frame, width=50, text='Type')
        # SizeLabel = Label(four_frame, text='Size')
        # show.entryBlock = Entry(fif_frame, width=52, text='Set')
        # BlockLabel = Label(fif_frame, text='Block')
        # show.entryCount = Entry(six_frame, width=50, text='Rarity')
        # CountLabel = Label(six_frame, text='Count cards')

        show.entryName.pack(side=RIGHT)
        nameLabel.pack(side=LEFT)
        # show.entrySet.pack(side=RIGHT)
        # SetLabel.pack(side=LEFT)
        # show.entryDate.pack(side=RIGHT)
        # DateLabel.pack(side=LEFT)
        # show.entrySize.pack(side=RIGHT)
        # SizeLabel.pack(side=LEFT)
        # show.entryBlock.pack(side=RIGHT)
        # BlockLabel.pack(side=LEFT)
        # show.entryCount.pack(side=RIGHT)
        # CountLabel.pack(side=LEFT)

        one_frame.pack(side=TOP)
        # sec_frame.pack(side=TOP)
        # thr_frame.pack(side=TOP)
        # four_frame.pack(side=TOP)
        # fif_frame.pack(side=TOP)
        # six_frame.pack(side=TOP)

        show.entry_sheet.pack(side=TOP)
        show.commitButton.bind('<ButtonRelease-1>', commitFrameChanger(show, forget, 0))
        show.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(show, forget))
        forget.pack_forget()
        show.pack()

    return changer

class DBFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_f = Frame(self)
        table_frame = Frame(self.top_f)
        right_frame = Frame(self.top_f)
        self.bottom_frame = Frame(self)

        inspector = inspect(engine)

        Session = sessionmaker(bind=engine)  # bound session
        session = Session()

        x = session.query(func.public.all_databases()).all()
        rows_data = [name[0] for name in session.query(func.public.all_databases()).all()]

        self.table = Table(table_frame, headings=['DB name'], rows=rows_data)

        self.table.pack(expand=YES, fill=BOTH)

        self.createDBButton = Button(right_frame, bg="red", fg="blue", text="add new DB")
        self.deleteDBButton = Button(right_frame, bg="red", fg="blue", text="delete DB")
        self.deleteDBButton.bind('<ButtonRelease-1>', deleteDB(session))

        self.createDBButton.pack()
        self.deleteDBButton.pack()

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)

        self.b3 = Button(self.bottom_frame, bg="red", fg="blue", text="Exit")
        self.b3.pack(side=LEFT)
        self.top_f.pack()
        self.bottom_frame.pack()


        #self.bind('<ButtonRelease-1>', DBInsertChanger(self, view))
        #self.pack()

    def insert_changer(self, view):
        self.createDBButton.bind('<ButtonRelease-1>', DBInsertChanger(self, view))

    # def set_changer(self, view):
    #     self.b3.bind('<ButtonRelease-1>', CardLoginChanger(self, view))
    #
    # def set_new_changer(self, view):
    #     self.b4.bind('<ButtonRelease-1>', CardSetChanger(self, view))
    #
    # def set_insert_changer(self, view):
    #     self.b2.bind('<ButtonRelease-1>', CardInsertChanger(self, view))
