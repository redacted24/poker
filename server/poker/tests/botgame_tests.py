import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *

test_AdvancedBots = True
test_CopyCat = True

# ---
@unittest.skipUnless(test_AdvancedBots, 'separate tests')
class TestFullGame(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = AdvancedBot('p4', 'loose', self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        print('game start -------------------------')
        self.table.play()
        self.table.reset()
        print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>')
        for i in range(2):
            print('game start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>')
 

if __name__ == "__main__":
    unittest.main()
