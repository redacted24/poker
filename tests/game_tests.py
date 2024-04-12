import sys
import unittest
sys.path.append('../poker/server/poker/classes')
from bots import *              # If you have Pylance installed ignore underline

# ---
class TestTableMethods(unittest.TestCase):
    def setUp(self):            # Run this for every unit test
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)

    def tearDown(self):
        self.table.end()

    def test_boardSize_preflop(self):
        self.table.pre_flop()
        self.assertEqual(len(self.table.board),3,'Incorrect number of cards on board')
    
    def test_boardSize_flop(self):
        self.table.pre_flop() 
        self.p1.check()
        self.table.play()
        self.assertEqual(len(self.table.board), 4, 'Incorrect number of cards on the baord (for the flop)')

    def test_onePlayerQueue(self):
        self.table.pre_flop()
        self.assertListEqual(self.table.player_queue, [self.p1])
    
    def test_twoPlayerQueue(self):
        self.p2 = Player('Player2', False, self.table)
        self.table.pre_flop()
        self.assertListEqual(self.table.player_queue, [self.p1, self.p2])

    def test_threePlayerQueue(self):
        self.p2 = Player('Player2', False, self.table)
        self.p3 = Player('Player3', False, self.table)
        self.table.pre_flop()
        self.assertListEqual(self.table.player_queue, [self.p1, self.p2, self.p3])
        
    def test_boardSize_flop(self):
        self.table.pre_flop()
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 3, 'Incorrect number of cards on board')

    def test_boardSize_turn(self):
        self.table.pre_flop()
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 4, 'Incorrect number of cards on board')

    def test_boardSize_river(self):
        self.table.pre_flop()
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.p1.call()
        self.table.play()
        self.assertEqual(len(self.table.board), 5, 'Incorrect number of cards on board')
    
    def test_playerBetIncreasesPot(self):
        self.table.pre_flop()
        self.p1.bet(100)
        self.assertEqual(self.table.pot,100,'Pot does not match with player bet')

    def test_addCard(self):
        self.table.pre_flop()
        self.table.add_card()
        self.assertEqual(len(self.table.board), 4, 'adding card does not add a card to the board correctly')
    
    def test_lastMoveBet(self):
        self.table.pre_flop()
        self.p1.bet(100)
        self.assertEqual(self.table.last_move, [self.p1.name,'bet'], 'Incoherent last move')

    def test_lastMoveFold(self):
        self.table.pre_flop()
        self.p1.fold()
        self.assertEqual(self.table.last_move, [self.p1.name,'fold'], 'Incoherent last move')

    def test_lastMoveCheck(self):
        self.table.pre_flop()
        self.p1.check()
        self.assertEqual(self.table.last_move, [self.p1.name,'check'], 'Incoherent last move')

    def test_lastMoveCall(self):
        self.table.pre_flop()
        self.p1.call()
        self.assertEqual(self.table.last_move, [self.p1.name,'call'], 'Incoherent last move')
    
    def test_playersOnTable(self):
        self.table.pre_flop()
        self.p2 = Player('p2', False, self.table)
        self.p3 = Player('p3', False, self.table)
        self.assertEqual([self.p1, self.p2, self.p3], self.table.players, 'Incorrect players on table')
    
    def test_tablePotIncrease(self):
        self.table.pre_flop()
        self.table.increase_pot(10)
        self.assertEqual(self.table.pot, 10, 'Pot increase is not coherent with table')
    
    def test_tableBurn(self):
        self.table.burn()
        self.assertEqual(len(self.table.deck), 51, 'Burn method does not work')



# ---
class testBoardMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)
    
    def test_boardInitialShowCards(self):
        self.assertFalse(self.table.board._show_cards)
    
    def test_initialBoardLength(self):
        self.assertEqual(len(self.table.board), 0, 'Board should start with zero cards')
    
    def test_boardPlacingCards(self):
        '''Test if board method place_card() works.'''
        with self.subTest('case 1: 1 card'):
            self.table.board.place_card(self.deck.get('As'))
        with self.subTest('case 2: 2 cards'):
            self.table.board.place_card(self.deck.get('Ks'))
        with self.subTest('case 3: 3 cards'):
            self.table.board.place_card(self.deck.get('Qs'))
        
    def test_boardRevealCards(self):
        '''Test if board method reveal() works'''
        self.table.board.reveal()
        self.assertTrue(self.table.board._show_cards)
    
    def test_boardHideCards(self):
        '''Test if board method hide() works'''
        self.table.board.hide()
        self.assertFalse(self.table.board._show_cards)
    
    def test_boardDisplayWhenCardsNotRevealed(self):
        '''Test if board display() method accurately returns a list of False elements if all cards are not revealed'''
        self.table.pre_flop()
        self.assertListEqual(self.table.board.display(), [False, False, False], 'List should only have false elements')
    
    def test_boardDisplayAfterReveal(self):
        '''Test if board display() method accurately returns a list of card names after revealing the cards through reveal() method'''
        self.table.pre_flop()
        self.table.board.reveal()
        for i in self.table.board.display():
            self.assertIsInstance(i, str)       # Everything should be a card name, or a string

    def test_boardDisplayAfterRevealAndHide(self):
        '''Test if board display() method accurately returns a list of card names after revealing then hiding the cards through reveal() and hide() methods'''
        self.table.pre_flop()
        self.table.board.reveal()
        self.table.board.hide()
        for i in self.table.board.display():
            self.assertFalse(i)       # Everything should be false name
        
    def test_boardClear(self):
        '''Test board method clear()'''
        self.table.pre_flop()
        self.table.board.clear()
        self.assertFalse(self.table.board.cards)


# ---
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)

    def tearDown(self):
        self.table.end()
    
    def test_playerInTable(self):
        self.table.pre_flop()
        self.assertIn(self.p1, self.table.players, 'Players not included by table')
    
    def test_playerStatBet(self):
        self.table.pre_flop()
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
        self.table.pre_flop()
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
        self.table.pre_flop()
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
        self.table.pre_flop()
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
    
    def test_playerFoldPoppedOutOfQueue(self):
        '''Verify that player folding actually pops them out of the table player queue.'''
        self.table.pre_flop()
        self.p1.fold()
        self.assertFalse(self.table.player_queue)       # Player queue should be an empty list [] which would be falsy
    
    def test_playerBetOutofTurn(self):
         '''Verify that a player cannot play in the wrong table order.'''
         self.table.pre_flop()
         self.p2 = Player('Player2', False, self.table)
         # Queue should be [p1, p2]
         self.assertRaises(ValueError, lambda:self.p2.bet(1))

    def test_playerFoldOutofTurn(self):
         '''Verify that a player cannot play in the wrong table order.'''
         self.table.pre_flop()
         self.p2 = Player('Player2', False, self.table)
         # Queue should be [p1, p2]
         self.assertRaises(ValueError, lambda:self.p2.fold())

    def test_playerCallOutofTurn(self):
         '''Verify that a player cannot play in the wrong table order.'''
         self.table.pre_flop()
         self.p2 = Player('Player2', False, self.table)
         # Queue should be [p1, p2]
         self.assertRaises(ValueError, lambda:self.p2.call())

    def test_playerCheckOutofTurn(self):
         '''Verify that a player cannot play in the wrong table order.'''
         self.table.pre_flop()
         self.p2 = Player('Player2', False, self.table)
         # Queue should be [p1, p2]
         self.assertRaises(ValueError, lambda:self.p2.check())
        

    
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
    
    def test_activePlayersFold(self):
        self.p2 = Player('p2', False, self.table)
        self.table.pre_flop()
        self.p1.fold()
        self.assertListEqual(self.table.active_players(), [self.p2])
    
    def test_activePlayers(self):
        self.p2 = Player('p2', False, self.table)
        self.table.pre_flop()
        self.assertListEqual(self.table.active_players(), [self.p1, self.p2])


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
    
    @unittest.skip      # Wait for fix
    def test_case2(self):
        cards = ['9s', '2s', '3s', 'As', 'Ts', 'Js', 'Qs']
        expectedResult = (5, "[As, Qs, Js, Ts, 9s]")
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
