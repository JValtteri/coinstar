#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import datetime
import sys, getopt
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


def main(argv):
    """Main function"""
    # Parse arguments

    helptext = 'coinstar.py <opts>\n\n' \
               '-s    --start  <start date> YYYY.MM.DD\n' \
               '-e    --end    <end date>   YYYY.MM.DD\n' \
               '-r    --raw                 Show raw data\n' \
               '-h    --help                Show this help\n'
    print_raw = False

    try:
        opts, args = getopt.getopt(argv,"hrs:e:",["start=","end=","help"])
    except getopt.GetoptError:
        print ('coinstar.py -s <start date> -e <end date> -r --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', 'help') or len(argv) is 0:
            print (helptext)
            sys.exit()
        elif opt in ("-s", "--start"):
            start_str = arg
        elif opt in ("-e", "--end"):
            end_str = arg
        elif opt in ("-r", "--raw"):
            print_raw = True

    if opts == []:
        print ('coinstar.py -s <start date> -e <end date> -r --help')
        sys.exit(2)

    start = [int(i) for i in start_str.split('.')]
    end = [int(i) for i in end_str.split('.')]

    # Process market data
    market = Market(
        time_from = time_to_posix(start[0], start[1], start[2]),
        time_to = time_to_posix(end[0], end[1], end[2]),
        coin="bitcoin",
        currency="eur"
    )

    # Print program outputs
    print(f"Start date: {start_str}")
    print(f"End date: {end_str}")

    market.print_days()
    print(f"Max Bearish: {market.longest_bearish}")
    if print_raw:
        print_datapoints(market.prices, "Prices")
        print_datapoints(market.volumes, "Volumes")

if __name__ == "__main__":
    main(sys.argv[1:])
