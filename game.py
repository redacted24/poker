from cards import *

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.pot = 0
        self.state = 0 
        # 0 : pre-flop
        # 1 : flop
        # 2 : turn
        # 3 : river
    
    def __repr__(self):
        '''Prints the cards on the board of the table'''
        return str(self.board)

    def deal(self):
        '''Deal cards to player'''
        pass
    
    def pre_flop(self):
        '''Shuffle deck, then draw pre-flop cards, then return the burnt card.'''
        self.deck.shuffle()
        for i in range(3):
            self.board.append(self.deck.draw())
        return self.deck.burn()
    
    def increase_pot(self, amount):
        '''Increase pot by certain amount.'''
        self.pot += amount
    
    def add_board(self, cards):
        '''Add cards on the board.'''
        if isinstance(cards, list):
            self.board.extend(cards)
        else:
            self.board.append(cards)
    
    def clear_board(self):
        '''Clears the current cards on the board.'''
        self.board.clear()

class Player():
        def __init__(self, name, table, balance = 1000):
            self.name = name
            self.table = table # Which table they are at
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

        def bet(self, amount): # Currently working on this
            '''Raise.'''
            if self.balance - amount < 0:
                print('Not enough chips.')
                raise ValueError

            elif self.balance - amount == 0:
                self.balance -= amount
                print('All-in')
                self.table.increase_pot(amount)

            else:
                self.balance -= amount
                self.table.increase_pot(amount)

        def fold(self):  
            '''Fold.'''
            pass

        def rake(self, pot):
            '''Take the pot amount. Player has won.'''
            self.balance += pot
