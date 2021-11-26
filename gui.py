#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# GUI (coinstar)

import sys
from  tkinter import *

class Gui():

    def __init__(self):
        pass

        self.run()

    def run(self):

        # Setup the window
        root = Tk()
        root.title("Coinstar GUI")
        # root.configure(bg="#050505")
        # root.geometry("400x200")

        # frame = Frame(root, padding=10)
        # frame.grid()

        # l_title = Label(root, text="Oh wow!")
        # l_title.grid(row=0, column=0)


        # BUTTONS

        btn_close = Button(root, text="Close", command=close, bg="#C08080", padx=10, pady=10)
        btn_close.grid(row=90, column=2)

        btn_get = Button(root, text="Get", command=self.get, bg="#80C080", padx=30, pady=15)
        btn_get.grid(row=90, column=1, padx=0, pady=5)

        # LABELS

        l_start = Label(root, text="Start date")
        l_start.grid(row=2, column=0)

        l_end = Label(root, text="End date")
        l_end.grid(row=4, column=0)

        # ENTRY FIELDS

        self.e_start = Entry(root, width=50)#, bg="#808080", fg="#000000")
        self.e_start.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.e_start.insert(0, "YYYY.MM.DD")

        self.e_end = Entry(root, width=50)#, bg="#808080", fg="#000000")
        self.e_end.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        self.e_end.insert(0, "YYYY.MM.DD")

        # Start program
        root.mainloop()


    def get(self):
        """Get start market data from 'start' to 'end'"""
        start = self.e_start.get()
        end = self.e_end.get()

def close():
    sys.exit()

if __name__ == "__main__":
    gui = Gui()

