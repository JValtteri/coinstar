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
               '-d    --data-points         Show formatted datapoints\n' \
               '-h    --help                Show this help\n'
    show_raw = False
    show_points = False

    if argv == []:
        # Start GUI
        # ui.start()
        print(short_help)
        sys.exit()

    # Parse arguments
    try:
        opts, args = getopt.getopt(argv,"hrds:e:",["start=","end=","help","data-points"])
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
        elif opt in ("-d", "--data-points"):
            show_points = True
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

    # Process market data
    market = Market(
        time_from = time_to_posix(start[0], start[1], start[2]),
        time_to = time_to_posix(end[0], end[1], end[2]),
        coin="bitcoin",
        currency="eur"
    )

    # Print program outputs
    print(f"\nStart date: {start_str}, End date: {end_str}\n")
    # print(f"End date: {end_str}")

    market.print_days()
    print(f"Max Bearish: {market.longest_bearish}")
    # print(f"Max vomume was {market.max_volume_date}: {market.max_volume}")

    if show_raw:
        print_raw(market.prices, "Prices")
        print_raw(market.volumes, "Volumes")

    if show_points:
        print_datapoints(market.prices, market.volumes)


if __name__ == "__main__":
    main(sys.argv[1:])
