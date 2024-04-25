import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *

# choose which test to run, and how many games you want them to play against.
test_AdvancedBots = False           # 4 advancedbots
test_CopyCat = False                # 1 copycat vs 3 advancedbots
test_RingRingItsTheCaller = False   # 1 caller vs 3 advancedbots

iterations = 15

# ---
@unittest.skipUnless(test_AdvancedBots, 'separate tests')
class TestAdvancedBots(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = AdvancedBot('p4', 'moderate', self.table)

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        for i in range(iterations):
            print('\ngame start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('\nstats {')
            for i in self.table.players:
                print(f'{i} has a balance of {i.balance}')
            print('}')
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>\n')
 
@unittest.skipUnless(test_CopyCat, 'separate tests')
class TestCat(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = AdvancedBot('p3', 'tight', self.table)
        self.p4 = CopyCat('uwu', True, self.table)

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        for i in range(iterations):
            print('\ngame start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('\nstats {')
            for i in self.table.players:
                print(f'{i} has a balance of {i.balance}')
            print('}')
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>\n')

@unittest.skipUnless(test_RingRingItsTheCaller, 'separate tests')
class TestRingRing(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = RingRingItsTheCaller('caller', True, self.table)

    def tearDown(self):
        self.table.end()
    
    def test_fullGame(self):
        for i in range(iterations):
            print('\ngame start -------------------------')
            self.table.pre_flop()
            self.table.play()
            self.table.reset()
            print('\nstats {')
            for i in self.table.players:
                print(f'{i} has a balance of {i.balance}')
            print('}')
            print('game end >>>>>>>>>>>>>>>>>>>>>>>>>>\n')

class TestAllIn(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'loose', self.table)
        self.p2 = AdvancedBot('p2', 'tight', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = RingRingItsTheCaller('caller', True, self.table)

    def tearDown(self):
        self.table.end()

    def test_allin(self):
        print('eeeeeeee')
        self.table.pre_flop()
        self.p4.call()
        self.p1.all_in()
        self.p2.fold()
        self.p3.fold()
        self.p4.call()

if __name__ == "__main__":
    unittest.main()
