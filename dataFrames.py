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

        # for q in session.query(Card).all():
        #     z = list(q.__dict__.values())[1:]
        #     print(z)

        rows_data = [q.__dict__ for q in session.query(Card).all()]
        for card in rows_data:
            card.pop('_sa_instance_state')

        headings = [name['name'] for name in inspector.get_columns("Cards", "public")]

        sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in rows_data]

        table = Table(table_frame, headings=headings, rows=sorted_data)

        table.pack(expand=YES, fill=BOTH)

        session.close()

        b1 = Button(right_frame, bg="red", fg="blue",
                    text="Change State!!!")
        self.b2 = Button(right_frame, bg="red", fg="blue",
                    text="add new card")
        self.b4 = Button(right_frame, bg="red", fg="blue",
                         text="Sets")
        b1.pack()
        self.b2.pack()
        self.b4.pack()

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)

        self.b3 = Button(self.bottom_frame, bg="red", fg="blue",
                         text="Exit")
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

        # for q in session.query(Card).all():
        #     z = list(q.__dict__.values())[1:]
        #     print(z)

        sets_data = [q.__dict__ for q in session.query(Set).all()]
        for set in sets_data:
            set.pop('_sa_instance_state')

        headings = [name['name'] for name in inspector.get_columns("Sets", "public")]

        sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in sets_data]

        table = Table(table_frame, headings=headings, rows=sorted_data)
        table.pack(expand=YES, fill=BOTH)

        data = session.query(func.public.print_cards()).all()
        # session.query(
        #   func.public.insert_row_in_cards('Skyblade of the Legion', 'White', 2, 'Creature', 'Ixalan', 'Common',
        #                                  False)).all()

        session.close()

        b1 = Button(right_frame, bg="red", fg="blue",
                    text="tt")
        b2 = Button(right_frame, bg="red", fg="blue",
                    text="add new set")
        b1.pack()
        b2.pack()
        self.b4 = Button(right_frame, bg="red", fg="blue",
                         text="Cards")
        self.b4.pack(side=LEFT)

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)

        self.b3 = Button(self.bottom_frame, bg="red", fg="blue",
                         text="Exit")
        self.b3.pack(side=LEFT)
        self.top_f.pack()
        self.bottom_frame.pack()

    def set_changer(self, view):
        self.b3.bind('<ButtonRelease-1>', CardLoginChanger(self, view))

    def set_new_changer(self, view):
        self.b4.bind('<ButtonRelease-1>', CardSetChanger(self, view))
