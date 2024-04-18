import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *

# ---
class TestFullGame(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'loose', self.table)
        self.p3 = AdvancedBot('p3', 'loose', self.table)
        self.p4 = AdvancedBot('p4', 'loose', self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        self.table.play()


if __name__ == "__main__":
    unittest.main()
