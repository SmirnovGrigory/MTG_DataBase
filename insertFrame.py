from collections import OrderedDict
from tkinter import *

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from dataClasses import *
from dataFrames import engine
from table import Table


def insertFrameChanger(forget, show):
    def changer(event):
        forget.pack_forget()
        show.pack()

    return changer


def commitFrameChanger(forget, show):
    def changer(event):
        newCard = Card(forget.entryName.get(),
                       forget.entryColor.get(),
                       forget.entryManaValue.get(),
                       forget.entryType.get(),
                       forget.entrySet.get(),
                       forget.entryRarity.get(),
                       forget.isLegendary.get())

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
        finally:
            session.close()
        forget.pack_forget()
        show.pack()

    return changer


class InsertFrame(Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.top_f = Frame(self)
        table_frame = Frame(self.top_f)
        right_frame = Frame(self.top_f)
        self.bottom_frame = Frame(self)
        one_frame = Frame(self)
        sec_frame = Frame(self)
        thr_frame = Frame(self)
        four_frame = Frame(self)
        fif_frame = Frame(self)
        six_frame = Frame(self)

        self.entryName = Entry(one_frame, width=50, text='Name')
        self.nameLabel = Label(one_frame, text='Name')
        self.entryColor = Entry(sec_frame, width=50, text='Color')
        self.colorLabel = Label(sec_frame, text='Color')
        self.entryManaValue = Entry(thr_frame, width=46, text='ManaValue')
        self.manaLabel = Label(thr_frame, text='Mana value')
        self.entryType = Entry(four_frame, width=50, text='Type')
        self.typeLabel = Label(four_frame, text='Type')
        self.entrySet = Entry(fif_frame, width=52, text='Set')
        self.setLabel = Label(fif_frame, text='Set')
        self.entryRarity = Entry(six_frame, width=50, text='Rarity')
        self.rarityLabel = Label(six_frame, text='Rarity')
        self.isLegendary = BooleanVar()
        self.isLegendaryRadio = Checkbutton(self, text='isLegendary', variable=self.isLegendary)  #######

        self.entryName.pack(side=RIGHT)
        self.nameLabel.pack(side=LEFT)
        self.entryColor.pack(side=RIGHT)
        self.colorLabel.pack(side=LEFT)
        self.entryManaValue.pack(side=RIGHT)
        self.manaLabel.pack(side=LEFT)
        self.entryType.pack(side=RIGHT)
        self.typeLabel.pack(side=LEFT)
        self.entrySet.pack(side=RIGHT)
        self.setLabel.pack(side=LEFT)
        self.entryRarity.pack(side=RIGHT)
        self.rarityLabel.pack(side=LEFT)

        self.commitButton = Button(right_frame, bg="red", fg="blue", text="commit")
        self.cancelButton = Button(right_frame, bg="red", fg="blue", text="cancel")

        # self.commitButton.config(command=self.commitRow)
        # self.cancelButton.config(command=self.cancelInsert)

        self.commitButton.pack(side=LEFT)
        self.cancelButton.pack(side=LEFT)

        one_frame.pack(side=TOP)
        sec_frame.pack(side=TOP)
        thr_frame.pack(side=TOP)
        four_frame.pack(side=TOP)
        fif_frame.pack(side=TOP)
        six_frame.pack(side=TOP)
        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=TOP)
        self.isLegendaryRadio.pack()

        self.top_f.pack()
        self.bottom_frame.pack()

    def commitRow(self, view):
        self.commitButton.bind('<ButtonRelease-1>', commitFrameChanger(self, view))

    def cancelInsert(self, view):
        self.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(self, view))
