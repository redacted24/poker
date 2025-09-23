from poker.classes.deck import *
from poker.classes.player import Player
import random

PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
SHOWDOWN = 4

class Board():
    def __init__(self):
        self._cards: list[Card] = []

    def __repr__(self):
        return str(self._cards)

    def place_cards(self, cards: list[Card]):
        '''Places a card onto the board'''
        self._cards.extend(cards)

    def display(self):
        '''Returns a list containing strings of all cards names on the board.
        A card is False if it is not revealed.'''
        return [card for card in self._cards]

    def reset(self):
        '''Clears and resets the board to its initial state'''
        self._cards = []



class Table():
    def __init__(self):
        self.deck = Deck()
        self.board = Board()
        self.pot = 100
        self.dealer_index = 0
        self.turn_index = 0
        self.players: list[Player] = []
        self.stage = PREFLOP
        self.required_bet = 0
        self.min_raise = 0

    def add_players(self, players: list[Player]):
        self.players.extend(players)

    def __repr__(self):
        return (
            f"Stage: {Table.stage_map[self.stage]}, Pot: {self.pot}, Dealer: {self.players[self.dealer_index]}, Turn: {self.players[self.turn_index]}\n"
            f"Board: {self.board}\n"
            f"Players:\n  "
            f"{'\n  '.join([repr(p) for p in self.players])}"
            "\n"
        )
    
    def evaluate_hand(hand: list[Card]):
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
        
        def checkFlush(suits: dict, hand: list[Card]):
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
        
    stage_map = {
        PREFLOP: "Preflop",
        FLOP: "Flop",
        TURN: "Turn",
        RIVER: "River",
        SHOWDOWN: "Showdown",
    }

    def next_turn(self):
        n = len(self.players)
        for _ in range(n):
            self.turn_index = (self.turn_index + 1) % n
            p = self.players[self.turn_index]
            if not p.folded and not p.is_all_in:
                return

        return None
    
    def play_round(self):
        while self.turn_index is not None:
            active_players = [p for p in self.players if not p.folded and not p.is_all_in]

            # If there is only one active player
            if len(active_players) <= 1:
                break

            # If all bets are equalized
            if all(p.current_bet == self.required_bet and p.last_move for p in active_players):
                break

            player = self.players[self.turn_index]
            player.play(self)
            print(player, player.last_move)

            self.next_turn()

    def preflop(self):
        self.stage = PREFLOP
        for p in self.players:
            p.hand = [self.deck.draw(), self.deck.draw()]
            p.folded = False
            p.is_all_in = False
        
        self.players[(self.dealer_index + 1) % len(self.players)].raise_bet(self, 5)
        self.players[(self.dealer_index + 2) % len(self.players)].raise_bet(self, 5)
        
        self.turn_index = (self.dealer_index + 3) % len(self.players)

    def flop(self):
        self.stage = FLOP
        self.board.place_cards([self.deck.draw(), self.deck.draw(), self.deck.draw()])

    def turn(self):
        self.stage = TURN
        self.board.place_cards([self.deck.draw()])

    def river(self):
        self.stage = RIVER
        self.board.place_cards([self.deck.draw()])
    
    def showdown(self):
        self.stage = SHOWDOWN
        winner = random.choice([p for p in self.players if not p.folded])
        winner.stack += self.pot

    def reset(self):
        self.deck.reset()
        self.board.reset()
        self.pot = 0
        self.required_bet = 0
        self.min_raise = 0
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
    
    def play(self):
        for round in [self.preflop, self.flop, self.turn, self.river, self.showdown]:
            round()
            self.play_round()
            print(self)

            for p in self.players:
                p.last_move = ""
                p.current_bet = 0
            
            self.min_raise = 10
            self.required_bet = 0

        self.reset()
    

if __name__ == "__main__":
    t = Table()
    alice = Player('alice')
    bob = Player('bob')
    charlie = Player('charlie')
    diana = Player('diana')

    t.add_players([alice, bob, charlie, diana])
    t.play()
    # print('All tests passed.')

    # def flop(self):
    #     self.

    # def turn(self):
    #     '''Ready game for the turn.
    #     - Sets required bet to 0
    #     - Clears all bets for all players
    #     - Clears last move
    #     - Start the queue again for all players
    #     - Adds a card to the board.'''
    #     print('Turn', end = ': ')
    #     self.prepare_round()
    #     self.add_card()
    #     print(self.board.cards())
    
    # def river(self):
    #     '''Ready game for the river.
    #     - Sets required bet to 0
    #     - Clears all bets for all players
    #     - Clears last move
    #     - Start the queue again for all players
    #     - Adds a card to the board.'''
    #     print('River', end=': ')
    #     self.prepare_round()
    #     self.add_card()
    #     print(self.board.cards())

    # def showdown(self):
    #     '''Checks who will win.'''
    #     print('Showdown')
    #     winning_player = self.active_players()[0]

    #     for player in self.active_players():
    #         print(f"{player} had {player.handEval(self.board.cards())}")
    #         if player.handEval(self.board.cards()) > winning_player.handEval(self.board.cards()):
    #             winning_player = player

    #     print(f'The winning player is {winning_player}, with a hand of {winning_player.handEval(self.board.cards())}')
    #     winning_player.rake()       # Winning player takes in all the money
    #     self.winning_hand = winning_player.handEval(self.board.cards())
    #     self.winning_player = winning_player


    # def play(self):
    #     '''Lets all the computers play their turn, then starts the next round if needed.'''

    #     while len(self.player_queue) != 0:
    #         if len([p for p in self.active_players() if not p.is_all_in]) == 1:
    #             self.player_queue.clear()
    #             break
    #         current_player = self.player_queue[0]

    #         if current_player.is_all_in:                 # the player does not need to act if they are already all in
    #             self.player_queue.pop(0)
    #             continue

    #         if (current_player.is_computer):
    #             current_player.previous_step = None
    #             sleep(1.5)
    #             current_player.play()
    #             return True
    #         else:
    #             return False

    #     if len(self.player_queue) != 0: return False

    #     if self.state != 5:
    #         self.state = (self.state + 1) % 6
    #         rounds = [self.pre_flop, self.flop, self.turn, self.river, self.showdown, self.reset]
            
    #         rounds[self.state]()
    #         if 0 < self.state < 4:
    #             sleep(0.5)
    #             return True

    #     return False


    # def reset(self):
    #     '''Clears current cards on the board, resets deck, and removes all player handheld cards.
    #     Clears current round stats. Game stats are left unchanged.
    #     Players are still on the table, but shifted by one seat'''
    #     print('Reset')
    #     self.pot = 0
    #     self.state = 5
    #     self.board.clear()
    #     self.deck.reset()
    #     self.winning_player = None
    #     self.winning_hand = (None, [])
    #     self.dealer = (self.dealer + 1) % len(self.players)     # Shift players
    #     self.betting_cap = 0                                    # Reset betting cap
    #     self.last_move: list[str, str] = []                     # Reset self.last_move
    #     self.small_blind_amount += self.blind_interval
    #     self.big_blind_amount += self.blind_interval * 2
    #     for stat in self.game_stats.keys():
    #         self.round_stats[stat] = 0
    #     for player in self.players:
    #         player.reset()
    #     if not self.auto_rebuy:
    #         self.players = [p for p in self.players if p.balance > 0]       # kicks players who have no money left
    #     else:
    #         for p in self.players:
    #             if p.balance == 0:
    #                 p.balance = self.initial_balance

    #     self.player_queue.clear()


    # # Player actions Table Class
    # def update_table_stats(self, player, move):
    #     '''Updates all table stats, based on the move. Used in all possible game moves.'''
    #     self.game_stats[move] += 1
    #     self.round_stats[move] += 1
    #     player.stats[move] += 1
    #     self.last_move = [player.name, move]

    # def call(self, player):
    #     '''Player calls, matching the current bet.'''
    #     if player == self.player_queue[0]:
    #         self.update_table_stats(player, 'call')
    #         amount_to_call = self.required_bet - player.current_bet
    #         player.balance -= amount_to_call
    #         self.increase_pot(amount_to_call)
    #         print(f"{player} has called for {self.required_bet-player.current_bet}$ (balance: {player.balance}) (pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
    #         player.current_bet = self.required_bet
    #         self.player_queue.pop(0)
    #     else:
    #         raise(ValueError('Not your turn yet!'))

    # def check(self, player):
    #     '''Player checks, passing the turn without betting.'''
    #     if player == self.player_queue[0]:
    #         if player.current_bet == self.required_bet:
    #             print(f"{player} has checked. (balance: {player.balance}) They had {player.hand()}", "EHS:", player.ehs)
    #             self.update_table_stats(player, 'check')
    #             self.player_queue.pop(0)
    #         else:
    #             raise Exception("Can't check if your current bet does not match required bet!")
    #     else:
    #         raise(ValueError('Not your turn yet!'))

    # def fold(self, player):
    #     '''Player folds, giving up their hand.'''
    #     if player == self.player_queue[0]:
    #         print(f"{player} has folded. (balance: {player.balance}) They had {player.hand()}", "EHS:", player.ehs)
    #         self.update_table_stats(player, 'fold')
    #         self.player_queue.pop(0)
    #     else:
    #         raise(ValueError('Not your turn yet!'))     # ValueError is accounted for in tests, i.e. its appearance is checked for several testCases. You may decide to use another way of handling error, we'll just need to also change the test file.

    # def bet(self, player, amount):
    #     '''Player bets, raising the required bet to stay in for the entire table.'''
    #     if player == self.player_queue[0]:
    #         if self.round_stats['bet'] == 3:        # Player cannot raise past this
    #             self.call(player)                   # Call the betting cap
    #         elif amount==self.required_bet:     # If bet amount is the same as required bet, it's basically a call.
    #             self.call(player)
    #         elif amount - self.required_bet < self.required_raise:
    #             raise Exception('cannot bet under minimum raise requirement')
    #         else: 
    #             self.update_table_stats(player, 'bet')              # Update table stats
    #             amount_bet = amount - player.current_bet            # amount that the player throws into the pot
    #             player.balance -= amount_bet                        # Remove amount bet from player balance. The exact amount is not removed, because player could already have some money in the pot (current bet)
    #             self.increase_pot(amount_bet)                       # Increase the table pot by the extra amount that the player has bet on top of what they have already bet
    #             player.current_bet = amount                         # Set the player bet to the full current amount
    #             self.required_raise = amount - self.required_bet    # amount that the player has raised the pot by. this is now the minimum raise value, and the next raises cannot be lower than this
    #             self.required_bet = player.current_bet              
    #             self.betting_cap += 1
    #             print(f"{player} has bet {amount}$ (balance: {player.balance}) (the pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
    #             self.extend_queue(self.state)
    #             self.player_queue.pop(0)
    #     else:
    #         raise(ValueError('Not your turn yet!'))

    # def all_in(self, player):
    #     '''Player all-ins, betting the remainder of their balance to stay in the game.'''
    #     if player == self.player_queue[0]:
    #         self.update_table_stats(player, 'all-in')                                                   # Update table stats
    #         self.increase_pot(player.balance)                                                           # Increase the table pot by the extra amount that the player has bet on top of what they have already bet
    #         player.current_bet += player.balance                                                        # Set the player bet to the full current amount
    #         self.required_raise = max(player.balance - self.required_bet, self.required_raise)          # The maximum raise becomes the raise that the player has just performed if it is larger than the current raise
    #         self.required_bet = max(player.current_bet, self.required_bet)              
    #         self.betting_cap += 1
    #         print(f"{player} has gone all-in with {player.balance}$ (balance: {player.balance}) (the pot is now {self.pot}$). They had {player.hand()}", "EHS:", player.ehs)
    #         player.balance = 0                                                                         # Remove amount bet from player balance. The exact amount is not removed, because player could already have some money in the pot (current bet)
    #         player.is_all_in = True
    #         self.extend_queue(self.state)
    #         self.player_queue.pop(0)

    # # Misc
    # def add_player(self, player):
    #     if player not in self.players:
    #         self.players.append(player)
    #         player.join(self)


    # def remove_player(self, player_name_to_remove):
    #     updated_players = []
    #     for player in self.players:
    #         if player.name == player_name_to_remove:
    #             player.leave()
    #         else:
    #             updated_players.append(player)
        
    #     self.players = updated_players
    #     self.player_queue = [p for p in self.player_queue if p.name != player_name_to_remove]

    # def toJSON(self, player_name=None):
    #     return {
    #         'board': self.board.display(),
    #         'pot': self.pot,
    #         'players': [p.toJSON(player_name, self.show_all_bot_cards, self.show_all_cards) for p in self.players],
    #         'player_queue': [p.toJSON(player_name, self.show_all_bot_cards, self.show_all_cards) for p in self.player_queue],
    #         'required_bet': self.required_bet,
    #         'required_raise': self.required_raise,
    #         'state': self.state,
    #         'last_move': self.last_move,
    #         'winning_player': self.winning_player and self.winning_player.toJSON(player_name, self.show_all_bot_cards, self.show_all_cards),
    #         'winning_hand': [self.winning_hand[0], [card.shortName for card in self.winning_hand[1]]],
    #         'dynamic_table': self.dynamic_table,
    #         'id': self.id
    #     }

    # def end(self):
    #     '''A method that ends the current game. Clears game_stats. Players leave the table. Basically a harder reset than the reset method.'''
    #     self.reset()
    #     self.blinds_adjustment_factor = 0
    #     self.players.clear()
    #     for stat in self.game_stats.keys():
    #         self.game_stats[stat] = 0

# # -------------------------- #








# # -------------------------- #
# class Player():
#         def __init__(self, name, is_computer=True, table=None, balance = 1000):
#             '''The Player class. All bots/computers inherit from this class.'''
#             self.name = name
#             self.is_computer = is_computer
#             self.table: Table | None = None
#             self.__hand = []
#             self.balance = balance
#             self.current_bet = 0                # Balance of the player's bet for the current round
#             self.active = True                  # Whether the player is still in round (hasn't folded yet).
#             self.position = None                # Determines the position of the player. 0 = dealer, 1 = small blind, 2 = big blind, etc.
#             self.previous_step = []             # Holds the information of the previous move of the player (e.g. 'check')
#             self.ehs = 0
#             self.is_all_in = False
#             self.stats = {
#                 'bet': 0,
#                 'raise': 0,
#                 'call': 0,
#                 'check': 0,
#                 'all-in': 0,
#                 'fold': 0
#             }

#             if table:
#                 table.add_player(self)              # Add player to table
        
#         def __repr__(self):
#             return self.name
        
#         def join(self, table: Table):
#             self.table = table

#         def leave(self):
#             self.table = None

#         def handEval(self, river):
#             '''Compute strength of a certain hand of a certain size.
#             Takes in a list of 7 card objects, and returns (int, list) where first int is the hand type and the list is the cards in hand.
#             10. Royal Flush
#             9. Straight Flush
#             8. Four of a Kind
#             7. Full House
#             6. Flush
#             5. Straight
#             4. Three of a kind
#             3. Two Pair
#             2. Pair
#             1. High Card'''

#             def getOriginalStraight(values, hand):
#                 winning_hand = []
#                 for card in hand:
#                     if values and card.value == values[0]:
#                         winning_hand.append(card)
#                         values.pop(0)

#                 if values:
#                     winning_hand.append(hand[0])
#                 return winning_hand

#             def checkStraight(values: dict, hand):
#                 sorted_values = sorted(values.keys(), reverse=True)
#                 if 14 in sorted_values: sorted_values.append(1)
#                 consecutive = 1
#                 for i in range(0, len(sorted_values) - 1):
#                     if sorted_values[i] - 1 == sorted_values[i+1]:
#                         consecutive += 1
#                         if consecutive == 5:
#                             return getOriginalStraight(sorted_values[i-3:i+2], hand)
#                     else:
#                         consecutive = 1
#                 return False
            
#             def checkFlush(suits: dict, hand: list[Cards]):
#                 for suit, items in suits.items():
#                     if items >= 5:
#                         suited_cards = [card for card in hand if card.suit == suit]
#                         flush_values = {}
#                         for card in suited_cards:
#                             flush_values[card.value] = values.get(card.value, 0) + 1
#                         flush_straight = checkStraight(flush_values, suited_cards)
#                         return flush_straight, suited_cards
#                 return False, False


#             def getOriginalValues(num_items, values, hand):
#                 winning_hand = []
#                 while num_items:
#                     for value, items in sorted(values.items(), key=lambda x: x[1]):
#                         if num_items and items >= num_items[0]:
#                             winning_hand += [card for card in hand if card.value == value]
#                             num_items.pop(0)

#                 winning_hand = winning_hand[0:5]

#                 for card in hand:
#                     if card not in winning_hand:
#                         if len(winning_hand) >= 5:
#                             break
#                         winning_hand.append(card)

#                 return winning_hand

#             hand = self.hand() + river
#             values = {}
#             suits = {}
#             sorted_hand = sorted(hand, reverse=True, key=lambda c: c.value)
#             for card in sorted_hand:
#                 values[card.value] = values.get(card.value, 0) + 1
#                 suits[card.suit] = suits.get(card.suit, 0) + 1

#             flush_straight, flush = checkFlush(suits, sorted_hand)
#             straight = checkStraight(values, sorted_hand)

#             if flush_straight and flush_straight[0].value == 14:
#                 return 10, flush_straight
#             elif flush_straight:
#                     return 9, flush_straight
#             elif 4 in values.values():
#                 return 8, getOriginalValues([4], values, sorted_hand)
#             elif len([v for v in values.values() if v == 3]) == 2 or (3 in values.values() and 2 in values.values()):
#                 return 7, getOriginalValues([3, 2], values, sorted_hand)
#             elif flush:
#                 return 6, flush[0:5]
#             elif straight:
#                 return 5, straight
#             elif 3 in values.values():
#                 return 4, getOriginalValues([3], values, sorted_hand)
#             elif len([v for v in values.values() if v == 2]) >= 2:
#                 return 3, getOriginalValues([2, 2], values, sorted_hand)
#             elif 2 in values.values():
#                 return 2, getOriginalValues([2], values, sorted_hand)
#             else:
#                 return 1, sorted_hand[0:5]

#         def riverEval(self):
#             '''Return the highest scoring hand pattern of player + board.'''
#             # Deprecated
#             pass

#         def look(self):
#             '''Prints player hand.'''
#             print(f'Your hand is: {str(self.__hand)}')
        
#         def hand(self):
#             '''Returns player hand'''
#             return self.__hand

#         def receive(self, cards):
#             '''Receives cards in hand.'''
#             if isinstance(cards, list):
#                 self.__hand.extend(cards)
#             else:
#                 self.__hand.append(cards)

#         def clear_hand(self):
#             '''Removes all cards held in hand.'''
#             self.__hand.clear()


#         # Player moves
#         def call(self):
#             '''Try calling, otherwise go all-in and bet'''
#             if self.balance > self.table.required_bet - self.current_bet:
#                 self.table.call(self)
#                 self.previous_step = ['call', self.table.required_bet]
#             else:
#                 self.all_in()


#         def check(self):
#             '''Check, a.k.a do nothing'''
#             self.table.check(self)
#             self.previous_step = ['check']
        
#         def fold(self):
#             '''Lay down your cards and leave the table.'''
#             self.active = False
#             self.table.fold(self)
#             self.previous_step = ['fold']

#         def bet(self, amount):
#             '''Bet a certain amount into the pot'''
#             if self.balance > (amount - self.current_bet):
#                 self.table.bet(self, amount)
#                 self.previous_step = ['bet', self.current_bet]
#             else:
#                 self.all_in()

#         def all_in(self):
#             '''Go all-in'''
#             print('All-in')
#             self.table.all_in(self)
#             self.previous_step = ['all-in', self.balance]

#         def rake(self):
#             '''Take in the amount of money in the pot after a win.'''
#             self.balance += self.table.pot


#         # Misc
#         def reset(self):
#             '''Reset player stats'''
#             self.current_bet = 0
#             self.active = True
#             self.is_all_in = False
#             self.clear_hand()
#             self.position = None
#             self.previous_step = []
#             self.bluffing = False
#             self.ehs = 0

#         def toJSON(self, player_name, show_all_bot_card, show_all_cards):
#             '''Put all player variables into JSON. Used for communication with frontend'''
#             response = {
#                 'name': self.name,
#                 'is_computer': self.is_computer,
#                 'hand': [c.shortName for c in self.hand()],
#                 'balance': self.balance,
#                 'current_bet': self.current_bet,
#                 'active': self.active,
#                 'is_all_in': self.is_all_in,
#                 'previous_step': self.previous_step,
#                 'position': self.position
#             }

#             if self.name == player_name or self.table.state == 4 or (show_all_bot_card and self.is_computer) or show_all_cards:
#                 response['hand'] = [c.shortName for c in self.hand()]
#             else:
#                 response['hand'] = [False for _ in self.hand()]

#             return response

#         def clear_all_stats(self):
#             '''Clears all player stats.'''
#             for stat in self.stats.keys():
#                 self.stats[stat] = 0

#         def update_player_position(self):
#             '''Update player_position. Used if the player is a computer'''
#             pass

#         def update_strategy_thresholds(self):
#             '''Update strategy_thresholds. Used if the player is a computer'''
#             pass



