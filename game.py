from cards import *
class Player():
    def __init__(self, balance = 1000):
        self.__hand = []
        self.balance = balance
        self.active = True # Whether the player is stil in round (hasn't folded yet).
        self.is_big_blind = False
        self.is_small_blind = False

    def hand(self):
        '''Returns player hand.'''
        return self.__hand

    # Game moves
    def call(self):
        '''Call.'''
        pass

    def check(self):
        '''Check.'''
        pass

    def bet(amount):
        '''Raise.'''
        pass

    def fold(self):  
        '''Fold.'''
        pass

    def rake(self, pot):
        '''Take the pot amount. Player has won.'''
        self.__balance += pot

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.pot = 0
    
    