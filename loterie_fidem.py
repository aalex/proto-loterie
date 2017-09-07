#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Loterie Fidem.
"""

import argparse
import random
import shlex


class Lottery(object):
    """
    Lottery with a given number of tickets.
    """
    def __init__(self, name="Fidem", balance=200, num_tickets=50):
        """
        @param name Name of the lottery.
        @param balance How much money there is to win; total.
        @param num_tickets How many tickets there are.
        """
        self._name = name
        self._balance = balance
        self._tickets = []
        self._next_to_be_sold = 0
        self._winners = [-1, -1, -1]
        if num_tickets < 3:
            raise RuntimeError("There must be a minimum of 3 tickets")
        for i in range(num_tickets):
            self._tickets.append("")
        random.seed()

    def sell_ticket(self, first_name):
        """
        Sells a ticket.
        @return Index of the ticket sold.
        @rtype C{int}
        @raise L{RuntimeError} If name is not empty of there are no tickets left."
        """
        if first_name == "":
            raise RuntimeError("First name must not be empty")
        if self.has_tickets_left():
            self._tickets[self._next_to_be_sold] = first_name
            ret = self._next_to_be_sold
            self._next_to_be_sold += 1
            return ret
        else:
            raise RuntimeError("There are no tickets left")

    def has_tickets_left(self):
        """
        Checks if there is at least one ticket left.
        @rtype C{bool}
        """
        return self._next_to_be_sold < len(self._tickets)

    def draw_winners(self):
        if -1 not in self._winners:
            raise RuntimeError("The winners were already drawn")
        for i in range(len(self._winners)):
            index = -2
            while index not in self._winners:
                index = random.randint(0, len(self._tickets) - 1)
                if index not in self._winners:
                    self._winners[i] = index
        return self._winners
    
    def get_prizes_values(self):
        values = [
            int(self._balance * 0.75),
            int(self._balance * 0.15),
            int(self._balance * 0.10),
            ]
        return values
    
    def format_winners_table(self):
        if -1 in self._winners:
            raise RuntimeError("We don't know the winners, yet.")
        return """
        +------------------+-------------------+--------------------+
        | 1ère boule       | 2ième boule       | 3ième boule        |
        +------------------+-------------------+--------------------+
        | %{name1}         | %{name2}          | %{name3}           |
        +------------------+-------------------+--------------------+
        """.format(
                name1=self._tickets[self._winners[0],
                name2=self._tickets[self._winners[1],
                name3=self._tickets[self._winners[2]
                )



class Application(object):
    def __init__(self):
        self._lottery = Lottery()

    def achat(self):

    def tirage(self):

    def gagnants(self):
        print(self._lottery.format_winners_table())

if __name__ == '__main__':
    
