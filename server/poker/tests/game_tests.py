import sys
import unittest
from ..classes.bots import *
from ..classes.cards import *
from ..classes.game import *

# ---
class TestTableMethods(unittest.TestCase):
    def setUp(self):            # Run this for every unit test
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()

    def test_boardSize_preflop(self):
        self.assertEqual(len(self.table.board),3,'Incorrect number of cards on board')

    def test_boardSize_flop(self):
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 3, 'Incorrect number of cards on board')

    def test_boardSize_turn(self):
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 4, 'Incorrect number of cards on board')

    def test_boardSize_river(self):
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 5, 'Incorrect number of cards on board')
    
    def test_playerBetIncreasesPot(self):
        self.p1.bet(100)
        self.assertEqual(self.table.pot,100,'Pot does not match with player bet')

    def test_addCard(self):
        self.table.add_card()
        self.assertEqual(len(self.table.board), 4, 'adding card does not add a card to the board correctly')
    
    def test_lastMoveBet(self):
        self.p1.bet(100)
        self.assertEqual(self.table.last_move, [self.p1.name,'bet'], 'Incoherent last move')

    def test_lastMoveFold(self):
        self.p1.fold()
        self.assertEqual(self.table.last_move, [self.p1.name,'fold'], 'Incoherent last move')

    def test_lastMoveCheck(self):
        self.p1.check()
        self.assertEqual(self.table.last_move, [self.p1.name,'check'], 'Incoherent last move')

    def test_lastMoveCall(self):
        self.p1.call()
        self.assertEqual(self.table.last_move, [self.p1.name,'call'], 'Incoherent last move')
    
    def test_playersOnTable(self):
        self.p2 = Player('p2', False, self.table)
        self.p3 = Player('p3', False, self.table)
        self.assertEqual([self.p1, self.p2, self.p3], self.table.players, 'Incorrect players on table')


# ---
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()
    
    def test_playerInTable(self):
        self.assertIn(self.p1, self.table.players, 'Players not included by table')
    
    def test_playerStatBet(self):
        self.p1.bet(100)
        d1 = {
            'bet': 1,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p1.stats, 'Incoherent game stats (bet)')

    def test_playerStatFold(self):
        self.p1.fold()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 1
        }
        self.assertDictEqual(d1, self.p1.stats, 'Incoherent game stats (fold)')

    def test_playerStatCheck(self):
        self.p1.check()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 1,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p1.stats, 'Incoherent game stats (check)')

    def test_playerStatCall(self):
        self.p1.call()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 1,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p1.stats, 'Incoherent game stats (call)')
    
    # def test_aggroFactorOnlyBet(self):
    #     for i in range(5):
    #         for j in range(5):
    #             self.p1.bet(1)          # Any amount of p1 bets won't change aggro factor as long as no calls have been made
    #         self.assertEqual(self.p1.aggro_factor, 0, 'Aggression factor is incorrect')
    
    # def test_aggroFactorBetWithCallEqualProportion(self):
    #     for j in range(5):
    #         self.p1.bet(1)
    #         self.p1.call()
    #     self.assertAlmostEqual(self.p1.aggro_factor, 1, 3, 'Aggression factor incorrect')

    # def test_aggroFactorBetWithCall5050Proportion(self):
    #     for j in range(5):
    #         self.p1.bet(1)
    #         self.p1.call()
    #         self.p1.call()
    #     self.assertAlmostEqual(self.p1.aggro_factor, 0.5, 3, 'Aggression factor incorrect')

    # def test_aggroFrequencyNoActions(self):
    #     self.assertAlmostEqual(self.p1.aggro_frequency, 0, 3, 'Aggression frequency incorrect')
    
    # def test_aggroFrequencyOnlyBets(self):
    #     for i in range(5):
    #         self.p1.bet(1)
    #     self.assertAlmostEqual(self.p1.aggro_frequency, 100, 3, 'Aggression frequency incorrect')

    def test_receivingCards(self):
        deck2 = Deck()
        self.p1.receive(deck2.get('As'))
        self.assertEqual(self.p1.hand()[-1], deck2.get('As'), 'Player hand does not match what is received')
    
    def test_clearingHand(self):
        self.p1.receive(self.table.deck.get('As'))
        self.p1.clear_hand()
        self.assertFalse(self.p1.hand(), 'Clearing player hand does not function properly')


# ------------------------- #
# --- HAND EVAL TESTING --- #
# ------------------------- #
class TestFlush(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_case1(self):
        cards = ['As', 'Ks', 'Qs', 'Ts', '9s']
        expectedResult = (5, "[As, Ks, Qs, Ts, 9s]")
        result = Player.handEval([self.deck.get(cards[0]), self.deck.get(cards[1]), self.deck.get(cards[2]), self.deck.get(cards[3]), self.deck.get(cards[4])])
        self.assertTupleEqual(result, expectedResult)

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
