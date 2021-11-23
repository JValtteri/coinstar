#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import time, datetime
import requests


class Market():

    def __init__(self, time_from, time_to, coin='bitcoin', currency='eur'):

        self.SECONDS_IN_DAY = 86400
        self.SECONDS_IN_HOUR = 3600

        self.time_from = time_from
        self.time_to = time_to + self.SECONDS_IN_DAY + self.SECONDS_IN_HOUR
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
        start_of_day = self.time_from
        last_value = 0
        market_days = []
        day_volume = []
        for datapoint in self.prices:
            if datapoint[0] > start_of_day:
                start_of_day += self.SECONDS_IN_DAY
                start_value = datapoint[1]

        try:
            bearish = market_days[-1].close_value > end_value

        except KeyError:
            # If day is the first day, previous day is not defined
            bearish = False

        market_days.append( Market_day(start_value, end_value, volume, bearish) )

        return market_days


class Market_day():

    def __init__(self, start, end, volume, bearish):

        self.start_value = start
        self.close_value = end
        self.is_bearish = bearish
        self.trading_volume = volume


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    time_object = datetime.datetime(year, mon, day, hour, min, sec)
    timestamp = round( time_object.timestamp() )
    return timestamp


if __name__ == "__main__":
    bitcoin_market = Market(
        time_from = time_to_posix(2021, 11, 22),
        time_to = time_to_posix(2021, 11, 23),
        coin="bitcoin",
        currency="eur"
    )
    print(f"Prices:")
    print(json.dumps(bitcoin_market.prices, indent=4, sort_keys=True))

    # print(f"volumes:")
    # print(json.dumps(bitcoin_market.volumes, indent=4, sort_keys=True))

