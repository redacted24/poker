from cards import *

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.pot = 0
    
    def increase_pot(self, amount):
        '''Increase pot by certain amount.'''
        self.pot += amount

class Player(Table):
        def __init__(self, name, balance = 1000):
            self.name = name
            self.__hand = []
            self.balance = balance
            self.active = True # Whether the player is stil in round (hasn't folded yet).
            self.is_big_blind = False
            self.is_small_blind = False

        def hand(self):
            '''Returns player hand.'''
            return self.__hand
        
        def receive(self, cards):
            '''Receives cards in hand.'''
            if isinstance(cards, list):
                self.__hand.extend(cards)
            else:
                self.__hand.append(cards)
                
        def clear(self):
            '''Removes all cards held in hand.'''
            self.__hand.clear()

        # Game moves
        def call(self):
            '''Call.'''
            pass

        def check(self):
            '''Check.'''
            pass

        def bet(self, amount):
            '''Raise.'''
            if self.balance - amount < 0:
                print('Not enough chips.')

            elif self.balance - amount == 0:
                self.balance -= amount
                print('All-in')
                Table.increase_pot(Table, amount)

            
            else:
                self.balance -= amount
                Table.increase_pot(Table, amount)


        def fold(self):  
            '''Fold.'''
            pass

        def rake(self, pot):
            '''Take the pot amount. Player has won.'''
            self.balance += pot
