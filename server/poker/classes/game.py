from poker.classes.cards import *

class Table():
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.pot = 0
        self.state = 0              # Pre-flop (0), flop (1), turn (2), river (3)
        self.players = []           # [PlayerObject,'move']
        self.player_queue = []
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

    # Functionality
    def increase_pot(self, amount):
        '''Increase pot by certain amount.'''
        self.pot += amount

    def burn(self):
        '''Burn top deck card.'''
        self.deck.burn()

    def add_card(self):
        '''Add a card from the top of the deck to the board, and return it'''
        return self.board.append(self.deck.draw())
    
    def deal_hands(self):
        '''Deal two cards to all players in the table'''
        for p in self.players:
            p.receive(self.deck.draw())
            p.receive(self.deck.draw())
            self.deck.burn()


    # Game Rounds
    def pre_flop(self):
        '''Ready game for the pre-flop.'''
        print('Pre-flop')
        self.required_bet = 10
        self.last_move.clear()
        self.player_queue = self.players[:]

        self.deck.shuffle()
        self.deal_hands()
        for _ in range(3):
            self.add_card()

    def flop(self):
        '''Ready game for the flop.'''
        print('Flop')
        self.required_bet = 0
        self.last_move.clear()
        self.player_queue = self.players[:]
        # show flop cards

    def turn(self):
        '''Ready game for the turn.'''
        print('Turn')
        self.required_bet = 0
        self.last_move.clear()
        self.player_queue = self.players[:]
        self.add_card()
    
    def river(self):
        '''Ready game for the river.'''
        print('River')
        self.required_bet = 0
        self.last_move.clear()
        self.player_queue = self.players[:]
        self.add_card()

    def play(self):
        '''Lets all the computers play their turn, then starts the next round.'''
        while len(self.player_queue) != 0:
            if (self.player_queue[0].is_computer):
                current_player = self.player_queue.pop(0)
                current_player.play()
            else:
                break
        
        if len(self.player_queue) == 0:
            self.state = (self.state + 1) % 4
            rounds = [self.pre_flop, self.flop, self.turn, self.river]
            
            rounds[self.state]()


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


    # Player actions
    def update_table_stats(self, player, move):
        '''Updates all table stats, based on the move. Used in all possible game moves.'''
        self.game_stats[move] += 1
        self.round_stats[move] += 1
        player.stats[move] += 1
        self.last_move = [self,move]

    def call(self, player):
        '''Player calls, matching the current bet.'''
        if player == self.player_queue[0]:
            player.balance -= self.required_bet
            self.pot += self.required_bet
            self.update_table_stats(player, 'call')
            self.player_queue.pop(0)
        else:
            raise(ValueError, 'Not your turn yet!')

    # def check(self):
    #     '''Check.'''
    #     self.update_table_stats('check')
    #     print(self, 'checks.')
    #     pass

    #     def bet(self, amount):      # Currently working on this
    #         '''Raise. Prints a message stating that the current player has bet a certain amount.
    #         Also modifies player stats, #times betted + 1'''
    #         if self.balance <= 0:
    #             print('Not enough chips.')
    #             raise ValueError

    #         elif self.balance - amount <= 0:
    #             self.update_table_stats('all-in')
    #             self.current_bet += self.balance
    #             self.all_in()

    #         else:
    #             self.current_bet += amount
    #             self.balance -= amount
    #             self.table.increase_pot(amount)
    #             self.update_table_stats('bet')
    #             print(self, 'bets', str(amount)+'$')

    #     def all_in(self):
    #         'All-in on your balance!'
    #         self.table.increase_pot(self.balance)
    #         self.balance = 0
    #         print(self,'goes all-in.')

    #     def fold(self):
    #         '''Fold.'''
    #         self.stats['fold'] += 1
    #         self.table.round_stats['fold'] += 1    # Increase number of times folds for round stats
    #         self.table.game_stats['fold'] += 1
    #         self.__hand.clear()
    #         print('Player has folded')
    #         pass

    #     def rake(self, pot):
    #         '''Take the pot amount. Player has won.'''
    #         self.balance += pot
        


    # Misc
    def add_player(self, player):
        self.players.append(player)
        player.join(self)

    def view_state(self):
        '''Prints the cards on the board of the table, as well as the state (pre-flop, flop, turn, or river).'''
        states = ['PRE-FLOP', 'FLOP', 'TURN', 'RIVER']
        print(f'### {states[self.state]} ###')
        if self.state != 0:
            print(f'The current cards on the table are: {self.board}')
            print(f'The current pot is {self.pot}$')

    def end(self):
        '''A method that ends the current game. Clears game_stats. Players leave the table. Basically a harder reset than the reset method.'''
        self.reset()
        self.players.clear()
        for stat in self.game_stats.keys():
            self.game_stats[stat] = 0

# -------------------------- #

# -------------------------- #
class Player():
        def __init__(self, name, is_computer, balance = 1000):
            self.name = name
            self.is_computer = is_computer
            self.table: Table | None = None
            self.__hand = []
            self.balance = balance
            self.current_bet = 0                # Balance of the player's bet for the current round
            self.active = True                  # Whether the player is stil in round (hasn't folded yet).
            self.is_big_blind = False
            self.is_small_blind = False
            self.stats = {
                'bet': 0,
                'raise': 0,
                'call': 0,
                'check': 0,
                'all-in': 0,
                'fold': 0
            }
        
        def __repr__(self):
            return self.name
        
        def join(self, table: Table):
            self.table = table

        # WIP
        @staticmethod
        def handEval(hand):
            '''Compute strength of a certain hand of a certain size.
            Takes in a list of 7 card objects, and returns [int, int] where first int is the hand, last int is the value of the highest card in that hand.
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


        def riverEval(self):
            '''Return the highest scoring hand pattern of player + board.'''
            pass

        def look(self):
            '''Prints player hand.'''
            print(f'Your hand is: {str(self.__hand)}')
        
        def hand(self):
            '''Returns player hand'''
            return self.__hand

        def receive(self, cards):
            '''Receives cards in hand.'''
            if isinstance(cards, list):
                self.__hand.extend(cards)
            else:
                self.__hand.append(cards)

        def clear_hand(self):
            '''Removes all cards held in hand.'''
            self.__hand.clear()
        

        # Player moves
        def call(self):
            if self.balance >= self.table.required_bet:
                self.table.call(self)



if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    p1 = Player('Haha', table)

    # Check for flushes
    assert Player.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == [5, 14]
    assert not Player.handEval([deck.get('9d'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == []



    print('All tests passed.')