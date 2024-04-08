from game import *

class ScaryCat(Player):
    '''A bot that folds if the opponent bets.'''
    def test(self):
        return self.name

class Joker(Player):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''
    

if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    b1 = ScaryCat('Cat', table)

    assert b1.test() == 'Cat'

    print('All tests passed')