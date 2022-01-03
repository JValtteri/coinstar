#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# J.V.Ojala 12.12.2021
# status (coinstar)

from market import Market

class Status():
    '''Stores the state of the program. Mostly for GUI'''

    def __init__(self, coin="bitcoin", currency="eur"):

        self.start = None
        self.end = None
        self.market = None
        self.coin=coin
        self.currency=currency

        self.error = False

    def get_market(self):
        """Returns a valid"""
        self.market = Market(
            time_from = self.start,
            time_to = self.end,
            coin=self.coin,
            currency=self.currency
        )
        return self.market, self.market.error
