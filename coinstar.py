#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import datetime
import requests

class Market():

    def __init__(self, time_from, time_to, coin='bitcoin', currency='eur'):

        self.SECONDS_IN_DAY = 86400
        self.SECONDS_IN_HOUR = 3600
        self.TIMEOUT = 5

        self.time_from = time_from
        self.time_to = time_to + self.SECONDS_IN_DAY + self.SECONDS_IN_HOUR
        self.coin = coin
        self.currency = currency

        # Get market data
        self.transactions = self.https_getter()
        self.prices = self.transactions['prices']
        self.volumes = self.transactions['total_volumes']

        self.longest_bearish = 0

        self.market_days = self.create_days()


    def update_bearish(self, current_bearish, is_bearish):
        if is_bearish:
            current_bearish += 1
            if current_bearish > self.longest_bearish:
                self.longest_bearish = current_bearish
        else:
            current_bearish = 0

        return current_bearish


    def bearish_length(self):
        pass

    def find_max_volume(self):
        pass

    def best_buy(self):
        pass

    def best_sell(self):
        pass


    def print_days(self):
        for day in self.market_days:
            self.print_day(day)


    def print_day(self, day):
        print(f"Open: {day.open_value} {self.currency}, Close: {day.close_value} {self.currency}, " \
              f"Volume: {day.trading_volume}, Bearish: {day.is_bearish}")


    def https_getter(self):
        address = f"https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart/range"\
                  f"?vs_currency={self.currency}&from={self.time_from}&to={self.time_to}"
        try:
            r = requests.get(address, timeout=self.TIMEOUT)
        except requests.exceptions.ReadTimeout:
            print(f"HTTP timeout {self.TIMEOUT} s exceeded")
            exit()
        return r.json()


    def create_days(self):
        MS_IN_DAY = self.SECONDS_IN_DAY * 1000
        start_of_day = self.time_from * 1000                        # Convert timestamp to ms
        prices = self.prices
        volumes = self.volumes

        TIMESTAMP = 0
        VALUE = 1

        last_day_close_value = 0
        market_days = []
        day_volume = 0
        first_day = True                                            # Is this the first day in range?
        bearish = False
        current_bearish = 0

        for i in range(len(prices)):

            if prices[i][TIMESTAMP] > start_of_day:                 # Look for the start of a new day
                day_close_value = prices[i-1][VALUE]                  # previous datapoint was last days last datapoint.

                if not first_day:
                    is_bearish = last_day_close_value > day_close_value
                    market_days.append( Market_day(day_open_value, day_close_value, day_volume, is_bearish) )

                    current_bearish = self.update_bearish(current_bearish, is_bearish)

                    # Setup variables for next day
                    last_day = market_days[-1]
                    last_day_close_value = last_day.close_value

                # Reset day variables to a new day
                day_open_value = prices[i][VALUE]
                day_volume = volumes[i][VALUE]

                first_day = False
                start_of_day += MS_IN_DAY                           # Next day starts in 24h

            else:
                day_volume += volumes[i][VALUE]                     # Add datapoint volume to the days volume

        return market_days


class Market_day():

    def __init__(self, start, end, volume=None, bearish=False):

        self.open_value = start
        self.close_value = end
        self.is_bearish = bearish
        self.trading_volume = volume


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    time_object = datetime.datetime(year, mon, day, hour, min, sec)
    timestamp = round( time_object.timestamp() )
    return timestamp


if __name__ == "__main__":
    market = Market(
        time_from = time_to_posix(2020, 1, 19),
        time_to = time_to_posix(2020, 1, 21),
        coin="bitcoin",
        currency="eur"
    )

    market.print_days()
    print(f"Max Bearish: {market.longest_bearish}")



    # print(f"Prices:")
    # print(json.dumps(bitcoin_market.prices, indent=4, sort_keys=True))

    # print(f"volumes:")
    # print(json.dumps(bitcoin_market.volumes, indent=4, sort_keys=True))

