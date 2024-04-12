from game import *

class AdvancedBot(Player):
    # --- Pre-Flop Betting Strategy --- #
    def __init__(self, name, table):
        '''The general class for an advanced bot. Contains all the necessary information for advanced play. Children class will have specific methods that tweak information in this class in order to play.
        
        - Name (str)
        - Table (table object)

        There is no is_computer parameter since it is put as True by default in AdvancedBot class.'''
        Player.__init__(self, name, True, table)
        # Expert-defined values to calculate strategy thresholds. There are technically different thresholds, but we'll use the ones for 3-4 players for the sake of simplicity.
        # Dictionnary values are as:
        # 'name of strategy': [(base, increment) for each type of play], where the types of play are "tight", "moderate", and "loose"
        # The values for 'call1' and 'make1' are the same, as well as the values for 'call2' and 'make2'
        self.pre_flop_strategy_threshold = {
            'make1': [(50, 50), (50,25), (50,10)],
            'make2': [(200, 50), (200, 25), (200,10)],
            'make4': [(580, 0), (580, 0), (580, 0)]
        }
        # Income rates for pre-flop. Used to determine what strategy to play
        self.income_rates = [
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
    
    def get_income_rate(self):
        '''Return the IR rate of the bot's hand.'''
        temp = sorted(self.hand(), key=lambda x:x.value)
        if self.hand()[0].suit == self.hand()[1].suit:
            return self.income_rates[temp[1].value-2][temp[0].value-2]
        else:
            return self.income_rates[temp[0].value-2][temp[1].value-2]


    def make0(self):
        '''Fold if it costs more than zero to continue playing, otherwise check'''
        pass

    def call1(self):
        '''Fold if it costs more than 1 bet to continue playing, otherwise check/call'''
        pass

    def make1(self):
        '''If no bets have been made this round, then bet. Fold if two or more bets are required to continue. Otherwise check/call'''
        pass

    def call2(self):
        '''Always check/call, whatever bet is on the table'''
        pass

    def make2(self):
        '''Bet/raise if less than two bets/raises have been made this round, otherwise call'''
        pass

    def make4(self):
        '''Bet/raise until betting is capped'''
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
        self.call()

class Joker(Player):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''

# Real playstyles
class TightPassive(AdvancedBot):
    '''A bot that plays very few hands and is usually always checking, calling, or folding most of the time.'''
    # Currently working on implementing always checking/calling unless required bet is more than half of its own balance.
    def play(self):
        pass
