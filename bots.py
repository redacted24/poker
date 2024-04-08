from game import *

class Better(Player):
    '''A bot that always bets 99$, or all of his balance if it is less than 99$.'''
    def play(self):
        if self.balance <= 99:      # Check if balance is less than 99.
            self.bet(99)            # Bet 99 if it is more or equal to 99.
        else:
            self.bet(self.balance)  # Otherwise, bet the remaining balance of the bot.

class ScaryCat(Player):
    '''A bot that folds if the opponent bets.'''
    def test(self):
        return self.name

class Joker(Player):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''
    

if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    scary_cat = ScaryCat('Cat', table)
    better = Better('Better', table)

    table.pre_flop()
    for i in range(2):
        scary_cat.receive(table.deck.draw())
        better.receive(table.deck.draw())

    assert scary_cat.name == 'Cat'

    print('All tests passed')
