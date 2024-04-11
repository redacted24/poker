from cards import *

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.pot = 0
        self.state = 0
        self.players = 0
        # 0 : pre-flop
        # 1 : flop
        # 2 : turn
        # 3 : river

    # Functionality
    def increase_pot(self, amount):
        '''Increase pot by certain amount.'''
        self.pot += amount

    def view_state(self):
        '''Prints the cards on the board of the table, as well as the state (pre-flop, flop, turn, or river).'''
        states = ['PRE-FLOP', 'FLOP', 'TURN', 'RIVER']
        print(f'### {states[self.state]} ###')
        if self.state != 0:
            print(f'The current cards on the table are: {self.board}')
            print(f'The current pot is {self.pot}$')

    def burn(self):
        '''Burn top deck card.'''
        self.deck.burn()

    def add_card(self):
        '''Add a card from the top of the deck to the board, and return it'''
        return self.board.append(self.deck.draw())

    def clear_board(self):
        '''Clears the current cards on the board.'''
        self.board.clear()

    # Game Rounds
    def pre_flop(self):
        '''Shuffle deck, then draw pre-flop cards, then return the burnt card.'''
        self.deck.shuffle()
        for i in range(3):
            self.add_card()
        return self.deck.burn()


# -------------------------- #

# -------------------------- #
class Player():
        def __init__(self, name, table, bot=False, balance = 1000):
            self.name = name
            self.table = table # Which table they are at
            self.__hand = []
            self.balance = balance
            self.active = True # Whether the player is stil in round (hasn't folded yet).
            self.bot = bot # Whether the player is a bot (computer) or not
            self.is_big_blind = False
            self.is_small_blind = False
            self.table.players += 1
            self.stats = {
                'bet': 0,
                'raise': 0,
                'call': 0,
                'check': 0,
                'all-in': 0
            }

        # WIP
        @staticmethod
        def handEval(hand):
            '''Compute strength of a certain hand of a certain size.
            Takes in a list of 7 card objects, and returns (int, list) where first int is the hand type and the list is the cards in hand.
            1. Royal Flush
            2. Straight Flush
            3. Four of a Kind
            4. Full House
            5. Flush
            6. Straight
            7. Three of a kind
            8. Two Pair
            9. Pair
            10. High Card'''
                                                    #takes in a list of 7 cards
            '''Check if hand is a flush and whether it's a Royal Flush, a Straight Flush or a regular Flush'''
            hand.sort(reverse = True)                                   #sorts the cards in descending order so the deck can be read from highest value to lowest value                                                #sorts the hand by value initially to have 
            suitHand = sorted(hand, key = lambda x: x. suit)                                     #sorts the hand by suits to check whether there are 5 of the same suits
            for i in range(len(hand) - 2):
                otherHand = hand[i:i+5]
                winningHand = sorted(suitHand[i:i+5], key = lambda x:x.suit)
                if winningHand[0].suit == winningHand[-1].suit:
                    if len(winningHand) >= 5 and all([(winningHand[i].value - winningHand[i+1].value) == 1 for i in range(len(winningHand) - 1)]):      #basic requirement for a Straight Flush or a Royal Flush
                        if int(winningHand[0].value) == 14:
                            return (1, str(winningHand))
                        else:
                            return (2, str(winningHand))
                    elif len(winningHand) >= 5: #regular flush
                        return (5, str(winningHand))
                elif all([(otherHand[i].value - otherHand[i+1].value) == 0 for i in range(len(otherHand) - 1)]):
                    return (3, str(hand[i:i+5]))
                else:
                    pass
            return False

            
            
        def riverEval(self):
            '''Return the highest scoring hand pattern of player + board.'''
            pass

        def look(self):
            '''Prints player hand.'''
            print(f'Your hand is: {str(self.__hand)}')

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
            print('Player checks.')
            pass

        def bet(self, amount):      # Currently working on this
            '''Raise. Also modifies player stats, #times betted + 1'''
            if self.balance - amount < 0:
                print('Not enough chips.')
                raise ValueError

            elif self.balance - amount <= 0:
                print('All-in')
                self.stats['all-in'] += 1       # Increase number of times all-ined
                self.table.increase_pot(self.balance)
                self.balance = 0

            else:
                self.balance -= amount
                self.stats['bet'] += 1      # Increase number of times bet
                self.table.increase_pot(amount)

        def all_in(self):
            'All-in on your balance!'
            self.table.increase_pot(self.balance)
            self.balance = 0

        def fold(self):
            '''Fold.'''
            print('Player has folded')
            self.__hand.clear()
            pass

        def rake(self, pot):
            '''Take the pot amount. Player has won.'''
            self.balance += pot

if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    p1 = Player('Haha', table)

    # Check for flushes
    assert Player.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (5, '[As, Ks, Js, Ts, 9s]')
    assert Player.handEval([deck.get('Ts'), deck.get('Qs'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (1, '[As, Ks, Qs, Js, Ts]')
    assert Player.handEval([deck.get('Ks'), deck.get('9s'), deck.get('9h'), deck.get('9d'), deck.get('9c'), deck.get('Th'), deck.get('Js')]) == (3, '[9s, 9h, 9d, 9c]') 
    assert Player.handEval([deck.get('As'), deck.get('Ks'), deck.get('Qs'), deck.get('Qh'), deck.get('Js'), deck.get('Jh'), deck.get('Ts')])
    print('All tests passed.')

