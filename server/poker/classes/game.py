import json, os
from poker.classes.cards import *

# Game States
PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
SHOWDOWN = 4
RAKE = 5


# Hand Types
ROYAL_FLUSH = 10
STRAIGHT_FLUSH = 9
FOUR_OF_A_KIND = 8
FULL_HOUSE = 7
FLUSH = 6
STRAIGHT = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
PAIR = 2
HIGH_CARD = 1


poker_hands = []

dirname = os.path.dirname(__file__)

fp = open(os.path.join(dirname, "poker_hands_5.json"))
poker_hands.append(json.load(fp))
fp = open(os.path.join(dirname, "poker_hands_6.json"))
poker_hands.append(json.load(fp))
fp = open(os.path.join(dirname, "poker_hands_7.json"))
poker_hands.append(json.load(fp))


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
    def __init__(self):
        self.deck: Deck = Deck()
        self.board: Board = Board()
        self.players: list[Player] = []
        self.dealer_pos: int = 0
        self.player_queue: list[Player] = []

        self.pot = 0
        self.required_bet = 0
        self.required_raise = 0
        self.state = PREFLOP
        self.winning_player = None
        self.winning_hand = None

        self.blind_amount = 5
        self.log_moves = True


    # Functionality
    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

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

    def set_queue(self, start_pos):
        queue = self.players[start_pos:] + self.players[:start_pos]
        self.player_queue = [p for p in queue if p.active]

    def log(self, message):
        if self.log_moves:
            print(message)

    # Player Actions
    def action(f):
        def wrapped(table, player, *args, **kwargs):
            if player != table.player_queue[0]: raise ValueError('Not your turn yet!')

            starting_balance = player.balance

            amount = f(table, player, *args, **kwargs)

            if (table.log_moves):
                print(str(player).ljust(8),
                      ':',
                      str(starting_balance).ljust(4),
                      "->",
                      str(player.balance).ljust(4),
                      "|",
                      f.__name__[0].upper(),
                      str(amount or "").ljust(4))

            table.player_queue.pop(0)

            if (len(table.player_queue) == 0):
                table.log(f"Pot: ${table.pot}")
                table.state += 1
                table.start_round()

        return wrapped


    @action
    def check(self, player):
        '''Player checks, passing the turn without betting.'''
        if (self.required_bet != player.current_bet): raise ValueError('Cannot check when a call is necessary!')

    @action
    def bet(self, player, amount):
        '''Player bets, raising the required bet to stay in for the entire table.'''
        if (amount - self.required_bet < self.required_bet + self.required_raise): raise ValueError('Less than the minimum raise!')

        bet_amount = amount - player.current_bet

        player.balance -= bet_amount
        self.increase_pot(bet_amount)
        self.required_bet = amount

        player.current_bet = self.required_bet
        self.set_queue(self.players.index(player))

        return bet_amount

    @action
    def call(self, player):
        '''Player calls, matching the current bet.'''
        if (self.required_bet == player.current_bet): raise ValueError('No bets to call!')

        call_amount = self.required_bet - player.current_bet
        player.balance -= call_amount
        self.increase_pot(call_amount)
    
        player.current_bet = self.required_bet

        return call_amount

    @action
    def fold(self, player):
        '''Player folds, giving up their hand.'''

    @action
    def all_in(self, player):
        '''Player all-ins, betting the remainder of their balance to stay in the game.'''

        amount = player.balance

        player.balance = 0
        player.current_bet += amount
        self.increase_pot(amount)

        self.required_bet = max(player.current_bet, self.required_bet)
        player.is_all_in = True
        self.set_queue(self.players.index(player))
        
        return amount
    
    @action
    def show_hand(self, player):
        '''Player shows their hand for the final showdown'''
        if (self.state != SHOWDOWN): raise ValueError('Not showdown yet!')
        
        if (self.winning_player is None or self.winning_player.handEval(self.board.cards()) < player.handEval(self.board.cards())):
            self.winning_player = player


    # Game Logic
    def start_round(self):
        self.required_bet = self.required_raise = 0
        for player in self.players:
            player.clear_bet()

        match self.state:
            case 0:
                self.pre_flop()

            case 1:
                self.flop()

            case 2:
                self.turn()
            
            case 3:
                self.river()

            case 4:
                self.showdown()

            case 5:
                self.rake()

    def pre_flop(self): 
        "Ready game for the pre-flop."

        self.set_queue(self.dealer_pos+1)
        self.deal_hands()
        for _ in range(3):
            self.add_card()

        self.print_setup()
        self.log("\nPreflop")

        self.player_queue[0].bet(self.blind_amount)
        self.player_queue[0].bet(self.blind_amount * 2)
        self.set_queue(self.dealer_pos+3)


    def flop(self):
        self.board.reveal()

        self.log(f"\nFlop: {self.board.cards()}")
        self.set_queue(self.dealer_pos+1)

    def turn(self):
        self.add_card()
        self.log(f"\nTurn: {self.board.cards()[:-1]} {self.board.cards()[-1:]}")
        self.set_queue(self.dealer_pos+1)

    def river(self):
        self.add_card()
        self.log(f"\nRiver: {self.board.cards()[:-1]} {self.board.cards()[-1:]}")
        self.set_queue(self.dealer_pos+1)

    def showdown(self):
        self.log(f"\nShowdown: {self.board.cards()}")
        self.set_queue(self.dealer_pos+1)

    def rake(self):
        self.winning_hand = self.winning_player.handEval(self.board.cards())
        self.winning_player.rake()       # Winning player takes in all the money

        self.log(f'The winning player is {self.winning_player}, with a hand of {self.winning_hand}')
        self.reset()

    def reset(self):
        '''Clears current cards on the board, resets deck, and removes all player handheld cards.
        Clears current round stats. Game stats are left unchanged.
        Players are still on the table, but shifted by one seat'''
        self.log('\nReset\n')

        self.deck.reset()
        self.board.clear()
        self.players = [p for p in self.players if p.balance > 0]
        self.dealer_pos = (self.dealer_pos + 1) % len(self.players)
        self.player_queue.clear()

        self.pot = 0
        self.required_bet = 0
        self.required_raise = 0
        self.state = PREFLOP
        self.winning_player = None
        self.winning_hand = None

        for player in self.players:
            player.reset()



    # Misc
    def print_setup(self):
        self.log("Setup")

        roles = ["SB", "BB"]

        for player, role in zip(self.player_queue, roles):
            self.log(f"{role}: {player}")


    def toJSON(self, player_name=None):
        return {
            'board': self.board.display(),
            'players': [p.toJSON(player_name) for p in self.players],
            'player_queue': [p.toJSON(player_name) for p in self.player_queue],
            'dealer_pos': self.dealer_pos,

            'pot': self.pot,
            'required_bet': self.required_bet,
            'required_raise': self.required_raise,
            'state': self.state,

            'winning_player': self.winning_player and self.winning_player.toJSON(player_name),
            'winning_hand': [self.winning_hand[0], [card.shortName for card in self.winning_hand[1]]]
        }

# -------------------------- #



# -------------------------- #
class Player():
        def __init__(self, name, table=None, is_computer=True, balance=1000):
            '''The Player class. All bots/computers inherit from this class.'''
            self.name = name
            self.is_computer = is_computer
            self.table: Table | None = table
            self.__hand = []
            self.balance = balance

            self.current_bet = 0                # Balance of the player's bet for the current round
            self.active = True                  # Whether the player is still in round (hasn't folded yet).

            self.ehs = 0
            self.is_all_in = False

            if table:
                table.add_player(self)              # Add player to table
        
        def __repr__(self):
            return self.name

        def join(self, table: Table):
            self.table = table
            table.add_player(self)

        def leave(self):
            self.table = None
            table.remove_player(self)
    
        def can_pay(self, amount):
            return self.balance > (amount - self.current_bet)


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
            
            def checkFlush(hand: list[Cards]):
                suits = {}

                for card in hand:
                    suits[card.suit] = suits.get(card.suit, []) + [card]
                
                for cards in suits.values():
                    if len(cards) >= 5:
                        return cards

                return False
            
            def getOriginalValues(hand: list[Cards], poker_hand: str):
                values_needed = [int(char, 16) for char in poker_hand]

                original_hand = []
                for value in values_needed:
                    for idx, card in enumerate(hand):
                        if value == card.value:
                            original_hand.append(hand.pop(idx))
                            break

                return original_hand


            hand = sorted(self.hand() + river, key=lambda c: c.value)

            converted_hand = ''.join([card.hex_value for card in hand])

            hand_type, poker_hand = poker_hands[len(hand) - 5].get(converted_hand, [HIGH_CARD, None])

            if (hand_type >= FULL_HOUSE):
                return hand_type, getOriginalValues(hand, poker_hand)

            flush_cards = checkFlush(hand)
            if (flush_cards):
                if hand_type == STRAIGHT:
                    converted_hand = ''.join([card.hex_value for card in flush_cards])
                    flush_hand_type, flush_poker_hand = poker_hands[len(flush_cards) - 5].get(converted_hand, [HIGH_CARD, None])
                    if (flush_hand_type == STRAIGHT):
                        return STRAIGHT_FLUSH + (flush_poker_hand[0] == 'E'), getOriginalValues(hand, flush_poker_hand)

                return FLUSH, flush_cards[:-6:-1]

            if hand_type == HIGH_CARD: return hand_type, hand[:-6:-1] 

            return hand_type, getOriginalValues(hand, poker_hand)

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
        def check(self):
            '''Check, a.k.a do nothing'''
            self.table.check(self)

        def fold(self):
            '''Lay down your cards and leave the table.'''
            self.active = False
            self.table.fold(self)

        def call(self):
            '''Try calling, otherwise go all-in and bet'''
            if self.can_pay(self.table.required_bet): 
                self.table.call(self)
            else: 
                self.all_in()

        def bet(self, amount):
            '''Bet a certain amount into the pot'''
            if self.can_pay(amount):
                self.table.bet(self, amount)
            else:
                self.all_in()

        def all_in(self):
            '''Go all-in'''
            self.table.all_in(self)

        def show_hand(self):
            '''Shows hand'''
            self.table.show_hand(self)

        def rake(self):
            '''Take in the amount of money in the pot after a win.'''
            self.balance += self.table.pot


        # Misc
        def clear_bet(self):
            '''Reset player bet'''
            self.current_bet = 0

        def reset(self):
            self.__hand.clear()

            self.current_bet = 0                # Balance of the player's bet for the current round
            self.active = True                  # Whether the player is still in round (hasn't folded yet).

            self.ehs = 0
            self.is_all_in = False

        def toJSON(self, player_name, show_all_bot_card, show_all_cards):
            '''Put all player variables into JSON. Used for communication with frontend'''
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

            if self.name == player_name or self.table.state == 4 or (show_all_bot_card and self.is_computer) or show_all_cards:
                response['hand'] = [c.shortName for c in self.hand()]
            else:
                response['hand'] = [False for _ in self.hand()]

            return response



if __name__ == "__main__":
    table = Table()
    p1 = Player("alex", table)
    p2 = Player("bob", table)
    p3 = Player("charlie", table)
    p4 = Player("david", table)

    table.log_moves = True
    table.start_round()

    # Preflop
    p4.call()
    p1.bet(30)
    p2.call()
    p3.call()
    p4.call()

    # # Flop
    p2.check()
    p3.bet(50)
    p4.call()
    p1.bet(150)
    p2.fold()
    p3.call()
    p4.call()

    # # Turn
    p3.check()
    p4.bet(200)
    p1.call()
    p3.fold()

    # # River
    p4.bet(300)
    p1.call()

    # # Showdown
    p4.show_hand()
    p1.fold()

    print(table.player_queue)

    print(p1.handEval([Deck.get('9s'), Deck.get('Ts'), Deck.get('Js'), Deck.get('Ks'), Deck.get('As')])) # == (5, '[As, Ks, Js, Ts, 9s]')
    print(p1.handEval([Deck.get('Ts'), Deck.get('Qs'), Deck.get('Js'), Deck.get('Ks'), Deck.get('As')])) # == (1, '[As, Ks, Qs, Js, Ts]')
    print(p1.handEval([Deck.get(card) for card in ['2d', '6s', 'Kh', 'Qd', 'Ad', 'Ks', 'Td']])) # == (3, '[9s, 9h, 9d, 9c]') 
    print(p1.handEval([Deck.get('As'), Deck.get('Ks'), Deck.get('Qs'), Deck.get('Qh'), Deck.get('Js'), Deck.get('Jh'), Deck.get('Ts')])) # == (1, '[As, Ks, Qs, Js, Ts]')
    print(p1.handEval([Deck.get('Ks'), Deck.get('Ts'), Deck.get('8h'), Deck.get('9d'), Deck.get('7c'), Deck.get('6s'), Deck.get('8s')])) # == (6, '[10, 9, 8, 7, 6]')
    print(p1.handEval([Deck.get('Ks'), Deck.get('Ts'), Deck.get('8h'), Deck.get('9d'), Deck.get('8c'), Deck.get('8s'), Deck.get('6h')]))

    print('All tests passed.')