#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import time, datetime
import requests

class Market():

    def __init__(self, time_from, time_to, coin='bitcoin', currency='eur'):

        self.time_from
        self.time_to,
        self.coin='bitcoin'
        self.currency='eur'

def bearish_length(self):
    pass

def find_max_volume(self):
    pass

def best_buy(self):
    pass

def best_sell(self):
    pass

def https_getter(self):

    address = f"https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart/range"\
              f"?vs_currency={self.currency}&from={self.time_from}&to={self.time_to}"
    r = requests.get(address)
    r.json()

def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    time_object = datetime.datetime(year, mon, day, hour, min, sec)
    timestamp = round( time_object.timestamp() )
    return timestamp

if __name__ == "__main__":
    pass
