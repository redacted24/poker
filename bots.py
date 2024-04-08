from game import *

class Better(Player):
    '''A bot that always bets 99$, or all of his balance if it is less than 99$.'''
    def play(self):
        if self.balance >= 99:      # Check if balance is less than 99.
            self.bet(99)            # Bet 99 if it is more or equal to 99.
        elif self.balance == 0:
            raise ValueError('you broke ahh')       # If bot doesn't have anymore money, they lose.
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

    assert scary_cat.name == 'Cat'

    table.pre_flop()        # Pre-flop
    for i in range(2):
        scary_cat.receive(table.deck.draw())
        table.deck.burn
        better.receive(table.deck.draw())
    better.play()           # Better bot plays (bets 99)
    better.play()           # Better bot plays (bets 99)

    assert better.balance == 1000-99*2
    assert table.pot == 99*2

    for i in range(8):
        better.play()
    

    print('All tests passed')
