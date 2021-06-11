from tkinter import *
from collections import OrderedDict
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from dataClasses import *
from table import Table
from config import USER, PASSWORD

engine = create_engine('postgresql://{}:{}@localhost/mtg'.format(USER, PASSWORD),
                       echo=True)


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

        Session = sessionmaker(bind=engine)  # bound session
        session = Session()

        rows_data = [q.__dict__ for q in session.query(Card).all()]
        for card in rows_data:
            card.pop('_sa_instance_state')

        headings = [name['name'] for name in inspector.get_columns("Cards", "public")]

        sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in rows_data]

        table = Table(table_frame, headings=headings, rows=sorted_data)

        table.pack(expand=YES, fill=BOTH)

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
        self.b2.bind('<ButtonRelease-1>', CardSetChanger(self, view))


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

        table = Table(table_frame, headings=headings, rows=sorted_data)
        table.pack(expand=YES, fill=BOTH)

        data = session.query(func.public.print_cards()).all()

        b1 = Button(right_frame, bg="red", fg="blue",
                    text="tt")
        b2 = Button(right_frame, bg="red", fg="blue",
                    text="add new set")
        b1.pack()
        b2.pack()
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
