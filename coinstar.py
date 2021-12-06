#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import datetime
import sys, getopt
from market import Market
# from gui import *


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    try:
        time_object = datetime.datetime(year, mon, day, hour, min, sec)
    except ValueError:
        print("Date format error: invalid date format\n" \
              "Date format: YYYY.MM.DD")
        sys.exit(2)

    timestamp = round( time_object.timestamp() )
    return timestamp


def print_raw(datapoints, title="datapoints"):
    """function to print the raw datapoints json"""
    print(title)
    print(json.dumps(datapoints, indent=4, sort_keys=True))


def print_datapoints(prices, volumes):
    """Function to print formatted datapoints"""
    print(f"\nTime \t\t\t\t Price \t\t Volume")
    for i in range(len(prices)):
        timestamp = prices[i][0] / 1000                                 # Timestamp (ms -> s)
        price = round( prices[i][1], 2)                                 # Price
        volume = round( volumes[i][1] )                                 # Volume

        if prices[i][0] != volumes[i][0]:                               # Check that timestamps match
            print("Error! Timestamp mismatch")
            sys.exit(2)
        human_time = datetime.datetime.fromtimestamp(timestamp)         # Convert timestamp to human readable form

        print(f"{human_time} \t {price} \t {volume}")


def main(argv):
    """Main function"""

    short_help = 'coinstar.py -s <start date> -e <end date> -r -d --help'
    helptext = 'coinstar.py <opts>\n\n' \
               '-s    --start  <start date> YYYY.MM.DD\n' \
               '-e    --end    <end date>   YYYY.MM.DD\n' \
               '-r    --raw                 Show raw data\n' \
               '-f    --format              Show formatted datapoints\n' \
               '-d    --days                Show day values:\n' \
               '                            Open, Close, Volume, Bearish\n' \
               '-h    --help                Show this help\n'
    show_raw = False
    show_points = False
    show_days = False

    if argv == []:
        # Start GUI
        # ui.start()
        print(short_help)
        sys.exit()

    # Parse arguments
    try:
        opts, args = getopt.getopt(argv,"hrdfs:e:",["start=","end=","help","days","format"])
    except getopt.GetoptError:
        print(short_help)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help') or len(argv) == 0:
            print (helptext)
            sys.exit()
        elif opt in ("-s", "--start"):
            start_str = arg
        elif opt in ("-e", "--end"):
            end_str = arg
        elif opt in ("-f", "--format"):
            show_points = True
        elif opt in ("-d", "--days"):
            show_days = True
        elif opt in ("-r", "--raw"):
            show_raw = True

    if opts == []:
        print(short_help)
        sys.exit(2)

    try:
        start = [int(i) for i in start_str.split('.')]
        end = [int(i) for i in end_str.split('.')]
    except ValueError:
        print("Date format error: numbers only")
        sys.exit(2)
    except UnboundLocalError:
        print("Error: Both start and end date must be defined. Use -h for Help")
        sys.exit(2)

    # Convert dates to POSIX
    start = time_to_posix(start[0], start[1], start[2])
    end = time_to_posix(end[0], end[1], end[2])
    if end < start:
        print("Error: End date is earlier than start date")
        sys.exit(2)

    # Process market data
    market = Market(
        time_from = start,
        time_to = end,
        coin="bitcoin",
        currency="eur"
    )

    # Print program outputs
    print(f"\nStart date: {start_str}, End date: {end_str}\n")
    if show_days == True:
        market.print_days()
    print(f"Max Bearish:\t\t{market.longest_bearish} days")
    print(f"Max vomume was on:\t{market.max_volume_date}")
    print(f"Max volume was:\t\t{market.max_volume} {market.currency}")
    if market.best_buy_and_sell['profit'] > 0:
        print(f"Best day to buy was:\t{market.best_buy_and_sell['buy']}")
        print(f"Best day to sell was:\t{market.best_buy_and_sell['sell']}")
        print(f"Profit was:\t\t{round(market.best_buy_and_sell['profit'], 2)}")
    else:
        print("There was no opportunity to make profit")

    if show_raw:
        print_raw(market.prices, "Prices")
        print_raw(market.volumes, "Volumes")

    if show_points:
        print_datapoints(market.prices, market.volumes)


if __name__ == "__main__":
    main(sys.argv[1:])
