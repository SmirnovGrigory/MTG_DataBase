from tkinter import Frame, Button, Entry
from config import USER, PASSWORD
import tkinter.ttk as ttk


def LoginCardChanger(forget, show):
    def changer(event):
        if forget.login.get() == USER and forget.password.get() == PASSWORD:
            #print(forget.password.get())
            forget.pack_forget()
            show.pack()
        else:
            if forget.login.get() != USER:
                print("Wrong login!")
            elif forget.password.get() != PASSWORD:
                print("Wrong password!")

    return changer


class LoginFrame(Frame):

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
                                  values=('Lol', 'Alex', 'Bob', 'postgres', USER), width=70, justify='center')
        self.login.set(USER)
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
