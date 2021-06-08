from tkinter import *
import tkinter.ttk as ttk

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
