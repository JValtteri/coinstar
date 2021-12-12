#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# GUI (coinstar)

from getopt import error
import sys
from  tkinter import *
from  tkinter import ttk
from tkinter import messagebox
import coinstar

class Gui():

    def __init__(self):

        self.status = coinstar.Status()
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

        btn_get = Button(root, text="Get", command=self.get, bg="#80C080", padx=30, pady=15)
        btn_get.grid(row=90, column=1, padx=0, pady=5)

        btn_reset = Button(root, text="Reset", command=self.reset, padx=10, pady=10)
        btn_reset.grid(row=90, column=0, padx=0, pady=5)

        btn_close = Button(root, text="Close", command=close, bg="#C08080", padx=10, pady=10)
        btn_close.grid(row=90, column=2)

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

        self.e_end = Entry(root, width=50)#, bg="#808080", fg="#000000")
        self.e_end.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

        self.reset_inputs()

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
        s = self.status

        start_str = self.e_start.get()
        end_str = self.e_end.get()
        s.start, s.end, s.error = coinstar.parse_date(start_str, end_str)
        if s.error:
            messagebox.showwarning(title="Warning", message=s.error)

        self.clear_outputs()

        market = s.get_market()
        bearish = market.find_bearish()
        max_volume, volume_day = market.find_max_volume()
        max_volume = round(max_volume)
        buy = market.best_buy_and_sell["buy"]
        sell = market.best_buy_and_sell["sell"]
        profit = round( market.best_buy_and_sell["profit"], 2 )

        self.e_bear.insert("0", bearish)
        self.e_vol_day.insert("0", volume_day)
        self.e_vol.insert("0", max_volume)
        self.e_buy.insert("0", buy)
        self.e_sell.insert("0", sell)
        self.e_profit.insert("0", profit)

    def reset(self):
        """Reset Button action"""
        self.clear_outputs()
        self.reset_inputs()

    def clear_outputs(self):
        """Clears the output fields"""
        self.e_bear.delete("0", END)
        self.e_vol_day.delete("0", END)
        self.e_vol.delete("0", END)
        self.e_buy.delete("0", END)
        self.e_sell.delete("0", END)
        self.e_profit.delete("0", END)

    def reset_inputs(self):
        """Resets the input fields to examples"""
        self.e_start.delete(0, END)
        self.e_end.delete(0, END)
        self.e_start.insert(0, "YYYY.MM.DD")
        self.e_end.insert(0, "YYYY.MM.DD")

def close():
    sys.exit()

if __name__ == "__main__":
    gui = Gui()

