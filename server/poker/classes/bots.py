from game import *

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
class TightPassive(Player):
    '''A bot that plays very few hands and is usually always checking, calling, or folding most of the time.'''
    # Currently working on implementing always checking/calling unless required bet is more than half of its own balance.
    def play(self):
        pass
