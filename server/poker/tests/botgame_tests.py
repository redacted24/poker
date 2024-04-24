import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *

test_AdvancedBots = False
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


    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        for i in range(3):
            print('\ngame start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>\n')
 


@unittest.skipUnless(test_CopyCat, 'separate tests')
class TestFullGame(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = CopyCat('uwu', True, self.table)
        self.p4 = AdvancedBot('p1', 'tight', self.table)

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        for i in range(1):
            print('\ngame start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>\n')

if __name__ == "__main__":
    unittest.main()
