from game import *

class Bot(Player):
    # --- Pre-Flop Betting Strategy --- #
    def __init__(self):
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
            [-121, -440, -409, -382, -411, -432, -394, -357, -301, -259, -194, -116, 16],
            [-271, -42, -345, -312, -340, -358, -371, -328, -277, -231, -165, -87, 54],
            
        ]

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
class Better(Bot):
    '''A bot that always bets 99$, or all of his balance if it is less than 99$.'''
    def play(self):
        if self.balance >= 99:      # Check if balance is less than 99.
            self.bet(99)            # Bet 99 if it is more or equal to 99.
        elif self.balance == 0:
            raise ValueError('you broke ahh')       # If bot doesn't have anymore money, they lose.
        else:
            self.bet(self.balance)  # Otherwise, bet the remaining balance of the bot, as an all-in.

class ScaryCat(Bot):
    '''A bot that always if a single opponent bets. Otherwise, checks.'''
    def play(self):
        self.call()

class Joker(Bot):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''

# Real playstyles
class TightPassive(Bot):
    '''A bot that plays very few hands and is usually always checking, calling, or folding most of the time.'''
    # Currently working on implementing always checking/calling unless required bet is more than half of its own balance.
    def play(self):
        pass
