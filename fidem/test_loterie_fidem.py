#!/usr/bin/env python
"""
Test cases for fidem.application
"""
# TODO: do more unit tests

import unittest
from fidem import application


def _are_unique(items):
    # check that all elements are unique
    return len(items) == len(set(items))


class TestLottery(unittest.TestCase):
    def test_01_urn(self):
        items = application.random_urn([1, 2, 3, 4], 3)
        self.failUnless(_are_unique(items))
        items = application.random_urn([1, 2, 3], 3)
        self.failUnless(_are_unique(items))

    def test_02_draw(self):
        lottery = application.Lottery(balance=200, num_tickets=50)
        lottery.sell_ticket("a") # balance: 210
        lottery.sell_ticket("b") # balance: 220
        lottery.sell_ticket("c") # balance: 230
        lottery.sell_ticket("d") # balance: 240
        lottery.sell_ticket("e") # balance: 250
        lottery.sell_ticket("f") # balance: 260
        lottery.sell_ticket("g") # balance: 270
        lottery.sell_ticket("h") # balance: 280
        lottery.sell_ticket("j") # balance: 290
        lottery.sell_ticket("k") # balance: 300
        lottery.sell_ticket("l") # balance: 310
        lottery.sell_ticket("m") # balance: 320

        winners = lottery.draw_winners()
        self.failUnless(_are_unique(winners))

        prices = lottery.get_prices()
        self.failUnlessEqual(prices[0], 120)
        self.failUnlessEqual(prices[1], 24)
        self.failUnlessEqual(prices[2], 16)


if __name__ == '__main__':
    unittest.main()

