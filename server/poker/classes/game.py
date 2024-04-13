from poker.classes.cards import *

class Board():
    def __init__(self):
        self.cards: list[Cards] = []
        self._show_cards: bool = False

    def __len__(self):
        return len(self.cards)

    def place_card(self, card: Cards):
        '''Places a card onto the board'''
        self.cards.append(card)
    
    def reveal(self):
        '''Reveals all cards on the board'''
        self._show_cards = True
    
    def hide(self):
        '''Hides all cards on the board'''
        self._show_cards = False

    def display(self):
        '''Returns a list containing strings of all cards names on the board.
        A card is False if it is not revealed.'''
        if self._show_cards:
            return [card.shortName for card in self.cards]
        else:
            return [False for _ in self.cards]
    
    def clear(self):
        '''Clears and resets the board to its initial state'''
        self.cards = []
        self._show_cards = False

class Table():
    def __init__(self, deck):
        self.deck = deck            # Setup the deck used for the table
        self.board = Board()        # Making a board class. Easier to manage the state of the board
        self.pot = 0                # The flop on the table
        self.state = 0              # Pre-flop (0), flop (1), turn (2), river (3), showdown(4)
        self.players = []           # [PlayerObject,'move']
        self.player_queue = []      # A list of all the players that will be playing in the round
        self.winning_player = None  # The player who won the round
        self.required_bet = 0       # How much money is required to stay in the game. Very useful to program the call function
        self.last_move = []         # [Player.name, 'nameOfMove'] A list of two elements, where the first is the playername as a string, and the second is the name of the move (e.g. bet) as a string
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
        '''Add a card from the top of the deck to the board'''
        self.board.place_card(self.deck.draw())
    
    def deal_hands(self):
        '''Deal two cards to all players in the table'''
        for p in self.players:
            p.receive(self.deck.draw())
            p.receive(self.deck.draw())
            self.deck.burn()

    def clear_bets(self):
        for p in self.active_players():
            p.current_bet = 0

    def active_players(self):
        '''Returns a list of the active players in the round'''
        return [p for p in self.players if p.active]

    def start_queue(self):
        '''Adds a queue for the players' turn to play'''
        self.player_queue = self.active_players()[:]

        
    # Game Rounds
    def pre_flop(self):
        '''Ready game for the pre-flop.
        - Sets required bet to 10$ (small blind)
        - Clears all bets for all players
        - Clears last move
        - Start the queue again for all players
        - Shuffle deck and add three cards to the board'''
        print('Pre-flop')
        self.required_bet = 10
        self.clear_bets()
        self.last_move.clear()
        self.start_queue()

        self.deck.shuffle()
        self.deal_hands()
        for _ in range(3):
            self.add_card()

    def flop(self):
        '''Ready game for the flop.
        - Sets required bet to 0$
        - Clears all bets for all players
        - Clears last move
        - Starts the queue again for all players
        - Reveal cards on the board'''

        print('Flop')
        self.required_bet = 0
        self.clear_bets()
        self.last_move.clear()
        self.start_queue()
        self.board.reveal()

    def turn(self):
        '''Ready game for the turn.
        - Sets required bet to 0
        - Clears all bets for all players
        - Clears last move
        - Start the queue again for all players
        - Adds a card to the board.'''
        print('Turn')
        self.required_bet = 0
        self.clear_bets()
        self.last_move.clear()
        self.start_queue()
        self.add_card()
    
    def river(self):
        '''Ready game for the river.
        - Sets required bet to 0
        - Clears all bets for all players
        - Clears last move
        - Start the queue again for all players
        - Adds a card to the board.'''
        print('River')
        self.required_bet = 0
        self.clear_bets()
        self.last_move.clear()
        self.start_queue()
        self.add_card()

    def showdown(self):
        '''Checks who will win.'''
        print('Showdown')
        winning_player = self.active_players()[0]

        for player in self.active_players():
            if player.pts() > winning_player.pts():
                winning_player = player

        winning_player.rake()       # Winning player takes in all the money
        self.winning_player = winning_player


    def play(self):
        '''Lets all the computers play their turn, then starts the next round.'''
        while len(self.player_queue) != 0:
            current_player = self.player_queue[0]
            if (current_player.is_computer):
                current_player.play()
            else:
                break
        
        if len(self.player_queue) == 0:
            self.state = (self.state + 1) % 6
            rounds = [self.pre_flop, self.flop, self.turn, self.river, self.showdown, self.reset]
            
            rounds[self.state]()

    def reset(self):
        '''Clears current cards on the board, resets deck, and removes all player handheld cards.
        Clears current round stats. Game stats are left unchanged.
        Pot is left unchanged because it should be handled by the player "rake" func.
        Players are still on the table.'''
        print('Reset')
        self.pot = 0
        self.state = 0
        self.board.clear()
        self.deck.reset()
        self.start_queue()
        self.clear_bets()
        self.winning_player = None
        for stat in self.game_stats.keys():
            self.round_stats[stat] = 0
        for player in self.players:
            player.active = True
            player.clear_hand()


    # Player actions Table Class
    def update_table_stats(self, player, move):
        '''Updates all table stats, based on the move. Used in all possible game moves.'''
        self.game_stats[move] += 1
        self.round_stats[move] += 1
        player.stats[move] += 1
        self.last_move = [player.name, move]
        player.actions_done = sum(player.stats.values())
        # player.aggro_factor = 0 if player.stats['call'] == 0 else (player.stats['bet']+player.stats['raise'])/player.stats['call'] # Aggression factor ((bets+raises)/calls   
        # player.aggro_frequency = 0 if player.actions_done == 0 else (player.stats['bet']+player.stats['raise'])/(player.stats['call'] + player.stats['bet'] + player.stats['raise'] + player.stats['fold']) # Aggression frequency ([(bets + raises)/(bets + raises + calls + folds)] * 100)
        

    def call(self, player):
        '''Player calls, matching the current bet.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'call')
            player.balance -= self.required_bet
            self.pot += self.required_bet
            self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))

    def check(self, player):
        '''Player checks, passing the turn without betting.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'check')
            self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))

    def fold(self, player):
        '''Player folds, giving up their hand.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'fold')
            self.player_queue.pop(0)
            if len(self.active_players()) == 1:
                self.player_queue.clear()
                self.state = 4
                self.showdown()
        else:
            raise(ValueError('Not your turn yet!'))     # ValueError is accounted for in tests, i.e. its appearance is checked for several testCases. You may decide to use another way of handling error, we'll just need to also change the test file.

    def bet(self, player, amount):
        '''Player bets, raising the required bet to stay in for the entire table.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'bet')
            player.balance -= amount
            player.current_bet += amount
            self.increase_pot(amount)
            self.required_bet = amount
            self.player_queue.extend([p for p in self.players if p not in self.player_queue])
            self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))

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

    def toJSON(self):
        return {
            'board': self.board.display(),
            'pot': self.pot,
            'players': [p.toJSON() for p in self.players],
            'player_queue': [p.toJSON() for p in self.player_queue],
            'required_bet': self.required_bet,
            'last_move': self.last_move,
            'winning_player': self.winning_player and self.winning_player.toJSON()
        }

    def end(self):
        '''A method that ends the current game. Clears game_stats. Players leave the table. Basically a harder reset than the reset method.'''
        self.reset()
        self.players.clear()
        for stat in self.game_stats.keys():
            self.game_stats[stat] = 0

# -------------------------- #

# -------------------------- #
class Player():
        def __init__(self, name, is_computer, table=None, balance = 1000):
            '''
            - name: player name (str)
            - is_computer: is the player a computer or not? (bool) 
            - table: which table is the player sat on (object) 
            - balance: how much money does the player begin with (int)'''
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
            self.actions_done = 0
            
            # Important stats for player modeling and computer play
            self.aggro_factor = 0
            self.aggro_frequency = 0
            self.hand_strength = 0              # Hand strength. Mostly used to decide what to do in pre-flop
            self.hand_potential = 0             # Hand potential. Mostly used to decide what to do after cards are revealed. Might take a lot of computational time.

            if table:
                table.add_player(self)              # Add player to table
        
        def __repr__(self):
            return self.name
        
        def join(self, table: Table):
            self.table = table

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
                x = {i.value for i in hand[i:]}
                straightHand = sorted(x, reverse = True)
                winningHand = sorted(suitHand[i:i+5], key = lambda x:x.suit)
                if winningHand[0].suit == winningHand[-1].suit:
                    if len(winningHand) >= 5 and all([(winningHand[i].value - winningHand[i+1].value) == 1 for i in range(len(winningHand) - 1)]):      #basic requirement for a Straight Flush or a Royal Flush
                        if int(winningHand[0].value) == 14:
                            return (1, str(winningHand))
                        else:
                            return (2, str(winningHand))
                    elif len(winningHand) >= 5: #regular flush
                        return (5, str(winningHand))
                elif all([(otherHand[i].value - otherHand[i+1].value) == 0 for i in range(len(otherHand) - 2)]):
                    return (3, str(hand[i:i+4]))
                elif (not 14 in straightHand) and len(straightHand) == 5 and all([(straightHand[i] - straightHand[i+1]) == 1 for i in range(len(straightHand) - 1)]):
                    return (6, str(straightHand))
                elif all([(otherHand[i].value - otherHand[i+1].value) == 0 for i in range(len(otherHand) - 3)]):
                    return (7, str(hand[i:i+3]))

            return False

        def riverEval(self):
            '''Return the highest scoring hand pattern of player + board.'''
            pass

        def pts(self):
            from random import randint

            return randint(1, 100)

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
                self.current_bet = self.table.required_bet
                self.table.call(self)

        def check(self):
            self.table.check(self)
        
        def fold(self):
            self.active = False
            self.table.fold(self)

        def bet(self, amount):
            if self.balance >= amount:
                self.table.bet(self, amount)

        def rake(self):
            self.balance += self.table.pot


        # Misc
        def toJSON(self):
            return {
                'name': self.name,
                'is_computer': self.is_computer,
                'hand': [c.shortName for c in self.hand()],
                'balance': self.balance,
                'current_bet': self.current_bet,
                'active': self.active,
                'is_big_blind': self.is_big_blind,
                'is_small_blind': self.is_small_blind,
            }

        def clear_all_stats(self):
            '''Clears all player stats.'''
            for stat in self.stats.keys():
                self.stats[stat] = 0


if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    p1 = Player('Haha', table)

    # Check for flushes
    assert Player.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (5, '[As, Ks, Js, Ts, 9s]')
    assert Player.handEval([deck.get('Ts'), deck.get('Qs'), deck.get('Js'), deck.get('Ks'), deck.get('As')]) == (1, '[As, Ks, Qs, Js, Ts]')
    assert Player.handEval([deck.get('Ks'), deck.get('9s'), deck.get('9h'), deck.get('9d'), deck.get('9c'), deck.get('Th'), deck.get('Js')]) == (3, '[9s, 9h, 9d, 9c]') 
    assert Player.handEval([deck.get('As'), deck.get('Ks'), deck.get('Qs'), deck.get('Qh'), deck.get('Js'), deck.get('Jh'), deck.get('Ts')]) == (1, '[As, Ks, Qs, Js, Ts]')
    assert Player.handEval([deck.get('Ks'), deck.get('Ts'), deck.get('8h'), deck.get('9d'), deck.get('7c'), deck.get('6s'), deck.get('8s')]) == (6, '[10, 9, 8, 7, 6]')
    assert Player.handEval([deck.get('Ks'), deck.get('Ts'), deck.get('8h'), deck.get('9d'), deck.get('8c'), deck.get('8s'), deck.get('6h')])

    print('All tests passed.')
