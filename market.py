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

        # Get market data
        # self.transactions = self.https_getter(self.time_from, self.time_to)
        # self.prices = self.transactions['prices']
        # self.volumes = self.transactions['total_volumes']

        # Longest bearish is updated during market_days creatiion
        self.longest_bearish = 0

        # Generate a list of market days
        self.market_days = self.create_days()

        # Maximum volume day
        # max_volume, max_volume_date = self.find_max_volume()
        # self.max_volume = max_volume
        # self.max_volume_date = max_volume_date

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
        """Finds the biggest volume day and returns: volume, date"""
        max_volume = 0
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
        min_time_delta = None

        for i in range(len(prices)):
            if prices[i][TIMESTAMP] > midnight_time:                # Look for the start of a new day
                delta_point_a = abs( prices[i][TIMESTAMP] - midnight_time )
                delta_point_b = abs( prices[i-1][TIMESTAMP] - midnight_time )
                if delta_point_a < delta_point_b:                   # See which point is closer to midnight
                    midnight_value = prices[i][TIMESTAMP]
                    break
                else:
                    midnight_value = prices[i-1][TIMESTAMP]
                    break
            else:
                midnight_value = prices[i][TIMESTAMP]

        if len(prices) == 0:
            print(f"Midnight value not found")
            midnight_value = 0

        return midnight_value


    def get_day_volume(self, volumes):
        """Finds the volume for the day"""
        TIMESTAMP = 0
        day_volume = 0
        for volume in volumes:
            day_volume + volume

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
        return r.json()


    def create_days(self):
        """Generates a list of Market_day objects"""
        SECONDS_IN_HOUR = self.SECONDS_IN_HOUR
        MS_IN_DAY = self.MS_IN_DAY
        # start_of_day = self.time_from * 1000                        # Convert timestamp to ms
        # end_of_day = start_of_day + MS_IN_DAY
        day_timestamp = 0
        # prices = self.prices
        # volumes = self.volumes

        TIMESTAMP = 0
        VALUE = 1

        last_day_close_value = 0
        market_days = []
        day_volume = 0
        first_day = True                                            # Is this the first day in range?
        current_bearish = 0

        for start_of_day in range(self.time_from, self.time_to, MS_IN_DAY):

            end_of_day = start_of_day + MS_IN_DAY

            # Make a human readable timestamp
            date = self.human_readable_date(day_timestamp)

            # day_volumes = self.https_getter(start_of_day, end_of_day)["volumes"]
            # day_volume = self.get_day_volume(day_volumes)

            # Get a better resolution datapoints from around 00:00:00 midnight:
            # Start of day
            hour_before_midnight = start_of_day - SECONDS_IN_HOUR * 1000
            hour_after_midnight = start_of_day + SECONDS_IN_HOUR
            open_prices = self.https_getter(hour_before_midnight, hour_after_midnight)["prices"]

            # End of day
            hour_before_midnight = end_of_day - SECONDS_IN_HOUR * 1000
            hour_after_midnight = end_of_day + SECONDS_IN_HOUR
            close_prices = self.https_getter(hour_before_midnight, hour_after_midnight)["prices"]

            # Select the datapoint closest to 00:00:00 at start and end of the day
            day_open_value = self.find_midnight(open_prices, start_of_day - MS_IN_DAY)
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

            day_timestamp = start_of_day

            # start_of_day += MS_IN_DAY

        return market_days


        # # Iterates through datapoints
        # for i in range(len(prices)):

        #     if prices[i][TIMESTAMP] > start_of_day:                 # Look for the start of a new day
        #         day_close_value = prices[i-1][VALUE]                # previous datapoint was last days last datapoint.
        #         date = self.human_readable_date(day_timestamp)         # make human readable

        #         if not first_day:

        #             # Get a better resolution datapoint from

        #             open_prices = self.https_getter()["prices"]
        #             colos_prices = self.https_getter()["prices"]

        #             day_open_value = self.find_midnight(open_prices, start_of_day-MS_IN_DAY)
        #             day_close_value = self.find_midnight(colos_prices, start_of_day)

        #             # Generates the Market_day object and adds it to the list
        #             market_days.append(
        #                 Market_day(
        #                     date,
        #                     day_open_value,
        #                     day_close_value,
        #                     day_volume,
        #                     is_bearish
        #                     )
        #                 )

        #             current_bearish = self.update_bearish(current_bearish, is_bearish)

        #             # Setup variables for next day
        #             last_day = market_days[-1]
        #             last_day_close_value = last_day.close_value

        #         # Reset day variables to a new day
        #         day_open_value = prices[i][VALUE]
        #         day_volume = volumes[i][VALUE]

        #         first_day = False
        #         day_timestamp = start_of_day
        #         start_of_day += MS_IN_DAY                           # Next day starts in 24h

        #     else:
        #         day_volume += volumes[i][VALUE]                     # Add datapoint volume to the days volume

        # return market_days

    @staticmethod
    def human_readable_date(timestamp):
        """Make a human readable time from timestamp"""
        timestamp = timestamp / 1000                            # Convert timestamp from ms to s
        date = datetime.datetime.fromtimestamp(timestamp)       # Make human readable
        date = str(date).split(" ")[0]                          # Remove the time from the date
        date = str.replace(date, '-', '.')
        return date
