from collections import OrderedDict
from tkinter import *
import tkinter.ttk as ttk

from sqlalchemy import create_engine, func, inspect, MetaData
from sqlalchemy.engine import Inspector
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Table as SQLTable

import dataClasses
from config import USER, PASSWORD
from dataClasses import engine


def migrate_to_table(forget, show):
    forget.parent.master.master.pack_forget()
    show.db = forget.db

    Session = sessionmaker(bind=engine)  # bound session
    session = Session()
    rows_data = [q for q in session.query(func.public.all_tables(forget.db, PASSWORD)).all()]
    show.table.free()

    show.table.fill(rows_data)
    show.update()

    show.pack()

class Table:
    def __init__(self, parent, headings=tuple(), rows=tuple()):
        table = ttk.Treeview(parent, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings
        self.headings = headings

        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, anchor=CENTER)

        for row in rows:
            if type(row) != str:
                table.insert('', END, values=tuple(row))
            else:
                table.insert('', END, values=row)

        scrolltable = Scrollbar(parent, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH)
        self.table = table
        self.parent = parent

    def pack(self, *args, **kwargs):
        self.table.pack(*args, **kwargs)

    def generation(self, another):
        def print_selection(event):
            for selection in self.table.selection():
                item = self.table.item(selection)
                print(item["values"])
                self.db = item["values"][0]
                dataClasses.new_engine = create_engine('postgresql://{}:{}@localhost/{}'.format(USER, PASSWORD, item["values"][0]),
                       echo=True)
                migrate_to_table(self, another)

        return print_selection

    def next_generation(self, show):
        def changer(event):
            for selection in self.table.selection():
                item = self.table.item(selection)
                print(item["values"])
                self.tablename = item["values"][0]

                inspector = inspect(dataClasses.new_engine)
                meta = MetaData(dataClasses.new_engine)
                user_table = SQLTable(self.tablename, meta)
                inspector.reflect_table(user_table, None)
                #i = Inspector()
                #i.get


                Session = sessionmaker(bind=dataClasses.new_engine)  # bound session
                session = Session()
                #i = Inspector()
                #i.get_columns()
                data = session.query(user_table).all()
                headings = [head['name'] for head in inspector.get_columns(user_table)]
                # for card in data:
                #     card.pop('_sa_instance_state')
                sorted_data = [list(OrderedDict((k, d[k]) for k in headings).values()) for d in data]
                show.table.free()
                show.table.fill(sorted_data)
                show.update()

                self.parent.master.master.pack_forget()
                show.pack()


        return changer

    def free(self):
        #self.table.get_children();
        for i in self.table.get_children():
            self.table.delete(i)

    def fill(self, rows=tuple()):
        for row in rows:
            self.table.insert('', END, values=tuple(row))
