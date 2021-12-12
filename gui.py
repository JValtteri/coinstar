#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# GUI (coinstar)

import sys
from  tkinter import *
from  tkinter import ttk
import coinstar
import market

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
        l_start.grid(row=2, column=0, sticky='e')

        l_end = Label(root, text="End date")
        l_end.grid(row=5, column=0, sticky='e')

        l_out = Label(root, text="Output")
        l_out.grid(row=6, column=1)


        l_bearish = Label(root, text="Max bearish was:")
        l_bearish.grid(row=8, column=0, sticky='w')

        l_bearish_unit = Label(root, text="days")
        l_bearish_unit.grid(row=8, column=2, sticky='w')

        l_volume_day = Label(root, text="Max volume was on:")
        l_volume_day.grid(row=9, column=0, sticky='w')

        l_volume = Label(root, text="Max volume was:")
        l_volume.grid(row=10, column=0, sticky='w')



        l_buy = Label(root, text="Buy:")
        l_buy.grid(row=11, column=0, sticky='w')

        l_sell = Label(root, text="Sell:")
        l_sell.grid(row=12, column=0, sticky='w')

        l_profit = Label(root, text="Profit:")
        l_profit.grid(row=13, column=0, sticky='w')

        # l_bearish_unit = Label(root, text="credits")
        # l_bearish_unit.grid(row=10, column=2, sticky='w')

        # SEPARATOR

        separator = ttk.Separator(root, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=3, sticky='ew')#, padx=10, pady=10)

        # ENTRY FIELDS

        self.e_start = Entry(root, width=50)#, bg="#808080", fg="#000000")
        self.e_start.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.e_start.insert(0, "YYYY.MM.DD")

        self.e_end = Entry(root, width=50)#, bg="#808080", fg="#000000")
        self.e_end.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
        self.e_end.insert(0, "YYYY.MM.DD")

        self.e_bear = Entry(root, width=30, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_bear.grid(row=8, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

        self.e_vol_day = Entry(root, width=40, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_vol_day.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

        self.e_vol = Entry(root, width=30, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_vol.grid(row=10, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

        self.e_buy = Entry(root, width=30, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_buy.grid(row=11, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

        self.e_sell = Entry(root, width=30, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_sell.grid(row=12, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

        self.e_profit = Entry(root, width=30, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_profit.grid(row=13, column=1, columnspan=1, padx=10, pady=10, sticky='ew')
        # self.e_bear.insert(0, "YYYY.MM.DD")

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

