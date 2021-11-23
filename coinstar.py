#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import time, datetime
import requests


class Market():

    def __init__(self, time_from, time_to, coin='bitcoin', currency='eur'):

        SECONDS_IN_DAY = 86400 # seconds

        self.time_from = time_from - 3600
        self.time_to = time_to + 3600
        self.coin = coin
        self.currency = currency

        # Get market data
        self.transactions = self.https_getter()
        self.prices = self.transactions['prices']
        self.volumes = self.transactions['total_volumes']

        # self.market_days = self.create_days()


    def bearish_length(self):
        pass

    def is_bearish(self):
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
        return r.json()

    def create_days(self):
        market_days=[]

        market_days.append( Market_day(start, end, volume) )

        return market_days


class Market_day():

    def __init__(self, start, end, volume):

        self.start_value = start
        self.close_value = end
        self.is_bearish = start > end
        self.trading_volume = volume


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    time_object = datetime.datetime(year, mon, day, hour, min, sec)
    timestamp = round( time_object.timestamp() )
    return timestamp


if __name__ == "__main__":
    bitcoin_market = Market(
        time_from = time_to_posix(2021, 11, 22, hour=0, min=0, sec=0),
        time_to = time_to_posix(2021, 11, 23, hour=12, min=0, sec=0),
        coin="bitcoin",
        currency="eur"
    )
    print(f"Prices:")
    print(json.dumps(bitcoin_market.prices, indent=4, sort_keys=True))

    # print(f"volumes:")
    # print(json.dumps(bitcoin_market.volumes, indent=4, sort_keys=True))

