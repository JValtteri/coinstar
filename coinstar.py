#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 17.11.2021
# coinstar

import json
import datetime
import sys, getopt
import status
import gui
from market import human_readable_date


def time_to_posix(year, mon, day, hour=0, min=0, sec=0):
    """Takes date and time and returns POSIX timestamp in seconds"""
    try:
        time_object = datetime.datetime(year, mon, day, hour, min, sec, tzinfo=datetime.timezone.utc)
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
        human_time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)         # Convert timestamp to human readable form

        print(f"{human_time} \t {price} \t {volume}")

def parse_date(start_str, end_str):
    """Make date_strs to posix dates"""
    error = False

    # Convert date seperators
    start_str = start_str.replace('/', '.')
    end_str = end_str.replace('/', '.')
    start_str = start_str.replace('-', '.')
    end_str = end_str.replace('-', '.')

    try:
        start = [int(i) for i in start_str.split('.')]
        end = [int(i) for i in end_str.split('.')]
    except ValueError:
        error = "Date format error: numbers only\n" \
                "Date format: YYYY.MM.DD"
        return None, None, error
    except UnboundLocalError:
        print("Error: Both start and end date must be defined. Use -h for Help")
        return None, None, error
    # if len(start) != 3 or len(end) != 3:
    #     error = "Date format error: Incomplete date\n" \
    #             "Date format: YYYY.MM.DD"
    #     return start, end, error

    parsed_start = [2000,1,1]
    for i in range(len(start)):
        parsed_start[i] = start[i]
    parsed_end = [2000,1,1]
    for i in range(len(end)):
        parsed_end[i] = end[i]

    # Convert dates to POSIX
    try:
        start_stamp = time_to_posix(parsed_start[0], parsed_start[1], parsed_start[2])
        end_stamp = time_to_posix(parsed_end[0], parsed_end[1], parsed_end[2])
    except:
        error = "Date error: Invalid date\n"
        return start, end, error

    if end < start:
        error = "Error: End date is earlier than start date"
        return parsed_start, end, error

    return start_stamp, end_stamp, error


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
    show_general = False
    show_today = False

    s = status.Status()

    if argv == []:
        # Start GUI
        # ui.start()
        print(short_help)
        sys.exit()

    # Parse arguments
    try:
        opts, args = getopt.getopt(argv,"hrdgfmts:e:",["start=","end=","help","days","format","gui","more","today"])
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
        elif opt in ("-m", "--more"):
            show_general = True
        elif opt in ("-t", "--today"):
            show_today = True
        elif opt in ("-g", "--gui"):
            gui.Gui()
            sys.exit()

    if opts == []:
        print(short_help)
        sys.exit(2)

    ###############################
    # Handling for various inputs #
    ###############################

    if show_today:
        # s.start =
        s.end = datetime.now(tzinfo=datetime.timezone.utc)
    else:
        s.start, s.end, error = parse_date(start_str, end_str)

    if error:
        print(error)
        sys.exit(2)

    # Process market data
    market, error = s.get_market()
    if error:
        print(error)
        sys.exit(2)

    ##################
    # PROGRAM OUTPUT #
    ##################

    start_date, _ = human_readable_date(s.start * 1000)
    end_date, _ = human_readable_date(s.end * 1000)

    print(f"\nStart date: {start_date}, End date: {end_date}\n")

    if show_days == True:
        market.print_days()

    if show_general:
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

    if show_today:

        pass

    if show_raw:
        print_raw(market.prices, "Prices")
        print_raw(market.volumes, "Volumes")

    if show_points:
        print_datapoints(market.prices, market.volumes)


if __name__ == "__main__":
    main(sys.argv[1:])
