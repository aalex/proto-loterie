#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Loterie Fidem.

Voir le document papier pour la documentation.
"""
# TODO: internationalization with gettext
# TODO: handle decimals with decimal
# XXX: exception messages are in English, since they should always be catched
# TODO: there could be a lot of improvements in the software architecture
#       in case we want to add a lot more commands.
# TODO: constants or config options for the price of the tickets, etc.

try:
    import readline # for history
except ImportError:
    pass # This module is not mandatory
import random
import shlex # shell-like lexical parser to split tokens
import copy


NUM_WINNERS = 3


def random_urn(items, num):
    """
    Draws a series of numbers from a list
    """
    ret = []
    if len(items) < num:
        raise RuntimeError("Not enought items in the list")
    _items = copy.deepcopy(items)
    for i in range(num):
        index = random.randint(0, len(_items) - 1)
        ret.append(_items[index])
        del _items[index]
    return ret


class Lottery(object):
    """
    Lottery with a given number of tickets.
    """
    def __init__(self, balance=200, num_tickets=50):
        """
        @param balance How much money there is to win; total.
        @param num_tickets How many tickets there are.
        """
        self._balance = balance
        self._tickets = []
        self._next_to_be_sold = 0
        self._winners = [-1, -1, -1] # indices (-1 means not drawn yet)
        self._prices = [0, 0, 0] # how much they won
        self._num_tickets = num_tickets
        if num_tickets < 3:
            raise RuntimeError("There must be a minimum of 3 tickets")
        self.reset_lottery()

    def get_balance(self):
        return self._balance

    def sell_ticket(self, first_name):
        """
        Sells a ticket.
        @return Number of the ticket sold.
        @rtype C{int}
        @raise L{RuntimeError} If first_name is empty of there are no tickets left."
        """
        if first_name == "":
            raise RuntimeError("First name is empty. You must provide a first name.")
        if self.has_tickets_left():
            self._tickets[self._next_to_be_sold] = first_name
            ret = self._next_to_be_sold + 1 # Tickets are numbered from 1 to N
            self._next_to_be_sold += 1
            self._balance += 10 # each ticket costs 10$. We add that to the balance
            return ret
        else:
            raise RuntimeError("There are no tickets left")

    def has_tickets_left(self):
        """
        Checks if there is at least one ticket left.
        @rtype C{bool}
        """
        return self._next_to_be_sold < len(self._tickets)
    
    def is_draw_done(self):
        if -1 in self._winners:
            return False
        else:
            return True

    def draw_winners(self):
        if self.is_draw_done():
            raise RuntimeError("The winners were already drawn")
        num_sold = self.get_num_tickets_sold()
        if num_sold < NUM_WINNERS:
            raise RuntimeError("There must be at least 3 tickets sold.")

        candidates = [] # list of indices
        for i in range(len(self._tickets)):
            if self._tickets[i] == "":
                break
            else:
                candidates.append(i)
        self._winners = random_urn(candidates, NUM_WINNERS)
        self._prices = self._get_prizes_values()
        self._balance -= sum(self._prices)
        return self._winners

    def get_num_tickets_sold(self):
        num_tickets_sold = 0
        for i in range(len(self._tickets)):
            if self._tickets[i] != "":
                num_tickets_sold += 1
        return num_tickets_sold

    def has_minimum_amount_of_tickets_sold(self):
        return self.get_num_tickets_sold() >= NUM_WINNERS

    def reset_lottery(self):
        """
        Resets the tickets, but keep the money balance.
        """
        self._tickets = []
        self._next_to_be_sold = 0
        for i in range(self._num_tickets):
            self._tickets.append("")

    def reset_random_seed(self):
        random.seed()
    
    def _get_prizes_values(self):
        values = [
            # FIXME: use decimal for accurate money calculations
            int(self._balance * 0.75 * 0.5),
            int(self._balance * 0.15 * 0.5),
            int(self._balance * 0.10 * 0.5),
            ]
        return values
    
    def format_winners_table(self):
        if -1 in self._winners:
            raise RuntimeError("We don't know the winners, yet.")
        return """
        +------------------+------------------+------------------+
        | 1ère boule       | 2ième boule      | 3ième boule      |
        +------------------+------------------+------------------+
        | %16s | %16s | %16s |
        +------------------+------------------+------------------+
        """ % (self._tickets[self._winners[0]],
                self._tickets[self._winners[1]],
                self._tickets[self._winners[2]])

    def get_prices(self):
        return self._prices

    def get_winner_indices(self):
        self._winners


class Application(object):
    def __init__(self):
        self._lottery = Lottery()

    def do_achat(self, first_name):
        ticket_number = self._lottery.sell_ticket(first_name)

    def do_tirage(self):
        if self._lottery.is_draw_done():
            print("Le tirage a déjà été effectué. Veuillez réinitialiser la loterie.")
            print("La commande pour le faire est \"%s\"" % ("réinitialiser"))
        else:
            if self._lottery.has_minimum_amount_of_tickets_sold():
                winners = self._lottery.draw_winners()
                for i in range(len(winners)):
                    winners[i] = winners[i] + 1
                print("Les gagnants sont %s" % (winners))
                prices = self._lottery.get_prices()
                print("Les valeurs des prix sont %s" % (prices))
            else:
                num = self._lottery.get_num_tickets_sold()
                print("Seulement %d billets ont été vendus" % (num))

    def do_gagnants(self):
        if self._lottery.is_draw_done():
            print(self._lottery.format_winners_table())
        else:
            print("Le tirage n'a pas encore été effectué.")
            print("La commande pour le faire est \"%s\"" % ("tirage"))

    def do_reinitialiser(self):
        self._lottery.reset_lottery()

    def do_solde(self):
        balance = self._lottery.get_balance()
        print("Le solde actuel est de %d $" % (balance))

    def do_prix(self):
        prices = self.get_prices()
        print("Les prix sont de %d, %d et %d $" % (
            prices[0], prices[1], prices[2]))

    def do_aide(self):
        usage = """
        Commandes disponibles:
        - aide - afficher ce menu
        - réinitialiser - remettre les billets dans l'urne
        - tirage - 
        - achat <prénom>
        - gagnants
        - solde
        - prix
        - quitter
        """
        print(usage)

    def run(self):
        is_wanting_to_quit = False
        while not is_wanting_to_quit:
            user_input = ""
            try:
                user_input = raw_input("%s:) " % ("Fidem"))
            except KeyboardInterrupt:
                is_wanting_to_quit = True
            except EOFError:
                is_wanting_to_quit = True
            else:
                tokens = shlex.split(user_input)
                try:
                    command = tokens[0]
                except IndexError:
                    print("Impossible d'exécuter la commande désirée.")
                    self._print_usage()

                if command == 'quitter':
                    print("Au revoir")
                    is_wanting_to_quit = True
                elif command == 'aide':
                    self.do_aide()
                elif command == 'réinitialiser':
                    self.do_reinitialiser()
                elif command == 'tirage':
                    self.do_tirage()
                elif command == 'solde':
                    self.do_solde()
                elif command == 'prix':
                    self.do_prix()
                elif command == 'achat':
                    first_name = ""
                    try:
                        first_name = tokens[1]
                    except IndexError:
                        print("Erreur : Vous devez fournir un prénom")
                        print("Usage :  achat <prénom>")
                    else:
                        self.do_achat(first_name)
                elif command == "gagnants":
                    self.do_gagnants()
                else:
                    print("Commande inconnue : \"%s\"" % (command))


if __name__ == '__main__':
    app = Application()
    app.run()

