#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import datetime
import sys, getopt
from market import Market
import gui


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
               '-g    --gui                 Start GUI\n' \
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
        opts, args = getopt.getopt(argv,"hrdgfs:e:",["start=","end=","help","days","format","gui"])
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
        elif opt in ("-g", "--gui"):
            gui.Gui()
            sys.exit()

    if opts == []:
        print(short_help)
        sys.exit(2)

    ###############################
    # Handling for various inputs #
    ###############################

    # Convert date seperators
    start_str = start_str.replace('/', '.')
    end_str = end_str.replace('/', '.')
    start_str = start_str.replace('-', '.')
    end_str = end_str.replace('-', '.')

    try:
        start = [int(i) for i in start_str.split('.')]
        end = [int(i) for i in end_str.split('.')]
    except ValueError:
        print("Date format error: numbers only\n" \
              "Date format: YYYY.MM.DD")
        sys.exit(2)
    except UnboundLocalError:
        print("Error: Both start and end date must be defined. Use -h for Help")
        sys.exit(2)
    if len(start) != 3 or len(end) != 3:
        print("Date format error: Incomplete date\n" \
              "Date format: YYYY.MM.DD")
        sys.exit(2)

    # Convert dates to POSIX
    try:
        start = time_to_posix(start[0], start[1], start[2])
        end = time_to_posix(end[0], end[1], end[2])
    except:
        print("Date error: Invalid date\n")
        sys.exit(2)

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

    ##################
    # PROGRAM OUTPUT #
    ##################

    print(f"\nStart date: {start_str}, End date: {end_str}\n")

    if show_days == True:
        market.print_days()
    print(f"Max bearish length:\t{market.longest_bearish} days")
    print(f"Max volume was on:\t{market.max_volume_date}")
    print(f"Max volume was:\t\t{round(market.max_volume)} {market.currency}")

    if market.best_buy_and_sell['profit'] > 0:
        buy_day = market.best_buy_and_sell['buy']
        sell_day = market.best_buy_and_sell['sell']
        profit = round(market.best_buy_and_sell['profit'], 2)

        print(f"Best day to buy was:\t{buy_day}")
        print(f"Best day to sell was:\t{sell_day}")
        print(f"Profit was:\t\t{profit} {market.currency}")
    else:
        print("There was no opportunity to make profit")

    if show_raw:
        print_raw(market.prices, "Prices")
        print_raw(market.volumes, "Volumes")

    if show_points:
        print_datapoints(market.prices, market.volumes)


if __name__ == "__main__":
    main(sys.argv[1:])
