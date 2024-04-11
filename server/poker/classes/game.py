from cards import *

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.pot = 0
<<<<<<< HEAD
        self.state = 0
        self.players = 0
        # 0 : pre-flop
        # 1 : flop
        # 2 : turn
        # 3 : river
=======
        self.state = 0              # Pre-flop (0), flop (1), turn (2), river (3)
        self.players = []           # [PlayerObject,'move']
        self.required_bet = 0       # How much money is required to stay in the game. Very useful to program the call function
        self.last_move = []
        self.round_stats = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.game_stats = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4

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

<<<<<<< HEAD
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
=======
    def reset(self):
        '''Clears current cards on the board, resets deck, and removes all player handheld cards.
        Clears current round stats. Game stats are left unchanged.
        Pot is left unchanged because it should be handled by the player "rake" func.
        Players are still on the table.'''
        self.board.clear()
        self.deck.reset()
        for stat in self.game_stats.keys():
            self.round_stats[stat] = 0
        for player in self.players:
            player.clear_hand()
        print('Table has been cleared.')

    def end(self):
        '''A method that ends the current game. Clears game_stats. Players leave the table. Basically a harder reset than the reset method.'''
        self.reset()
        for player in self.players:
            player.clear_all_stats()
        self.players.clear()
        for stat in self.game_stats.keys():
            self.game_stats[stat] = 0


    # Game Rounds
    def pre_flop(self):
        '''Ready game for the pre-flop.'''
        print('Pre-flop')
        self.deck.shuffle()
        self.current_bet = 0
        self.last_move.clear()
        self.state = 0
        for i in range(3):
            self.add_card()

    def flop(self):
        '''Ready game for the flop.'''
        print('Flop')
        self.current_bet = 0
        self.state = 1
        self.last_move.clear()
        # show flop cards

    def turn(self):
        '''Ready game for the turn.'''
        print('Turn')
        self.current_bet = 0
        self.state = 2
        self.last_move.clear()
        self.add_card()
    
    def river(self):
        '''Ready game for the river.'''
        print('River')
        self.current_bet = 0
        self.state = 3
        self.last_move.clear()
        self.add_card()
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4


# -------------------------- #

# -------------------------- #
class Player():
<<<<<<< HEAD
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
=======
        def __init__(self, name, table, balance = 1000):
            self.name = name
            self.table = table                  # Which table they are at
            self.__hand = []
            self.balance = balance
            self.current_bet = 0                # Balance of the player's bet for the current round
            self.active = True                  # Whether the player is stil in round (hasn't folded yet).
            self.is_big_blind = False
            self.is_small_blind = False
            self.table.players.append(self)     # Add self to the table player list.
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
            self.stats = {
                'bet': 0,
                'raise': 0,
                'call': 0,
                'check': 0,
<<<<<<< HEAD
                'all-in': 0
            }
=======
                'all-in': 0,
                'fold': 0
            }
            self.actions_done = sum(self.stats.values())

            # Important stats for player modeling and computer play
            self.aggro_factor = 0
            self.aggro_frequency = 0
            self.hand_strength = 0              # Hand strength. Mostly used to decide what to do in pre-flop
            self.hand_potential = 0             # Hand potential. Mostly used to decide what to do after cards are revealed. Might take a lot of computational time.
        
        def __repr__(self):
            return self.name
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4

        # WIP
        @staticmethod
        def handEval(hand):
            '''Compute strength of a certain hand of a certain size.
<<<<<<< HEAD
            Takes in a list of 7 card objects, and returns (int, list) where first int is the hand type and the list is the cards in hand.
=======
            Takes in a list of 7 card objects, and returns [int, int] where first int is the hand, last int is the value of the highest card in that hand.
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
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
<<<<<<< HEAD
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

            
            
=======

            def isFlush(hand):                                              #takes in a list of 7 cards
                '''Check if hand is a flush and whether it's a Royal Flush, a Straight Flush or a regular Flush'''
                hand.sort(key=lambda x : x.suit)                            #sorts the hand by suits to check whether there are 5 of the same suits
                for i in range(len(hand) - 5):
                    if hand[i].suit == hand[i+5].suit:                      #this should work
                        return True
                return False

            output = []
            if isFlush(hand):
                output.extend([5,max(hand, key=lambda x : x.value)])        #making a list containing the type of hand and the max value of the player's hand
            return output


>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
        def riverEval(self):
            '''Return the highest scoring hand pattern of player + board.'''
            pass

        def look(self):
            '''Prints player hand.'''
            print(f'Your hand is: {str(self.__hand)}')
<<<<<<< HEAD
=======
        
        def hand(self):
            '''Returns player hand'''
            return self.__hand
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4

        def receive(self, cards):
            '''Receives cards in hand.'''
            if isinstance(cards, list):
                self.__hand.extend(cards)
            else:
                self.__hand.append(cards)

<<<<<<< HEAD
        def clear(self):
            '''Removes all cards held in hand.'''
            self.__hand.clear()
=======
        def clear_hand(self):
            '''Removes all cards held in hand.'''
            self.__hand.clear()
        
        def update_all_stats(self, move:str):
            '''Updates all table stats, based on the move. Used in all possible game moves.'''
            self.table.last_move = [self, move]
            self.table.game_stats[move] += 1
            self.table.round_stats[move] += 1
            self.stats[move] += 1
            self.table.last_move = [self,move]
            self.aggro_factor = 0 if self.stats['call'] == 0 else (self.stats['bet']+self.stats['raise'])/self.stats['call'] # Aggression factor ((bets+raises)/calls   
            self.aggro_frequency = 0 if self.actions_done == 0 else (self.stats['bet']+self.stats['raise'])/(self.stats['call'] + self.stats['bet'] + self.stats['raise'] + self.stats['fold']) # Aggression frequency ([(bets + raises)/(bets + raises + calls + folds)] * 100)
        
        def clear_all_stats(self):
            '''Clears all player stats.'''
            for stat in self.stats.keys():
                self.stats[stat] = 0

>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4

        # Game moves
        def call(self):
            '''Call.'''
<<<<<<< HEAD
=======
            self.update_all_stats('call')
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
            pass

        def check(self):
            '''Check.'''
<<<<<<< HEAD
            print('Player checks.')
            pass

        def bet(self, amount):      # Currently working on this
            '''Raise. Also modifies player stats, #times betted + 1'''
            if self.balance - amount < 0:
=======
            self.update_all_stats('check')
            print(self, 'checks.')
            pass

        def bet(self, amount):      # Currently working on this
            '''Raise. Prints a message stating that the current player has bet a certain amount.
            Also modifies player stats, #times betted + 1'''
            if self.balance <= 0:
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
                print('Not enough chips.')
                raise ValueError

            elif self.balance - amount <= 0:
<<<<<<< HEAD
                print('All-in')
                self.stats['all-in'] += 1       # Increase number of times all-ined
                self.table.increase_pot(self.balance)
                self.balance = 0

            else:
                self.balance -= amount
                self.stats['bet'] += 1      # Increase number of times bet
                self.table.increase_pot(amount)
=======
                self.update_all_stats('all-in')
                self.current_bet += self.balance
                self.all_in()

            else:
                self.current_bet += amount
                self.balance -= amount
                self.table.increase_pot(amount)
                self.update_all_stats('bet')
                print(self, 'bets', str(amount)+'$')
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4

        def all_in(self):
            'All-in on your balance!'
            self.table.increase_pot(self.balance)
<<<<<<< HEAD
            self.balance = 0

        def fold(self):
            '''Fold.'''
            print('Player has folded')
            self.__hand.clear()
=======
            self.update_all_stats('all-in')
            self.balance = 0
            print(self,'goes all-in.')

        def fold(self):
            '''Fold.'''
            self.update_all_stats('fold')
            self.__hand.clear()
            print('Player has folded')
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
            pass

        def rake(self, pot):
            '''Take the pot amount. Player has won.'''
            self.balance += pot

if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    p1 = Player('Haha', table)

    # Check for flushes
<<<<<<< HEAD
    assert Player.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (5, '[As, Ks, Js, Ts, 9s]')
    assert Player.handEval([deck.get('Ts'), deck.get('Qs'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (1, '[As, Ks, Qs, Js, Ts]')
    assert Player.handEval([deck.get('Ks'), deck.get('9s'), deck.get('9h'), deck.get('9d'), deck.get('9c'), deck.get('Th'), deck.get('Js')]) == (3, '[9s, 9h, 9d, 9c]') 
    assert Player.handEval([deck.get('As'), deck.get('Ks'), deck.get('Qs'), deck.get('Qh'), deck.get('Js'), deck.get('Jh'), deck.get('Ts')])
    print('All tests passed.')

=======
    assert Player.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == [5, 14]
    assert not Player.handEval([deck.get('9d'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == []



    print('All tests passed.')
>>>>>>> d85c322574d15987dd4099ccf775162539e9d8b4
