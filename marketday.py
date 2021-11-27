#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 26.11.2021
# marketday (coinstar)


class Market_day():

    def __init__(self, date, start, end, volume=None, bearish=False):

        self.date = date
        self.open_value = start
        self.close_value = end
        self.is_bearish = bearish
        self.trading_volume = volume
