from collections import OrderedDict
from tkinter import *

from sqlalchemy import inspect, func
from sqlalchemy.orm import sessionmaker

from dataClasses import *
from dataFrames import engine
from table import Table


def insertFrameChanger(forget, show):
    def changer(event):
        for old_widget in forget.entry_sheet.pack_slaves():
            old_widget.pack_forget()
        forget.entry_sheet.pack_forget()
        forget.pack_forget()
        show.pack()

    return changer


def commitFrameChanger(forget, show, state):
    def changer(event):
        if state == 1:
            # newCard = Card(forget.entryName.get(),
            #                forget.entryColor.get(),
            #                forget.entryManaValue.get(),
            #                forget.entryType.get(),
            #                forget.entrySet.get(),
            #                forget.entryRarity.get(),
            #                forget.IsLegendary.get())
            newCard = Card(*[data.get() for data in forget.pack_slaves()])

            Session = sessionmaker(bind=engine)  # bound session
            session = Session()
            try:
                session.add(newCard)
                session.commit()
                rows_data = [q.__dict__ for q in session.query(Card).all()]
                for card in rows_data:
                    card.pop('_sa_instance_state')
                show.table.free()
                sorted_data = [list(OrderedDict((k, d[k]) for k in show.table.headings).values()) for d in rows_data]
                show.table.fill(sorted_data)
                show.update()
                forget.pack_forget()
                show.pack()
            finally:
                session.close()
        elif state == 0:
            Session = sessionmaker(bind=engine)  # bound session
            session = Session()
            session.query(func.public.create_database()).all()
            # rows_data = [q.__dict__ for q in session.query(Card).all()]
            # for card in rows_data:
            #     card.pop('_sa_instance_state')
            # show.table.free()
            # sorted_data = [list(OrderedDict((k, d[k]) for k in show.table.headings).values()) for d in rows_data]
            # show.table.fill(sorted_data)
            # show.update()
            forget.pack_forget()
            show.pack()

    return changer


class InsertFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_f = Frame(self)
        right_frame = Frame(self.top_f)
        self.bottom_frame = Frame(self)

        self.commitButton = Button(self.bottom_frame, bg="red", fg="blue", text="commit")
        self.cancelButton = Button(self.bottom_frame, bg="red", fg="blue", text="cancel")

        self.commitButton.pack(side=LEFT)
        self.cancelButton.pack(side=LEFT)

        right_frame.pack(expand=YES, fill=BOTH, side=TOP)

        self.top_f.pack()
        self.bottom_frame.pack(side=BOTTOM)

    # def commitRow(self, view):
    #     self.commitButton.bind('<ButtonRelease-1>', commitFrameChanger(self, view))
    #
    # def cancelInsert(self, view):
    #     self.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(self, view))
