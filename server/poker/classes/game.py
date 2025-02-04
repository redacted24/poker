from poker.classes.cards import *

PREFLOP = 0
FLOP = 1
TURN = 2
RIVER = 3
SHOWDOWN = 4
RAKE = 5


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

    print('All tests passed.')
