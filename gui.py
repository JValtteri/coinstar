#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# GUI (coinstar)

import sys
from  tkinter import *



def start():

    # Setup the window
    root = Tk()
    root.title="Coinstar GUI"
    # root.configure(bg="#050505")
    # root.geometry("400x200")

    # frame = Frame(root, padding=10)
    # frame.grid()

    # l_title = Label(root, text="Oh wow!")
    # l_title.grid(row=0, column=0)

    btn_close = Button(root, text="Close", command=close, bg="#C00000", padx=10, pady=10)
    btn_close.grid(row=10)

    l_start = Label(root, text="Start date")
    l_start.grid(row=2, column=0)

    e_start = Entry(root, width=50)#, bg="#808080", fg="#000000")
    e_start.grid(row=3, column=0)

    l_end = Label(root, text="End date")
    l_end.grid(row=4, column=0)

    e_end = Entry(root, width=50)#, bg="#808080", fg="#000000")
    e_end.grid(row=5, column=0)

    # Start program
    root.mainloop()


def get():
    pass

def close():
    sys.exit()

if __name__ == "__main__":
    start()
