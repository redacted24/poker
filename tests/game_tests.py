import sys
import unittest
sys.path.append('../poker/server/poker/classes')
from bots import *              # If you have Pylance installed ignore underline

# ---
class TestTableMethods(unittest.TestCase):
    def setUp(self):            # Run this for every unit test
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', self.table)

    def tearDown(self):
        self.table.end()

    def test_boardSize_preflop(self):
        self.table.pre_flop()
        self.assertEqual(len(self.table.board),3,'Incorrect number of cards on board')

    def test_boardSize_flop(self):
        self.table.pre_flop()
        self.table.flop()
        self.assertEqual(len(self.table.board), 3, 'Incorrect number of cards on board')

    def test_boardSize_turn(self):
        self.table.pre_flop()
        self.table.flop()
        self.table.turn()
        self.assertEqual(len(self.table.board), 4, 'Incorrect number of cards on board')

    def test_boardSize_river(self):
        self.table.pre_flop()
        self.table.flop()
        self.table.turn()
        self.table.river()
        self.assertEqual(len(self.table.board), 5, 'Incorrect number of cards on board')
    
    def test_playerBetIncreasesPot(self):
        self.p1.bet(100)
        self.assertEqual(self.table.pot,100,'Pot does not match with player bet')

    def test_addCard(self):
        self.table.add_card()
        self.assertEqual(len(self.table.board), 1, 'adding card does not add a card to the board correctly')
    
    def test_roundStats(self):
        self.p1.bet(100)
        self.p1.bet(100)
        self.p1.check()
        self.p1.call()
        self.p1.fold()
        self.p1.all_in()
        output =    {
            'bet': 2,
            'raise': 0,
            'call': 1,
            'check': 1,
            'all-in': 1,
            'fold': 1
        }
        self.assertEqual(self.table.round_stats, output, 'Incoherent round stats')
    
    def test_roundStatsReset(self):
        self.p1.bet(100)
        self.p1.bet(100)
        self.p1.check()
        self.p1.call()
        self.p1.fold()
        self.table.reset()
        self.p1.bet(100)
        output =    {
            'bet': 1,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }

    def test_gameStats(self):
        self.p1.bet(100)
        self.p1.bet(100)
        self.p1.all_in()
        self.table.end()                            # Player leave table
        self.p1 = Player('Player1', self.table)     # Players rejoin table. Game stats should have reset
        self.p1.bet(100)
        output =    {
            'bet': 1,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.assertEqual(self.table.round_stats, output, 'Incoherent round stats')
    
    def test_lastMoveBet(self):
        self.p1.bet(100)
        self.assertEqual(self.table.last_move, [self.p1,'bet'], 'Incoherent last move')

    def test_lastMoveFold(self):
        self.p1.fold()
        self.assertEqual(self.table.last_move, [self.p1,'fold'], 'Incoherent last move')

    def test_lastMoveAllIn(self):
        self.p1.all_in()
        self.assertEqual(self.table.last_move, [self.p1,'all-in'], 'Incoherent last move')

    def test_lastMoveCheck(self):
        self.p1.check()
        self.assertEqual(self.table.last_move, [self.p1,'check'], 'Incoherent last move')

    def test_lastMoveCall(self):
        self.p1.call()
        self.assertEqual(self.table.last_move, [self.p1,'call'], 'Incoherent last move')

# ---
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', self.table)

    def tearDown(self):
        self.table.end()

# ---
class TestBetterBot(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Better('Player1', self.table)
    
    def tearDown(self):
        self.table.end()
    


if __name__ == "__main__":
    unittest.main()

    # deck = Deck()
    # table = Table(deck)
    # scary_cat = ScaryCat('ScaryCat', table)
    # better = Better('Better', table)
    # assert scary_cat.name == 'ScaryCat'

    # # --- Test 1 ---
    # table.pre_flop()        # Pre-flop
    # for i in range(2):
    #     scary_cat.receive(table.deck.draw())
    #     table.deck.burn
    #     better.receive(table.deck.draw())
    # better.play()                           # Better bot plays (bets 99)
    # better.play()                           # Better bot plays (bets 99)
    # assert better.balance == 1000-99*2
    # assert table.pot == 99*2
    # for i in range(9):
    #     better.play()
    # assert better.balance == 0              # Check if all stats match
    # assert table.game_stats['bet'] == 10
    # assert table.game_stats['all-in'] == 1
    # assert better.stats['all-in'] == 1
    # assert better.stats['bet'] == 10
    # table.reset()
    # assert table.round_stats['bet'] == 0        # Round stats should be reset.
    # assert table.round_stats['all-in'] == 0
    # assert table.game_stats['bet'] == 10        # Game stats shouldn't be reset.
    # assert table.game_stats['all-in'] == 1
    # table.end()
    # assert not table.players

    # # --- Test 2 ---
    # table.pre_flop()
    # assert len(table.board) == 3
    # assert table.state == 0
    # table.flop()
    # assert len(table.board) == 3
    # table.turn()
    # assert len(table.board) == 4
    # table.river()
    # assert len(table.board) == 5        # Check if table has 5 cards after river
    # table.reset()
    # for player in table.players:        # Check that all cards have been cleared
    #     assert not player.hand()
    # assert not table.board              # Check that there is nothing on the board.
    # table.end()
    # assert not table.players            # Check if players have been cleared

    # # --- Test 3 ---
    


    # # --- End tests ---
    # print('################')
    # print('All tests passed')
