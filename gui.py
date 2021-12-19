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
import status

class Gui():

    def __init__(self):

        # SETUP THE WINDOW

        self.root = Tk()
        self.root.title("Coinstar GUI")
        # root.configure(bg="#050505")

        # Creates an object to hold the status of the program
        self.status = status.Status()
        self.example_format = "YYYY.MM.DD"

        # Bind ENTER key to get() function (GET Button)
        self.root.bind('<Return>', self.get)

        # INPUT
        self.create_input_area()
        self.reset_inputs()

        # BUTTONS
        self.create_buttons()

        # SEPARATOR
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=3, sticky='ew')

        # OUTPUT
        self.ceate_output_area()

        self.run()


    def run(self):

        # START PROGRAM
        self.root.mainloop()


    def create_buttons(self):
        """Create buttons"""
        btn_get = Button(self.root, text="Get", command=self.get, bg="#80C080", padx=30, pady=15)
        btn_get.grid(row=90, column=1, padx=0, pady=5)

        btn_reset = Button(self.root, text="Reset", command=self.reset, padx=10, pady=10)
        btn_reset.grid(row=90, column=0, padx=0, pady=5)

        btn_close = Button(self.root, text="Close", command=close, bg="#C08080", padx=10, pady=10)
        btn_close.grid(row=90, column=2, padx=10, pady=10)


    def create_input_area(self):
        """Creates input area GUI"""

        # LABELS

        l_start = Label(self.root, text="Start date")
        l_start.grid(row=2, column=0, sticky='e')

        l_end = Label(self.root, text="End date")
        l_end.grid(row=5, column=0, sticky='e')

        # ENTRY FIELDS

        self.e_start = Entry(self.root, width=30)#, bg="#808080", fg="#000000")
        self.e_start.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        self.e_start.bind("<1>", self.clear_start)

        self.e_end = Entry(self.root, width=30)#, bg="#808080", fg="#000000")
        self.e_end.grid(row=5, column=1, columnspan=2, padx=10, pady=10)
        self.e_end.bind("<1>", self.clear_end)


    def ceate_output_area(self):
        """Creates output area GUI"""

        # LABELS

        l_bearish = Label(self.root, text="Max bearish was:")
        l_bearish.grid(row=8, column=0, padx=10, sticky='w')

        l_bearish_unit = Label(self.root, text="days")
        l_bearish_unit.grid(row=8, column=2, sticky='w')

        self.units = StringVar()
        self.units.set("")

        l_vol_unit = Label(self.root, textvariable=self.units)
        l_vol_unit.grid(row=10, column=2, sticky='w')

        l_profit_unit = Label(self.root, textvariable=self.units)
        l_profit_unit.grid(row=13, column=2, sticky='w')

        l_volume_day = Label(self.root, text="Max volume was on:")
        l_volume_day.grid(row=9, column=0, padx=10, sticky='w')

        l_volume = Label(self.root, text="Max volume was:")
        l_volume.grid(row=10, column=0, padx=10, sticky='w')

        l_buy = Label(self.root, text="Buy:")
        l_buy.grid(row=11, column=0, padx=10, sticky='w')

        l_sell = Label(self.root, text="Sell:")
        l_sell.grid(row=12, column=0, padx=10, sticky='w')

        l_profit = Label(self.root, text="Profit:")
        l_profit.grid(row=13, column=0, padx=10, sticky='w')

        # ENTRY FIELDS

        self.e_bear = Entry(self.root, width=10, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_bear.grid(row=8, column=1, columnspan=1, padx=10, pady=10, sticky='ew')

        self.e_vol_day = Entry(self.root, width=25, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_vol_day.grid(row=9, column=1, columnspan=1, padx=10, pady=10, sticky='ew')

        self.e_vol = Entry(self.root, width=25, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_vol.grid(row=10, column=1, columnspan=1, padx=10, pady=10, sticky='ew')

        self.e_buy = Entry(self.root, width=25, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_buy.grid(row=11, column=1, columnspan=1, padx=10, pady=10, sticky='ew')

        self.e_sell = Entry(self.root, width=25, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_sell.grid(row=12, column=1, columnspan=1, padx=10, pady=10, sticky='ew')

        self.e_profit = Entry(self.root, width=25, bg="#EEEEEE")#, bg="#808080", fg="#000000")
        self.e_profit.grid(row=13, column=1, columnspan=1, padx=10, pady=10, sticky='ew')


    def get(self, event=None):
        """Get market data from 'start' to 'end' and display it"""
        s = self.status

        # GET INPUT VALUES

        start_str = self.e_start.get()
        end_str = self.e_end.get()
        s.start, s.end, s.error = coinstar.parse_date(start_str, end_str)
        if s.error:
            messagebox.showwarning(title="Warning", message=s.error)

        # CLEAR OUTPUT FIELD FOR NEW VALUES

        self.clear_outputs()

        # DEFINE OUTPUT VALUES

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

        self.update_units(s)


    def update_units(self, s):
        """Update displayed units"""
        self.units.set(s.currency)


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


    def clear_start(self, event=None):
        if self.e_start.get() == self.example_format:
            self.e_start.delete(0, END)


    def clear_end(self, event=None):
        if self.e_end.get() == self.example_format:
            self.e_end.delete(0, END)


def close():
    sys.exit()

if __name__ == "__main__":
    gui = Gui()

