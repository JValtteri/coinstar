#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import datetime
from market import Market


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    time_object = datetime.datetime(year, mon, day, hour, min, sec)
    timestamp = round( time_object.timestamp() )
    return timestamp

def print_datapoints(datapoints, title="datapoints"):
    """function to print the raw datapoints json"""
    print(title)
    print(json.dumps(datapoints, indent=4, sort_keys=True))

if __name__ == "__main__":
    market = Market(
        time_from = time_to_posix(2020, 1, 19),
        time_to = time_to_posix(2020, 1, 21),
        coin="bitcoin",
        currency="eur"
    )

    market.print_days()
    print(f"Max Bearish: {market.longest_bearish}")


    print_datapoints(market.prices, "Prices")
    print_datapoints(market.volumes, "Volumes")
