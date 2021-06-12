from tkinter import *
from collections import OrderedDict

from sqlalchemy.engine import Inspector
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, Table as SQLTable
from dataClasses import *
from insertFrame import commitFrameChanger, insertFrameChanger
from table import Table


def CardLoginChanger(forget, show):
    def changer(event):
        show.password.delete(0, 'end')
        show.on_focusout('<FocusOut>')
        show.login.focus_set()
        forget.pack_forget()
        show.pack()

    return changer


def CardSetChanger(forget, show):
    def changer(event):
        forget.pack_forget()
        show.pack()

    return changer

def CardInsertChanger(forget, show):
    def changer(event):
        show.entry_sheet = Frame(show)
        one_frame = Frame(show.entry_sheet)
        sec_frame = Frame(show.entry_sheet)
        thr_frame = Frame(show.entry_sheet)
        four_frame = Frame(show.entry_sheet)
        fif_frame = Frame(show.entry_sheet)
        six_frame = Frame(show.entry_sheet)

        show.entryName = Entry(one_frame, width=50, text='Name')
        nameLabel = Label(one_frame, text='Name')
        show.entryColor = Entry(sec_frame, width=50, text='Color')
        colorLabel = Label(sec_frame, text='Color')
        show.entryManaValue = Entry(thr_frame, width=46, text='ManaValue')
        manaLabel = Label(thr_frame, text='Mana value')
        show.entryType = Entry(four_frame, width=50, text='Type')
        typeLabel = Label(four_frame, text='Type')
        show.entrySet = Entry(fif_frame, width=52, text='Set')
        setLabel = Label(fif_frame, text='Set')
        show.entryRarity = Entry(six_frame, width=50, text='Rarity')
        rarityLabel = Label(six_frame, text='Rarity')
        show.IsLegendary = BooleanVar()
        isLegendaryRadio = Checkbutton(show.entry_sheet, text='isLegendary', variable=show.IsLegendary)

        show.entryName.pack(side=RIGHT)
        nameLabel.pack(side=LEFT)
        show.entryColor.pack(side=RIGHT)
        colorLabel.pack(side=LEFT)
        show.entryManaValue.pack(side=RIGHT)
        manaLabel.pack(side=LEFT)
        show.entryType.pack(side=RIGHT)
        typeLabel.pack(side=LEFT)
        show.entrySet.pack(side=RIGHT)
        setLabel.pack(side=LEFT)
        show.entryRarity.pack(side=RIGHT)
        rarityLabel.pack(side=LEFT)

        one_frame.pack(side=TOP)
        sec_frame.pack(side=TOP)
        thr_frame.pack(side=TOP)
        four_frame.pack(side=TOP)
        fif_frame.pack(side=TOP)
        six_frame.pack(side=TOP)
        isLegendaryRadio.pack()

        show.entry_sheet.pack(side=TOP)
        forget.pack_forget()
        show.commitButton.bind('<ButtonRelease-1>', commitFrameChanger(show, forget, 1))
        show.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(show, forget))
        show.pack()

    return changer

def SetInsertChanger(forget, show):
    def changer(event):
        show.entry_sheet = Frame(show)
        one_frame = Frame(show.entry_sheet)
        sec_frame = Frame(show.entry_sheet)
        thr_frame = Frame(show.entry_sheet)
        four_frame = Frame(show.entry_sheet)
        fif_frame = Frame(show.entry_sheet)
        six_frame = Frame(show.entry_sheet)

        show.entryName = Entry(one_frame, width=50, text='Name')
        nameLabel = Label(one_frame, text='Name')
        show.entrySet = Entry(sec_frame, width=50, text='Color')
        SetLabel = Label(sec_frame, text='Set code')
        show.entryDate = Entry(thr_frame, width=46, text='ManaValue')
        DateLabel = Label(thr_frame, text='Release date')
        show.entrySize = Entry(four_frame, width=50, text='Type')
        SizeLabel = Label(four_frame, text='Size')
        show.entryBlock = Entry(fif_frame, width=52, text='Set')
        BlockLabel = Label(fif_frame, text='Block')
        show.entryCount = Entry(six_frame, width=50, text='Rarity')
        CountLabel = Label(six_frame, text='Count cards')

        show.entryName.pack(side=RIGHT)
        nameLabel.pack(side=LEFT)
        show.entrySet.pack(side=RIGHT)
        SetLabel.pack(side=LEFT)
        show.entryDate.pack(side=RIGHT)
        DateLabel.pack(side=LEFT)
        show.entrySize.pack(side=RIGHT)
        SizeLabel.pack(side=LEFT)
        show.entryBlock.pack(side=RIGHT)
        BlockLabel.pack(side=LEFT)
        show.entryCount.pack(side=RIGHT)
        CountLabel.pack(side=LEFT)

        one_frame.pack(side=TOP)
        sec_frame.pack(side=TOP)
        thr_frame.pack(side=TOP)
        four_frame.pack(side=TOP)
        fif_frame.pack(side=TOP)
        six_frame.pack(side=TOP)

        show.entry_sheet.pack(side=TOP)
        show.commitButton.bind('<ButtonRelease-1>', commitFrameChanger(show, forget, 1))
        show.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(show, forget))
        forget.pack_forget()
        show.pack()

    return changer


def clearCards(session):
    def changer(event):
        session.query(func.public.clearcards()).first()
        session.commit()

    return changer


def clearSets(session):
    def changer(event):
        session.query(func.public.clearsets()).first()
        session.commit()

    return changer

def createDB(session):
    def changer(event):
        pass

    return changer


def deleteDB(session):
    def changer(event):
        pass

    return changer


def showOneCardFrame(session, name):
    def changer(event):
        lstCardFields = session.query(func.public.get_card(name)).all()

    return changer


class ViewFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_f = Frame(self)
        table_frame = Frame(self.top_f)
        right_frame = Frame(self.top_f)
        self.bottom_frame = Frame(self)

        inspector = inspect(engine)
        meta = MetaData(engine)
        user_table = SQLTable('Cards', meta)
        inspector.reflect_table(user_table, None)

        Session = sessionmaker(bind=engine)  # bound session
        session = Session()

        z = session.query(user_table).all()

        rows_data = [q.__dict__ for q in session.query(Card).all()]
        for card in rows_data:
            card.pop('_sa_instance_state')

        headings = [name['name'] for name in inspector.get_columns("Cards", "public")]

        sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in rows_data]

        self.table = Table(table_frame, headings=headings, rows=sorted_data)

        self.table.pack(expand=YES, fill=BOTH)

        self.b2 = Button(right_frame, bg="red", fg="blue", text="add new card")
        self.b4 = Button(right_frame, bg="red", fg="blue", text="Sets")
        self.clearCardsButton = Button(right_frame, bg="red", fg="blue", text="clear cards")
        self.clearCardsButton.bind('<ButtonRelease-1>', clearCards(session))
        self.clearAllTablesButton = Button(right_frame, bg="red", fg="blue", text="clear all")

        self.entryName = Entry(self, width=50, text='card name')
        self.findCardButton = Button(right_frame, bg="red", fg="blue", text="find card")
        self.findCardButton.bind('<ButtonRelease-1>', showOneCardFrame(session, self.entryName.get()))
        self.createDBButton = Button(right_frame, bg="red", fg="blue", text="add new DB")
        self.createDBButton.bind('<ButtonRelease-1>', createDB(session))

        self.deleteDBButton = Button(right_frame, bg="red", fg="blue", text="delete DB")
        self.deleteDBButton.bind('<ButtonRelease-1>', deleteDB(session))

        self.b2.pack()
        self.b4.pack()
        self.clearCardsButton.pack()
        self.clearAllTablesButton.pack()
        self.entryName.pack()
        self.findCardButton.pack()
        self.createDBButton.pack()
        self.deleteDBButton.pack()

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)

        self.b3 = Button(self.bottom_frame, bg="red", fg="blue", text="Exit")
        self.b3.pack(side=LEFT)
        self.top_f.pack()
        self.bottom_frame.pack()

    def set_changer(self, view):
        self.b3.bind('<ButtonRelease-1>', CardLoginChanger(self, view))

    def set_new_changer(self, view):
        self.b4.bind('<ButtonRelease-1>', CardSetChanger(self, view))

    def set_insert_changer(self, view):
        self.b2.bind('<ButtonRelease-1>', CardInsertChanger(self, view))


class SetFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_f = Frame(self)
        table_frame = Frame(self.top_f)
        right_frame = Frame(self.top_f)
        self.bottom_frame = Frame(self)

        inspector = inspect(engine)

        Session = sessionmaker(bind=engine)  # bound session
        session = Session()

        sets_data = [q.__dict__ for q in session.query(Set).all()]
        for set in sets_data:
            set.pop('_sa_instance_state')

        headings = [name['name'] for name in inspector.get_columns("Sets", "public")]

        sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in sets_data]

        self.table = Table(table_frame, headings=headings, rows=sorted_data)
        self.table.pack(expand=YES, fill=BOTH)

        data = session.query(func.public.print_cards()).all()

        b1 = Button(right_frame, bg="red", fg="blue",
                    text="tt")
        self.b2 = Button(right_frame, bg="red", fg="blue",
                    text="add new set")
        b1.pack()
        self.b2.pack()
        self.b4 = Button(right_frame, bg="red", fg="blue",
                         text="Cards")
        self.b4.pack(side=LEFT)
        self.clearSetsButton = Button(right_frame, bg="red", fg="blue", text="clear sets")
        self.clearSetsButton.bind('<ButtonRelease-1>', clearSets(session))

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)

        self.clearSetsButton.pack()
        self.b3 = Button(self.bottom_frame, bg="red", fg="blue", text="Exit")
        self.b3.pack(side=LEFT)
        self.top_f.pack()
        self.bottom_frame.pack()

    def set_changer(self, view):
        self.b3.bind('<ButtonRelease-1>', CardLoginChanger(self, view))

    def set_new_changer(self, view):
        self.b4.bind('<ButtonRelease-1>', CardSetChanger(self, view))

    def set_insert_changer(self, view):
        self.b2.bind('<ButtonRelease-1>', SetInsertChanger(self, view))
