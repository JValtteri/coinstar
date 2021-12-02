#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 26.11.2021
# market (coinstar)

import datetime
import requests
from marketday import Market_day

class Market():

    def __init__(self, time_from, time_to, coin='bitcoin', currency='eur'):

        self.SECONDS_IN_DAY = 86400
        self.MS_IN_DAY = self.SECONDS_IN_DAY * 1000
        self.SECONDS_IN_HOUR = 3600
        self.TIMEOUT = 5

        self.time_from = time_from
        self.time_to = time_to + self.SECONDS_IN_DAY #+ self.SECONDS_IN_HOUR
        self.coin = coin
        self.currency = currency

        # Generate a list of market days
        self.market_days = self.create_days()

        # Longest bearish is updated during market_days creation
        self.longest_bearish = 0
        self.longest_bearish = self.find_bearish()

        # Maximum volume day
        max_volume, max_volume_date = self.find_max_volume()
        self.max_volume = max_volume
        self.max_volume_date = max_volume_date


    def find_bearish(self):
        longest_bearish = 0
        current_bearish = 0
        for day in self.market_days:
            if day.is_bearish:
                current_bearish += 1
                # print(f"bearish now is {current_bearish}")
                if current_bearish > longest_bearish:
                    longest_bearish = current_bearish
            else:
                current_bearish = 0

        return longest_bearish


    def bearish_length(self):
        pass

    def find_max_volume(self):
        """Finds the biggest volume day and returns: volume, date"""
        max_volume = 0
        max_volume_day = 0
        for day in self.market_days:
            if day.trading_volume > max_volume:
                max_volume = day.trading_volume
                max_volume_day = day.date

        return max_volume, max_volume_day

    def best_buy(self):
        pass

    def best_sell(self):
        pass


    def print_days(self):
        for day in self.market_days:
            self.print_day(day)
        print("")


    def find_midnight(self, prices, midnight_time):
        """Finds the price closest to midnight"""
        TIMESTAMP = 0
        VALUE = 1
        midnight_time = midnight_time * 1000                        # Convert to MS

        for i in range(len(prices)):
            # Look for the point closest to midnight
            # i.e. smalles delta time
            if prices[i][TIMESTAMP] > midnight_time:
                delta_point_a = abs( prices[i][TIMESTAMP] - midnight_time )
                delta_point_b = abs( prices[i-1][TIMESTAMP] - midnight_time )

                # See which point is closer to midnight
                if delta_point_a < delta_point_b:
                    midnight_value = prices[i][VALUE]
                    print("Midnight timestamp")
                    stamp = prices[i][TIMESTAMP]
                    print(datetime.datetime.fromtimestamp(stamp/1000))
                    break
                else:
                    midnight_value = prices[i-1][VALUE]
                    print("Midnight timestamp")
                    stamp = prices[i][TIMESTAMP]
                    print( datetime.datetime.fromtimestamp(stamp/1000) )
                    break
            else:
                midnight_value = prices[i][VALUE]

        if len(prices) == 0:
            # print(f"Midnight value not found")
            midnight_value = 0

        return midnight_value


    def get_day_volume(self, volumes):
        """Finds the volume for the day"""
        TIMESTAMP = 0
        day_volume = 0
        for volume in volumes:
            day_volume += volume[1]

        return day_volume


    def print_day(self, day):
        """Prints the key figures of a market day"""
        date = day.date
        open_value = round(day.open_value, 3)
        close_value = round(day.close_value, 3)
        volume = round(day.trading_volume)
        currency = self.currency

        print(f"Date: {day.date}, Open: {open_value} {currency}, Close: {close_value} {currency}, " \
              f"Volume: {volume}, Bearish: {day.is_bearish}")


    def https_getter(self, time_from, time_to):
        address = f"https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart/range"\
                  f"?vs_currency={self.currency}&from={time_from}&to={time_to}"
        try:
            r = requests.get(address, timeout=self.TIMEOUT)
        except requests.exceptions.ReadTimeout:
            print(f"HTTP timeout {self.TIMEOUT} s exceeded")
            exit()
        try:
            return r.json()
        except:
            print("HTTP Returned empty")
            return {
                "total_volumes": [],
                "prices": []
            }


    def create_days(self):
        """Generates a list of Market_day objects"""
        SECONDS_IN_HOUR = self.SECONDS_IN_HOUR
        SECONDS_IN_DAY = self.SECONDS_IN_DAY

        TIMESTAMP = 0
        VALUE = 1

        market_days = []
        day_volume = 0

        for start_of_day in range(self.time_from, self.time_to, SECONDS_IN_DAY):

            # print("Start of day")
            # print( datetime.datetime.fromtimestamp(start_of_day) )

            end_of_day = start_of_day + SECONDS_IN_DAY

            # Make a human readable timestamp
            date = self.human_readable_date(start_of_day*1000)

            day_volumes = self.https_getter(start_of_day, end_of_day)["total_volumes"]
            day_volume = self.get_day_volume(day_volumes)

            # Get a better resolution datapoints from around 00:00:00 midnight:
            # Start of day
            hour_before_midnight = start_of_day - SECONDS_IN_HOUR
            hour_after_midnight = start_of_day + SECONDS_IN_HOUR

            open_prices = self.https_getter(hour_before_midnight, hour_after_midnight)["prices"]
            # self.foo(open_prices)

            # End of day
            hour_before_midnight = end_of_day - SECONDS_IN_HOUR
            hour_after_midnight = end_of_day + SECONDS_IN_HOUR
            close_prices = self.https_getter(hour_before_midnight, hour_after_midnight)["prices"]

            # Select the datapoint closest to 00:00:00 at start and end of the day
            day_open_value = self.find_midnight(open_prices, start_of_day - SECONDS_IN_DAY)
            day_close_value = self.find_midnight(close_prices, start_of_day)

            # Generates the Market_day object and adds it to the list
            market_days.append(
                Market_day(
                    date,
                    day_open_value,
                    day_close_value,
                    day_volume
                    )
                )

            # start_of_day += MS_IN_DAY

        return market_days


    @staticmethod
    def foo(prices):
        print("Midnight values:")
        for price in prices:
            atime = datetime.datetime.fromtimestamp( price[0]/1000 )
            value = price[1]
            print(f"{atime} {value}")



    @staticmethod
    def human_readable_date(timestamp):
        """Make a human readable time from timestamp"""
        timestamp = timestamp / 1000                            # Convert timestamp from ms to s
        date = datetime.datetime.fromtimestamp(timestamp)       # Make human readable
        date = str(date).split(" ")[0]                          # Remove the time from the date
        date = str.replace(date, '-', '.')
        return date
