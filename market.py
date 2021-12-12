#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 26.11.2021
# market (coinstar)

import time
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
        self.time_to = time_to + self.SECONDS_IN_DAY
        self.coin = coin
        self.currency = currency

        # API Throttiling
        self.request_count = 0
        self.throttle_limit = 49

        # Variable names for dataseries'
        self.prices = None
        self.volumes = None

        # Generate a list of market days
        self.market_days = self.create_days()

        # Longest bearish is updated during market_days creation
        self.longest_bearish = 0
        self.longest_bearish = self.find_bearish()

        # Maximum volume day
        max_volume, max_volume_date = self.find_max_volume()
        self.max_volume = max_volume
        self.max_volume_date = max_volume_date

        self.best_sell_for_days()
        self.best_buy_and_sell = self.find_best_buy_and_sell()


    def find_bearish(self):
        longest_bearish = 0
        current_bearish = 0
        for day in self.market_days:
            if day.is_bearish:
                current_bearish += 1
                if current_bearish > longest_bearish:
                    longest_bearish = current_bearish
            else:
                current_bearish = 0

        return longest_bearish


    def find_max_volume(self):
        """Finds the biggest volume day and returns: volume, date"""
        max_volume = 0
        max_volume_day = ''
        for day in self.market_days:
            if day.trading_volume > max_volume:
                max_volume = day.trading_volume
                max_volume_day = day.date

        return max_volume, max_volume_day


    def best_sell_for_days(self):
        """Finds the Best day to buy and best day to sell the bought coins"""
        # Find the best day to sell coins bought each day
        for i, buy_day in enumerate(self.market_days):
            sell_profit = []

            # Find the best day to sell coins bought on day i
            # Iterates through days
            for j in range( i, len(self.market_days) ):
                sell_day_price = self.market_days[j].close_value
                buy_day_price = buy_day.close_value
                profit = sell_day_price - buy_day_price
                timestamp = self.market_days[j].date
                sell_profit.append((profit, timestamp))

            # Takes the best profit and saves a tuple
            # (profit, date) to market day
            sell_profit.sort()
            buy_day.sell_profit = sell_profit[-1]


    def find_best_buy_and_sell(self):
        """Finds the most profitable buy-sell date pair"""
        max_profit_tuple = ()
        max_profit_day = None
        for buy_day in self.market_days:
            if buy_day.sell_profit > max_profit_tuple:
                max_profit_tuple = buy_day.sell_profit
                max_profit_day = buy_day.date
        max_profit = {
            "buy": max_profit_day,
            "sell": max_profit_tuple[1],
            "profit": max_profit_tuple[0]
        }
        return max_profit


    def print_days(self):
        """Print key figures for all days"""
        for day in self.market_days:
            self.print_day(day)
        print("")


    def print_day(self, day):
        """Prints the key figures of a market day"""
        date = day.date
        open_value = round(day.open_value, 3)
        close_value = round(day.close_value, 3)
        volume = round(day.trading_volume)
        currency = self.currency

        print(f"Date: {day.date}, Open: {open_value} {currency}, Close: {close_value} {currency}, " \
              f"Volume: {volume}, Bearish: {day.is_bearish}")


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
                    break
                else:
                    midnight_value = prices[i-1][VALUE]
                    break
            else:
                midnight_value = prices[i][VALUE]

        if len(prices) == 0:
            # print(f"Midnight value not found")
            midnight_value = 0

        return midnight_value


    def get_day_volume(self, start, end, volumes):
        """Finds the volume for the day"""
        day_volume = 0
        start = start * 1000
        end = end * 1000
        for volume in volumes:
            # If datapoint is between start and end
            if start < volume[0] < end:
                day_volume += volume[1]
            # If datapoint is past the end, stop iterating
            elif volume[0] > end:
                break

        return day_volume


    def https_getter(self, time_from, time_to):
        address = f"https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart/range"\
                  f"?vs_currency={self.currency}&from={time_from}&to={time_to}"
        try:
            r = requests.get(address, timeout=self.TIMEOUT)
        except requests.exceptions.ReadTimeout:
            print(f"HTTP timeout {self.TIMEOUT} s exceeded")
            exit()
        except:
            print(f"HTTP connection error")
            exit()
        self.request_count += 1
        if self.request_count >= self.throttle_limit:
            print("Throttling connection")
            time.sleep(1.21)
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
        SECONDS_IN_DAY = self.SECONDS_IN_DAY

        market_days = []
        day_volume = 0

        # Get data
        sample_start = self.time_from
        sample_end = self.time_to + self.SECONDS_IN_HOUR
        sample_data = self.https_getter(sample_start, sample_end)

        prices = sample_data["prices"]
        day_volumes = sample_data["total_volumes"]
        self.prices = prices
        self.volumes = day_volumes

        # Generate days from data
        for start_of_day in range(self.time_from, self.time_to, SECONDS_IN_DAY):
            end_of_day = start_of_day + SECONDS_IN_DAY

            # Make a human readable timestamp
            date = self.human_readable_date(start_of_day*1000)

            day_volume = self.get_day_volume(start_of_day, end_of_day, day_volumes)

            if day_volume > 0:
                # Select the datapoint closest to 00:00:00 at start and end of the day
                day_open_value = self.find_midnight(prices, start_of_day)
                day_close_value = self.find_midnight(prices, end_of_day)

                # Generates the Market_day object and adds it to the list
                market_days.append(
                    Market_day(
                        date,
                        day_open_value,
                        day_close_value,
                        day_volume
                        )
                    )

        return market_days


    @staticmethod
    def human_readable_date(timestamp):
        """Make a human readable time from timestamp"""
        timestamp = timestamp / 1000                            # Convert timestamp from ms to s
        date = datetime.datetime.fromtimestamp(timestamp)       # Make human readable
        date = str(date).split(" ")[0]                          # Remove the time from the date
        date = str.replace(date, '-', '.')
        return date
