# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from collections import OrderedDict

from sqlalchemy.engine import Inspector
from config import USER, PASSWORD
from sqlalchemy import Column, Integer, String, MetaData, ForeignKey, Boolean, Text, Date, create_engine, \
    CheckConstraint
from sqlalchemy import func
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from tkinter import *
import tkinter.ttk as ttk

Base = declarative_base()

# data = db.session.query(func.your_schema.your_function_name()).all()

engine = create_engine('postgresql://{}:{}@localhost/mtg'.format(USER, PASSWORD),
                       echo=True)


class Card(Base):
    __tablename__ = 'Cards'
    __table_args__ = {'schema': 'public'}

    ManaValue = Column(Integer, CheckConstraint('ManaValue >= 0'), nullable=False)
    Set = Column(String, ForeignKey("sets.Name"), nullable=False)
    Name = Column(String, primary_key=True, nullable=False, autoincrement=True)
    Rarity = Column(String(8), nullable=False)
    Color = Column(String(9), nullable=False)
    isLegendary = Column(Boolean, nullable=False, default=False)
    Type = Column(String(12), nullable=False)

    def __init__(self, name, color, mana_value, type, set, rarity, is_legendary):
        self.Name = name
        self.Color = color
        self.ManaValue = mana_value
        self.Type = type
        self.Set = set
        self.Rarity = rarity
        self.IsLegendary = is_legendary

    def __repr__(self):
        return self.Name


class Set(Base):
    __tablename__ = 'Sets'
    __table_args__ = {'schema': 'public'}

    Name = Column(String, primary_key=True, nullable=False, autoincrement=True)
    Size = Column(Integer, CheckConstraint('Size > 0'), nullable=False)
    Block = Column(String, nullable=False)
    ReleaseDate = Column(Date, nullable=False)
    SetCode = Column(String(3), CheckConstraint('SetCode == upper(SetCode)'), nullable=False, unique=True)
    CountCards = Column(Integer, default=0)

    def __init__(self, name, set_code, release_date, size, block, count_cards):
        self.Name = name
        self.SetCode = set_code
        self.ReleaseDate = release_date
        self.Size = size
        self.Block = block
        self.CountCards = count_cards

    def __repr__(self):
        return self.Name


def App():
    class LogginFrame(Frame):

        def on_entry_click(self, event):
            """function that gets called whenever entry is clicked"""
            if self.password.get() == 'Enter your password...':
                self.password.delete(0, "end")  # delete all the text in the entry
                self.password.insert(0, '')  # Insert blank for user input
                self.password.config(fg='black')
                self.password.config(show='*')

        def on_focusout(self, event):
            if self.password.get() == '':
                self.password.insert(0, 'Enter your password...')
                self.password.config(fg='grey')
                self.password.config(show='')
            elif self.password.get() == 'Enter your password...':
                self.password.config(fg='grey')
                self.password.config(show='')

        def __init__(self, parent=None):
            super().__init__(parent)

            # Make login and password entry lines
            self.login = ttk.Combobox(self,
                                      values=('Lol', 'Alex', 'Bob', 'postgres'), width=70, justify='center')
            self.login.set('postgres')
            self.password = Entry(self, width=70, text='Enter your password')
            self.password.insert(0, 'Enter your password...')
            self.password.bind('<FocusIn>', self.on_entry_click)
            self.password.bind('<FocusOut>', self.on_focusout)
            self.submit = Button(self, bg="black", fg="blue",
                                 text="Login")

            # Pack all widgets
            self.login.pack()
            self.password.pack()
            self.submit.pack()

        def set_changer(self, view):
            self.submit.bind('<ButtonRelease-1>', LoginCardChanger(self, view))

    class Table:
        def __init__(self, parent, headings=tuple(), rows=tuple()):
            table = ttk.Treeview(parent, show="headings", selectmode="browse")
            table["columns"] = headings
            table["displaycolumns"] = headings

            for head in headings:
                table.heading(head, text=head, anchor=CENTER)
                table.column(head, anchor=CENTER)

            for row in rows:
                table.insert('', END, values=tuple(row))

            scrolltable = Scrollbar(parent, command=table.yview)
            table.configure(yscrollcommand=scrolltable.set)
            scrolltable.pack(side=RIGHT, fill=Y)
            table.pack(expand=YES, fill=BOTH)
            table.bind("<<TreeviewSelect>>", self.print_selection)
            self.table = table
            self.parent = parent

        def pack(self, *args, **kwargs):
            self.table.pack(*args, **kwargs)

        def print_selection(self, event):
            for selection in self.table.selection():
                item = self.table.item(selection)
                print(item["values"])

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
            b2 = Button(right_frame, bg="red", fg="blue",
                        text="right Bottom button")
            self.b4 = Button(right_frame, bg="red", fg="blue",
                             text="Sets")
            b1.pack()
            b2.pack()
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

            session.close()

            b1 = Button(right_frame, bg="red", fg="blue",
                        text="tt")
            b2 = Button(right_frame, bg="red", fg="blue",
                        text="right Bottom button")
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

    def LoginCardChanger(forget, show):
        def changer(event):
            if forget.login.get() == USER and forget.password.get() == PASSWORD:
                print(forget.password.get())
                forget.pack_forget()
                show.pack()
            else:
                if forget.login.get() != USER:
                    print("Wrong login!")
                elif forget.password.get() != PASSWORD:
                    print("Wrong password!")

        return changer

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

    root = Tk()
    root.title("Our database")

    loggin_f = LogginFrame(root)
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
    App()
