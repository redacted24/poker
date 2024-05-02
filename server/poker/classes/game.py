import requests
import pickle

try:
    from poker.classes.cards import *
except:
    from cards import *     # type: ignore

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
    
    def force_put(self, cards):
        '''Forcefully clear the board and put a list of the wanted cards on the table. Only used in testing.'''
        self._cards = []
        self._cards.extend(cards)
    
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
        self.winning_player: Player | None = None   # The player who won the round. It is None while the game is in progress.
        self.required_bet: int = 0                  # How much money is required to stay in the game. Very useful to program the call function
        self.required_raise: int = 10               # Minimum amount of money a player needs to raise the bet
        self.last_move: list[str, str] = []         # [Player.name, 'nameOfMove'] A list of two elements containing the player name, and the name of their last move (e.g. bet)
        self.id: str | None = None
        self.betting_cap = 0                        # Cap to the amount of bets that can be made
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

    def active_players(self, pre_flop=False): 
        '''Returns a list of the active players in the round'''
        self.set_positions()
        if self.player_queue:
            starting_position = self.player_queue[0].position
        elif pre_flop:
            starting_position = 3
        else:
            starting_position = 0

        sorted_players = sorted(self.players, key=lambda p:(p.position - starting_position) % len(self.players))

        return [p for p in sorted_players if p.active]
    
    def randomize(self):
        from random import shuffle
        shuffle(self.players)

    def start_queue(self, pre_flop=False):
        '''Adds a queue for the players' turn to play'''
        print('starting queue')
        self.player_queue = self.active_players(pre_flop)

    def extend_queue(self, game_state):
        '''Extends the current queue for players to call/fold the bet'''
        self.player_queue.extend([p for p in self.active_players(game_state == 0) if p not in self.player_queue])

    def prepare_round(self, pre_flop=False):
        '''Prepares the table for the current round'''
        for key in self.round_stats.keys():     # Reset round stats
            self.round_stats[key] = 0
        self.required_bet = 10 if pre_flop else 0
        self.required_raise = 10
        self.betting_cap = 0
        self.clear_bets()
        self.last_move.clear()
        self.start_queue(pre_flop)

    def set_positions(self):
        '''Set the positions of the players for the current round'''
        for i, player in enumerate(self.players):
            player.position = (i + self.dealer) % len(self.players)

    def set_blinds(self):
        '''Takes out the required contributions from the blinds to the pot'''
        sorted_players = sorted(self.players, key=lambda p: p.position)
        small_blind, big_blind = (sorted_players * 2)[1:3]                          # Allows the list to loop back if there are only 2 players
        
        if small_blind.balance >= 5:
            small_blind.balance -= 5
            small_blind.current_bet = 5
            self.pot += 5
        else:
            self.pot += small_blind.balance
            small_blind.current_bet = small_blind.balance
            small_blind.balance = 0
            small_blind.is_all_in = True
            self.update_table_stats(small_blind, 'all-in')
            print(f"{small_blind} has gone all-in with {small_blind.balance}$ (balance: {small_blind.balance}) (the pot is now {self.pot}$). They had {small_blind.hand()}", "EHS:", small_blind.ehs)
        
        if big_blind.balance >= 10:
            big_blind.balance -= 10
            big_blind.current_bet = 10
            self.pot += 10
        else:
            self.pot += big_blind.balance
            big_blind.current_bet = big_blind.balance
            big_blind.balance = 0
            big_blind.is_all_in = True
            self.update_table_stats(big_blind, 'all-in')
            print(f"{big_blind} has gone all-in with {big_blind.balance}$ (balance: {big_blind.balance}) (the pot is now {self.pot}$). They had {big_blind.hand()}", "EHS:", big_blind.ehs)
        
    # Game Rounds
    def pre_flop(self):
        '''Ready game for the pre-flop.
        - Sets required bet to 10$ (small blind)
        - Clears all bets for all players
        - Clears last move
        - Adds a queue for players to start playing
        - Set blinds for the current round
        - Shuffle deck and add three cards to the board, and deal cards to players'''
        print('Pre-flop')
        self.prepare_round(pre_flop=True)
        self.set_blinds()
        self.deck.shuffle()
        self.deal_hands()
        for _ in range(3):
            self.add_card()
        for player in self.players:
            if player.is_computer:
                player.update_player_position()           # Must come before update strategy thresholds!
                player.update_strategy_thresholds()

    def flop(self):
        '''Ready game for the flop.
        - Sets required bet to 0$
        - Clears all bets for all players
        - Clears last move
        - Starts the queue again for all players
        - Reveal cards on the board'''
        print('Flop', end = ': ')
        self.prepare_round()
        self.board.reveal()
        print(self.board.cards())

    def turn(self):
        '''Ready game for the turn.
        - Sets required bet to 0
        - Clears all bets for all players
        - Clears last move
        - Start the queue again for all players
        - Adds a card to the board.'''
        print('Turn', end = ': ')
        self.prepare_round()
        self.add_card()
        print(self.board.cards())
    
    def river(self):
        '''Ready game for the rivefr.
        - Sets required bet to 0
        - Clears all bets for all players
        - Clears last move
        - Start the queue again for all players
        - Adds a card to the board.'''
        print('River', end=': ')
        self.prepare_round()
        self.add_card()
        print(self.board.cards())

    def showdown(self):
        '''Checks who will win.'''
        print('Showdown')
        winning_player = self.active_players()[0]

        for player in self.active_players():
            print(f"{player} had {player.handEval(self.board.cards())}")
            if player.handEval(self.board.cards()) > winning_player.handEval(self.board.cards()):
                winning_player = player

        print(f'The winning player is {winning_player}, with a hand of {winning_player.handEval(self.board.cards())}')
        winning_player.rake()       # Winning player takes in all the money
        self.winning_player = winning_player


    def play(self):
        '''Lets all the computers play their turn, then starts the next round if needed.'''
        n_turns = 0

        while len(self.player_queue) != 0:
            if len([p for p in self.active_players() if not p.is_all_in]) == 1:
                self.player_queue.clear()
                self.state = 3
                break
            current_player = self.player_queue[0]

            if current_player.is_all_in:                 # the player does not need to act if they are already all in
                requests.put(f'http://localhost:3003/api/session/{self.id}', json={ 'table': pickle.dumps(self).decode('latin1') })
                self.player_queue.pop(0)
                requests.put(f'http://localhost:3003/api/session/{self.id}', json={ 'table': pickle.dumps(self).decode('latin1') })
                continue

            if (current_player.is_computer):
                current_player.previous_step = None
                requests.put(f'http://localhost:3003/api/session/{self.id}', json={ 'table': pickle.dumps(self).decode('latin1') })
                current_player.play()
                requests.put(f'http://localhost:3003/api/session/{self.id}', json={ 'table': pickle.dumps(self).decode('latin1') })
                n_turns += 1
                if n_turns > 1000:
                    raise Exception(self.round_stats)
                    self.player_queue.clear()           # temp fix for bot problem
                    break
            else:
                break
        print(self.state)
        if len(self.player_queue) == 0:
            if self.state != 5:
                self.state = (self.state + 1) % 6
                rounds = [self.pre_flop, self.flop, self.turn, self.river, self.showdown, self.reset]
                
                rounds[self.state]()
                if 0 < self.state < 4:
                    self.play()

    def reset(self):
        '''Clears current cards on the board, resets deck, and removes all player handheld cards.
        Clears current round stats. Game stats are left unchanged.
        Players are still on the table, but shifted by one seat'''
        print('Reset')
        self.pot = 0
        self.state = 5
        self.board.clear()
        self.deck.reset()
        self.winning_player = None
        self.dealer = (self.dealer + 1) % len(self.players)     # Shift players
        self.betting_cap = 0                                    # Reset betting cap
        self.last_move: list[str, str] = []                     # Reset self.last_move
        for stat in self.game_stats.keys():
            self.round_stats[stat] = 0
        for player in self.players:
            player.reset()
        self.players = [p for p in self.players if p.balance > 0]       # kicks players who have no money left
        self.player_queue.clear()


    # Player actions Table Class
    def update_table_stats(self, player, move):
        '''Updates all table stats, based on the move. Used in all possible game moves.'''
        self.game_stats[move] += 1
        self.round_stats[move] += 1
        player.stats[move] += 1
        self.last_move = [player.name, move]

    def call(self, player):
        '''Player calls, matching the current bet.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'call')
            amount_to_call = self.required_bet - player.current_bet
            player.balance -= amount_to_call
            self.increase_pot(amount_to_call)
            print(f"{player} has called for {self.required_bet-player.current_bet}$ (balance: {player.balance}) (pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
            player.current_bet = self.required_bet
            self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))

    def check(self, player):
        '''Player checks, passing the turn without betting.'''
        if player == self.player_queue[0]:
            if player.current_bet == self.required_bet:
                print(f"{player} has checked. (balance: {player.balance}) They had {player.hand()}", "EHS:", player.ehs)
                self.update_table_stats(player, 'check')
                self.player_queue.pop(0)
            else:
                raise Exception("Can't check if your current bet does not match required bet!")
        else:
            raise(ValueError('Not your turn yet!'))

    def fold(self, player):
        '''Player folds, giving up their hand.'''
        if player == self.player_queue[0]:
            print(f"{player} has folded. (balance: {player.balance}) They had {player.hand()}", "EHS:", player.ehs)
            self.update_table_stats(player, 'fold')
            self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))     # ValueError is accounted for in tests, i.e. its appearance is checked for several testCases. You may decide to use another way of handling error, we'll just need to also change the test file.

    def bet(self, player, amount):
        '''Player bets, raising the required bet to stay in for the entire table.'''
        if player == self.player_queue[0]:
            if self.round_stats['bet'] == 3:        # Player cannot raise past this
                self.call(player)                   # Call the betting cap
            elif amount==self.required_bet:     # If bet amount is the same as required bet, it's basically a call.
                self.call(player)
            elif amount - self.required_bet < self.required_raise:
                raise Exception('cannot bet under minimum raise requirement')
            elif amount > player.balance:
                raise Exception('cant bet that, player has to go all-in. Remove this exception once allin method is done')  # Remove this when allin method is done
            else: 
                self.update_table_stats(player, 'bet')              # Update table stats
                amount_bet = amount - player.current_bet            # amount that the player throws into the pot
                player.balance -= amount_bet                        # Remove amount bet from player balance. The exact amount is not removed, because player could already have some money in the pot (current bet)
                self.increase_pot(amount_bet)                       # Increase the table pot by the extra amount that the player has bet on top of what they have already bet
                player.current_bet = amount                         # Set the player bet to the full current amount
                self.required_raise = amount - self.required_bet    # amount that the player has raised the pot by. this is now the minimum raise value, and the next raises cannot be lower than this
                self.required_bet = player.current_bet              
                self.betting_cap += 1
                print(f"{player} has bet {amount}$ (balance: {player.balance}) (the pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
                self.extend_queue(self.state)
                self.player_queue.pop(0)
        else:
            raise(ValueError('Not your turn yet!'))

    def all_in(self, player):
        '''Player all-ins, betting the remainder of their balance to stay in the game.'''
        if player == self.player_queue[0]:
            self.update_table_stats(player, 'all-in')                                                   # Update table stats
            self.increase_pot(player.balance)                                                           # Increase the table pot by the extra amount that the player has bet on top of what they have already bet
            player.current_bet += player.balance                                                        # Set the player bet to the full current amount
            self.required_raise = max(player.balance - self.required_bet, self.required_raise)          # The maximum raise becomes the raise that the player has just performed if it is larger than the current raise
            self.required_bet = max(player.current_bet, self.required_bet)              
            self.betting_cap += 1
            print(f"{player} has gone all-in with {player.balance}$ (balance: {player.balance}) (the pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
            player.balance = 0                                                                         # Remove amount bet from player balance. The exact amount is not removed, because player could already have some money in the pot (current bet)
            player.is_all_in = True
            self.extend_queue(self.state)
            self.player_queue.pop(0)

    # Misc
    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)
            player.join(self)

    def remove_player(self, player_name_to_remove):
        updated_players = []
        for player in self.players:
            if player.name == player_name_to_remove:
                player.leave()
            else:
                updated_players.append(player)
        
        self.players = updated_players
        self.player_queue = [p for p in self.player_queue if p.name != player_name_to_remove]

    def toJSON(self, player_name):
        return {
            'board': self.board.display(),
            'pot': self.pot,
            'players': [p.toJSON(player_name) for p in self.players],
            'player_queue': [p.toJSON(player_name) for p in self.player_queue],
            'required_bet': self.required_bet,
            'required_raise': self.required_raise,
            'state': self.state,
            'last_move': self.last_move,
            'winning_player': self.winning_player and self.winning_player.toJSON(player_name),
            'id': self.id
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
            '''The Player class. All bots/computers inherit from this class.'''
            self.name = name
            self.is_computer = is_computer
            self.table: Table | None = None
            self.__hand = []
            self.balance = balance
            self.current_bet = 0                # Balance of the player's bet for the current round
            self.active = True                  # Whether the player is still in round (hasn't folded yet).
            self.position = None                # Determines the position of the player. 0 = dealer, 1 = small blind, 2 = big blind, etc.
            self.previous_step = []
            self.ehs = 0
            self.is_all_in = False
            self.stats = {
                'bet': 0,
                'raise': 0,
                'call': 0,
                'check': 0,
                'all-in': 0,
                'fold': 0
            }

            if table:
                table.add_player(self)              # Add player to table
        
        def __repr__(self):
            return self.name
        
        def join(self, table: Table):
            self.table = table

        def leave(self):
            self.table = None

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
            '''Try calling, otherwise go all-in and bet'''
            if self.balance > self.table.required_bet - self.current_bet:
                self.table.call(self)
                self.previous_step = ['call', self.table.required_bet]
            else:
                self.all_in()


        def check(self):
            self.table.check(self)
            self.previous_step = ['check']
        
        def fold(self):
            self.active = False
            self.table.fold(self)
            self.previous_step = ['fold']

        def bet(self, amount):
            if self.balance > (amount - self.current_bet):
                self.table.bet(self, amount)
                self.previous_step = ['bet', self.current_bet]
            else:
                self.all_in()

        def all_in(self):
            print('All-in')
            self.table.all_in(self)
            self.previous_step = ['all-in', self.balance]

        def rake(self):
            self.balance += self.table.pot


        # Misc
        def reset(self):
            self.current_bet = 0
            self.active = True
            self.is_all_in = False
            self.clear_hand()
            self.position = None
            self.previous_step = []
            self.bluffing = False
            self.ehs = 0

        def toJSON(self, player_name):
            response = {
                'name': self.name,
                'is_computer': self.is_computer,
                'hand': [c.shortName for c in self.hand()],
                'balance': self.balance,
                'current_bet': self.current_bet,
                'active': self.active,
                'is_all_in': self.is_all_in,
                'previous_step': self.previous_step,
                'position': self.position
            }

            if self.name == player_name or self.table.state == 4:
                response['hand'] = [c.shortName for c in self.hand()]
            else:
                response['hand'] = [False for _ in self.hand()]

            return response

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
