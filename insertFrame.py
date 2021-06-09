from tkinter import *
from dataClasses import *
from dataFrames import engine



def insertFrameChanger(forget, show):
    def changer(event):
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

        self.entryName = Entry(self, width=50, text='Name')
        self.entryColor = Entry(self, width=50, text='Color')
        self.entryManaValue = Entry(self, width=50, text='ManaValue')
        self.entryType = Entry(self, width=50, text='Type')
        self.entrySet = Entry(self, width=50, text='Set')
        self.entryRarity = Entry(self, width=50, text='Rarity')
        self.isLegendaryRadio = Radiobutton(text='isLegendary', value=False)  #######

        self.entryName.pack()
        self.entryColor.pack()
        self.entryManaValue.pack()
        self.entryType.pack()
        self.entrySet.pack()
        self.entryRarity.pack()
        self.isLegendaryRadio.pack()

        self.commitButton = Button(right_frame, bg="red", fg="blue", text="commit")
        self.cancelButton = Button(right_frame, bg="red", fg="blue", text="cancel")

        # self.commitButton.config(command=self.commitRow)
        # self.cancelButton.config(command=self.cancelInsert)

        self.commitButton.pack(side=LEFT)
        self.cancelButton.pack(side=LEFT)

        table_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        right_frame.pack(expand=YES, fill=BOTH, side=LEFT)
        self.top_f.pack()
        self.bottom_frame.pack()

    def commitRow(self, view):
        pass

    def cancelInsert(self, view):
        self.cancelButton.bind('<ButtonRelease-1>', insertFrameChanger(self, view))
