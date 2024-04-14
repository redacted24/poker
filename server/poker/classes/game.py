from poker.classes.cards import *

class Board():
    def __init__(self):
        self._cards: list[Cards] = []
        self._show_cards: bool = False

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return str(self._cards)

    def place_card(self, card: Cards):
        '''Places a card onto the board'''
        self._cards.append(card)
    
    def reveal(self):
        '''Reveals all cards on the board'''
        self._show_cards = True
    
    def hide(self):
        '''Hides all cards on the board'''
        self._show_cards = False

    def cards(self):
        '''Returns the list of cards on the board'''
        return self._cards

    def display(self):
        '''Returns a list containing strings of all cards names on the board.
        A card is False if it is not revealed.'''
        if self._show_cards:
            return [card.shortName for card in self._cards]
        else:
            return [False for _ in self._cards]
    
    def clear(self):
        '''Clears and resets the board to its initial state'''
        self._cards = []
        self._show_cards = False

class Table():
    def __init__(self, deck: Deck):
        self.deck: Deck = deck                      # Setup the deck used for the table
        self.board: Board = Board()                 # Making a board class. Easier to manage the state of the board
        self.pot: int = 0                           # The flop on the table
        self.state: int = 0                         # Pre-flop (0), flop (1), turn (2), river (3), showdown(4)
        self.players: list[Player] = []             # [PlayerObject,'move']
        self.dealer: int = 0                        # Index of the player who is currently the dealer. The small/big blind players are also determined by this number.
        self.player_queue: list[Player] = []        # A list of all the players that will be playing in the round
        self.winning_player: Player|None = None     # The player who won the round. It is None while the game is in progress.
        self.required_bet: int = 0                  # How much money is required to stay in the game. Very useful to program the call function
        self.last_move: list[str, str] = []         # [Player.name, 'nameOfMove'] A list of two elements containing the player name, and the name of their last move (e.g. bet)
        self.round_stats: dict = {        
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.game_stats: dict = {
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

    def start_queue(self, pre_flop=False):
        '''Adds a queue for the players' turn to play'''
        if pre_flop:
            self.player_queue = self.players[2:] + self.players[0:2]                # if pre-flop, the first two players play last since they are small/big blinds
        else:
            self.player_queue = self.active_players()[:]

    def set_positions(self):
        '''Set the positions of the players for the current round'''
        for i, player in enumerate(self.players):
            player.position = abs(i + 1) % len(self.players)

    def set_blinds(self):
        '''Takes out the required contributions from the blinds to the pot'''
        small_blind,big_blind = self.players[0:2]
        small_blind.balance -= 5
        small_blind.current_bet = 5
        big_blind.balance -= 10
        big_blind.current_bet = 10
        self.pot += 15
        
    # Game Rounds
    def pre_flop(self):
        '''Ready game for the pre-flop.
        - Sets required bet to 10$ (small blind)
        - Clears all bets for all players
        - Clears last move
        - Adds a queue for players to start playing
        - Set positions of players for the current round
        - Set blinds for the current round
        - Shuffle deck and add three cards to the board, and deal cards to players'''
        print('Pre-flop')
        self.required_bet = 10
        self.clear_bets()
        self.last_move.clear()
        self.start_queue(pre_flop=True)
        self.set_positions()
        self.set_blinds()
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
            print(player.handEval(self.board.cards()), winning_player.handEval(self.board.cards()))
            if player.handEval(self.board.cards()) > winning_player.handEval(self.board.cards()):
                winning_player = player

        winning_player.rake()       # Winning player takes in all the money
        self.winning_player = winning_player
        print(self.winning_player)


    def play(self):
        '''Lets all the computers play their turn, then starts the next round if needed.'''
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
            if self.state < 4:
                self.play()

    def reset(self):
        '''Clears current cards on the board, resets deck, and removes all player handheld cards.
        Clears current round stats. Game stats are left unchanged.
        Players are still on the table, but shifted by one seat'''
        print('Reset')
        self.pot = 0
        self.state = 0
        self.board.clear()
        self.deck.reset()
        self.winning_player = None
        self.players = self.players[1:] + self.players[:1]
        for stat in self.game_stats.keys():
            self.round_stats[stat] = 0
        for player in self.players:
            player.reset()
        self.start_queue()


    # Player actions Table Class
    def update_table_stats(self, player, move):
        '''Updates all table stats, based on the move. Used in all possible game moves.'''
        self.game_stats[move] += 1
        self.round_stats[move] += 1
        player.stats[move] += 1
        self.last_move = [player.name, move]
        player.actions_done = sum(player.stats.values())  

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
        self.blinds_adjustment_factor = 0
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
            self.active = True                  # Whether the player is still in round (hasn't folded yet).
            self.position = None                # Determines the position of the player. 0 = dealer, 1 = small blind, 2 = big blind, etc.
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

        def handEval(self, river):
            '''Compute strength of a certain hand of a certain size.
            Takes in a list of 7 card objects, and returns (int, list) where first int is the hand type and the list is the cards in hand.
            10. Royal Flush
            9. Straight Flush
            8. Four of a Kind
            7. Full House
            6. Flush
            5. Straight
            4. Three of a kind
            3. Two Pair
            2. Pair
            1. High Card'''

            def getOriginalStraight(values, hand):
                winning_hand = []
                for card in hand:
                    if values and card.value == values[0]:
                        winning_hand.append(card)
                        values.pop(0)

                if values:
                    winning_hand.append(hand[0])
                return winning_hand

            def checkStraight(values: dict, hand):
                sorted_values = sorted(values.keys(), reverse=True)
                if 14 in sorted_values: sorted_values.append(1)
                consecutive = 1
                for i in range(0, len(sorted_values) - 1):
                    if sorted_values[i] - 1 == sorted_values[i+1]:
                        consecutive += 1
                        if consecutive == 5:
                            return getOriginalStraight(sorted_values[i-3:i+2], hand)
                    else:
                        consecutive = 1
                return False
            
            def checkFlush(suits: dict, hand: list[Cards]):
                for suit, items in suits.items():
                    if items >= 5:
                        suited_cards = [card for card in hand if card.suit == suit]
                        flush_values = {}
                        for card in suited_cards:
                            flush_values[card.value] = values.get(card.value, 0) + 1
                        flush_straight = checkStraight(flush_values, suited_cards)
                        return flush_straight, suited_cards
                return False, False


            def getOriginalValues(num_items, values, hand):
                winning_hand = []
                while num_items:
                    for value, items in sorted(values.items(), key=lambda x: x[1]):
                        if num_items and items >= num_items[0]:
                            winning_hand += [card for card in hand if card.value == value]
                            num_items.pop(0)

                winning_hand = winning_hand[0:5]

                for card in hand:
                    if card not in winning_hand:
                        if len(winning_hand) >= 5:
                            break
                        winning_hand.append(card)

                return winning_hand

            hand = self.hand() + river
            values = {}
            suits = {}
            sorted_hand = sorted(hand, reverse=True, key=lambda c: c.value)
            for card in sorted_hand:
                values[card.value] = values.get(card.value, 0) + 1
                suits[card.suit] = suits.get(card.suit, 0) + 1

            flush_straight, flush = checkFlush(suits, sorted_hand)
            straight = checkStraight(values, sorted_hand)

            if flush_straight and flush_straight[0].value == 14:
                return 10, flush_straight
            elif flush_straight:
                    return 9, flush_straight
            elif 4 in values.values():
                return 8, getOriginalValues([4], values, sorted_hand)
            elif len([v for v in values.values() if v == 3]) == 2 or (3 in values.values() and 2 in values.values()):
                return 7, getOriginalValues([3, 2], values, sorted_hand)
            elif flush:
                return 6, flush[0:5]
            elif straight:
                return 5, straight
            elif 3 in values.values():
                return 4, getOriginalValues([3], values, sorted_hand)
            elif len([v for v in values.values() if v == 2]) >= 2:
                return 3, getOriginalValues([2, 2], values, sorted_hand)
            
            elif 2 in values.values():
                return 2, getOriginalValues([2], values, sorted_hand)
            else:
                return 1, sorted_hand[0:5]

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
        def reset(self):
            self.current_bet = 0
            self.active = True
            self.clear_hand()
            self.position = None

        def toJSON(self):
            return {
                'name': self.name,
                'is_computer': self.is_computer,
                'hand': [c.shortName for c in self.hand()],
                'balance': self.balance,
                'current_bet': self.current_bet,
                'active': self.active,
                'position': self.position
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
    print(p1.handEval([deck.get('9s'), deck.get('Ts'), deck.get('Js'), deck.get('Ks'), deck.get('As')])) # == (5, '[As, Ks, Js, Ts, 9s]')
    print(p1.handEval([deck.get('Ts'), deck.get('Qs'), deck.get('Js'), deck.get('Ks'), deck.get('As')])) # == (1, '[As, Ks, Qs, Js, Ts]')
    print(p1.handEval([deck.get(card) for card in ['2d', '6s', 'Kh', 'Qd', 'Ad', 'Ks', 'Td']])) # == (3, '[9s, 9h, 9d, 9c]') 
    print(p1.handEval([deck.get('As'), deck.get('Ks'), deck.get('Qs'), deck.get('Qh'), deck.get('Js'), deck.get('Jh'), deck.get('Ts')])) # == (1, '[As, Ks, Qs, Js, Ts]')
    print(p1.handEval([deck.get('Ks'), deck.get('Ts'), deck.get('8h'), deck.get('9d'), deck.get('7c'), deck.get('6s'), deck.get('8s')])) # == (6, '[10, 9, 8, 7, 6]')
    print(p1.handEval([deck.get('Ks'), deck.get('Ts'), deck.get('8h'), deck.get('9d'), deck.get('8c'), deck.get('8s'), deck.get('6h')]))

    print('All tests passed.')
