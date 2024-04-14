from poker.classes.game import *

class AdvancedBot(Player):
    # --- Pre-Flop Betting Strategy --- #
    # Income rates for pre-flop. Used to determine what strategy to play
    # From left to right, each column goes from 2 to A
    # From top to bottom, each row goes from 2 to A
    # Suited hand's IR is calculated for row>column, otherwise an unsuited hand's IR will be calculated as column<row
    income_rates = [
        [-121, -440, -409, -382, -411, -432, -394, -357, -301, -259, -194, -116, 16 ],
        [-271, -42,  -345, -312, -340, -358, -371, -328, -277, -231, -165, -87,  54 ],
        [-245, -183,  52,  -246, -269, -287, -300, -308, -252, -204, -135, -55,  84 ],
        [-219, -151, -91,   152, -200, -211, -227, -236, -227, -169, -104, -24,  118],
        [-247, -177, -113, -52,   256, -145, -152, -158, -152, -145, -74,   9,   99 ],
        [-261, -201, -129, -65,   3,    376, -76,  -79,  -68,  -66,  -44,  48,   148],
        [-226, -204, -140, -73,  -2,    66,   503,  0,    15,   24,   45,  84,   194],
        [-191, -166, -147, -79,  -5,    68,   138,  647,  104,  113,  136, 177,  241],
        [-141, -116, -91,  -69,  -4,    75,   150,  235,  806,  226,  255, 295,  354],
        [-89,  -67,  -41,  -12,   7,    82,   163,  248,  349,  965,  301, 348,  410],
        [-29,  -3,    22,   51,   80,   108,  185,  274,  379,  423,  1141,403,  473],
        [47,    76,   101,  128,  161,  199,  230,  318,  425,  473,  529, 1325, 541],
        [175,   211,  237,  266,  249,  295,  338,  381,  491,  539,  594, 655, 1554]
    ]

    # Expert-defined values to calculate strategy thresholds. There are technically different thresholds, but we'll use the ones for 3-4 players for the sake of simplicity.
    # Dictionnary values are as:
    # 'tightness': [(make1 values), (make2 values), (make3 values)] where values are a tuple (base, increment)
    # The values for 'call1' and 'make1' are the same, as well as the values for 'call2' and 'make2'
    preflop_strategy_values = {
        'tight': {'make1': (-50, 50), 'make2': (150, 50), 'make4': (300,0)},
        'moderate': {'make1': (-50, 50), 'make2': (50, 50), 'make4': (300,0)},
        'loose': {'make1': (-50, 50), 'make2': (0, 0), 'make4': (300,0)}
    }

    def __init__(self, name, table, tightness):
        '''The general class for an advanced bot. Contains all the necessary information for advanced play. Children class will have specific methods that tweak information in this class in order to play.
        
        - Name (str)
        - Table (table object)

        There is no is_computer parameter since it is put as True by default in AdvancedBot class.'''
        Player.__init__(self, name, True, table)
        self.chosen_pre_flop_strategy = AdvancedBot.preflop_strategy_values[tightness]        # Chosen strategy is moderate by default. The variable is a dictionnary. See preflop_strategy_values
        self.position = 0       # Position: "the number of players to act before it is the small blind's turn again." (Papp, 1998)
        self.strategy_thresholds = {
            'make1': 0,
            'make2': 0,
            'make4': 0
        }
    
    def play(self):
        '''Playing function for the bot.'''
    
    def update_player_position(self):
        '''Compute the position number of the player.'''
        # Calculated by number of active players - the index of the player in queue.
        # e.g. If we are checking for the position of the small blind in a two player match, it would be: 2 - 0 = 2. (because there are two players in the match, and small-blind is at the start of the player queue)
        if self.table.active_players() and self.table.player_queue:
            self.position = int(len(self.table.active_players())-(self.table.player_queue.index(self)))
        else:
            raise ValueError('Cannot update player position if game has not been started/set.')
        
    def update_strategy_thresholds(self):
        '''Update threshold values for all strategies (make1, make2, make4)'''
        self.strategy_thresholds['make1'] = self.chosen_pre_flop_strategy['make1'][0] + self.chosen_pre_flop_strategy['make1'][1]*self.position
        self.strategy_thresholds['make2'] = self.chosen_pre_flop_strategy['make2'][0] + self.chosen_pre_flop_strategy['make2'][1]*self.position
        self.strategy_thresholds['make4'] = self.chosen_pre_flop_strategy['make4'][0] + self.chosen_pre_flop_strategy['make4'][1]*self.position
    
    def get_income_rate(self):
        '''Return the IR rate of the bot's hand.'''
        temp = sorted(self.hand(), key=lambda x:x.value)
        if self.hand()[0].suit == self.hand()[1].suit:
            return AdvancedBot.income_rates[temp[1].value-2][temp[0].value-2]
        else:
            return AdvancedBot.income_rates[temp[0].value-2][temp[1].value-2]
        
    def call1(self):
        '''Fold if it costs more than 1 bet to continue playing and the bot hasn't put money into the pot this round yet, otherwise check/call. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        print('Call1 strategy used')
        # Not really used except for small blind
        if self.current_bet == 0 and self.table.round_stats['bet'] > 1:         # Fix self.current_bet == 0 when big blind and small blind are integrated (i.e. automatically deducted from player)
            self.fold()
            print('Bot has folded (call1)')
            return 'fold'
        else:
            if self.current_bet == self.table.required_bet:     # Should only happen if the bot is the big blind, in which case he would have automatically already bet
                self.check()
                print('Bot has checked (call1)')
                return 'check'
            else:
                self.call()
                print('Bot has called (call1)')
                return 'call'
        
    def make1(self):
        '''If no bets have been made this round, then bet. Fold if two or more bets are required to continue. Otherwise check/call. THIS STRATEGY SHOULD NOT BE CALLED IF BOT IS THE BIG BLIND (it shouldn't happen). Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        if self.current_bet == 0 and self.table.round_stats['bet'] > 1:
            self.fold()
            print('Bot has folded (make1)')
            return 'fold'
        elif self.table.round_stats['bet'] == 0:
            self.bet(100)
            print('Bot has bet (make1)')
            return 'bet'
        else:
            if self.current_bet == self.table.required_bet:
                self.check()
                print('Bot has checked (make1)')
                return 'check'
            else:
                self.call()
                print('Bot has called (make1)')
                return 'call'

    def call2(self):
        '''Always check/call, whatever bet is on the table. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        # Not really used except for small blind
        if self.current_bet == self.table.required_bet:
            print('bot checks (call2)')
            self.check()
            return 'check'
        else:
            self.call()
            print('bot calls (call2)')
            return 'call'

    def make2(self):
        '''Bet/raise if less than two bets/raises have been made this round, otherwise call. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        if self.table.round_stats['bet'] < 2:
            self.bet(100)
            print('Bot has bet (make2)')
            return 'bet'
        else:
            self.call()
            print('Bot has called (make2)')
            return 'call'

    def make4(self):
        '''Bet/raise until betting is capped. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        pass

# Meme bots
class Better(Player):
    '''A bot that always bets 99$, or all of his balance if it is less than 99$.'''
    def play(self):
        if self.balance >= 99:      # Check if balance is less than 99.
            self.bet(99)            # Bet 99 if it is more or equal to 99.
        elif self.balance == 0:
            raise ValueError('you broke ahh')       # If bot doesn't have anymore money, they lose.
        else:
            self.bet(self.balance)  # Otherwise, bet the remaining balance of the bot, as an all-in.

class ScaryCat(Player):
    '''A bot that always if a single opponent bets. Otherwise, checks.'''
    def play(self):
        if self.current_bet == self.table.required_bet:
            self.check()
        else:
            self.call()

class Joker(Player):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''

# Real playstyles
class TightPassive(AdvancedBot):
    '''A bot that plays very few hands and is usually always checking, calling, or folding most of the time.'''
    # Currently working on implementing always checking/calling unless required bet is more than half of its own balance.
    def play(self):
        pass
