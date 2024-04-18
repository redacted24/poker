import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *

# ---
class TestTableMethods(unittest.TestCase):
    # Tests are on a table of 4 players
    def setUp(self):            # Run this for every unit test
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('p1', False, self.table)
        self.p2 = Player('p2', False, self.table)
        self.p3 = Player('p3', False, self.table)
        self.p4 = Player('p4', False, self.table)

    def tearDown(self):
        self.table.end()
    
    def test_playerBetIncreasesPot(self):
        self.table.pre_flop()
        self.p4.bet(100)
        self.assertEqual(self.table.pot,115,'Pot does not match with player bet')

    def test_addCard(self):
        self.table.pre_flop()
        self.table.add_card()
        self.assertEqual(len(self.table.board), 4, 'adding card does not add a card to the board correctly')
    
    def test_lastMoveBet(self):
        self.table.pre_flop()
        self.p4.bet(100)
        self.assertEqual(self.table.last_move, [self.p4.name,'bet'], 'Incoherent last move')

    def test_lastMoveFold(self):
        self.table.pre_flop()
        self.p4.fold()
        self.assertEqual(self.table.last_move, [self.p4.name,'fold'], 'Incoherent last move')

    def test_lastMoveCheck(self):
        self.table.pre_flop()
        self.p4.check()
        self.assertEqual(self.table.last_move, [self.p4.name,'check'], 'Incoherent last move')

    def test_lastMoveCall(self):
        self.table.pre_flop()
        self.p4.call()
        self.assertEqual(self.table.last_move, [self.p4.name,'call'], 'Incoherent last move')
    
    def test_playersOnTable(self):
        self.table.pre_flop()
        self.assertEqual([self.p1, self.p2, self.p3, self.p4], self.table.players, 'Incorrect players on table')
    
    def test_tablePotIncrease(self):
        self.table.pre_flop()       # Already increases pot by 15 because of small blind and big blind
        self.table.increase_pot(10)
        self.assertEqual(self.table.pot, 25, 'Pot increase is not coherent with table')
    
    def test_tableBurn(self):
        self.table.burn()
        self.assertEqual(len(self.table.deck), 51, 'Burn method does not work')



# ---
class testBoardMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)
        self.p2 = Player('Player2', False, self.table)
        self.p3 = Player('Player3', False, self.table)
        self.p4 = Player('Player4', False, self.table)
    
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
        self.table.board.clear()
        self.assertFalse(self.table.board.cards())



# ---
class TestPlayerMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('Player1', False, self.table)
        self.p2 = Player('p2', False, self.table)
        self.p3 = Player('p3', False, self.table)
        self.p4 = Player('p4', False, self.table)

    def tearDown(self):
        self.table.end()
    
    def test_playerInTable(self):
        self.table.pre_flop()
        self.assertIn(self.p1, self.table.players, 'Players not included by table')
    
    def test_playerStatBet(self):
        self.table.pre_flop()
        self.p4.bet(100)
        d1 = {
            'bet': 1,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p4.stats, 'Incoherent game stats (bet)')

    def test_playerStatFold(self):
        self.table.pre_flop()
        self.p4.fold()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 0,
            'all-in': 0,
            'fold': 1
        }
        self.assertDictEqual(d1, self.p4.stats, 'Incoherent game stats (fold)')

    def test_playerStatCheck(self):
        self.table.pre_flop()
        self.p4.check()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 0,
            'check': 1,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p4.stats, 'Incoherent game stats (check)')

    def test_playerStatCall(self):
        self.table.pre_flop()
        self.p4.call()
        d1 = {
            'bet': 0,
            'raise': 0,
            'call': 1,
            'check': 0,
            'all-in': 0,
            'fold': 0
        }
        self.assertDictEqual(d1, self.p4.stats, 'Incoherent game stats (call)')
    
    def test_playerFoldPoppedOutOfQueue(self):
        '''Verify that player folding actually pops them out of the table player queue.'''
        self.table.pre_flop()
        self.p4.fold()
        self.assertListEqual(self.table.player_queue,[self.p1, self.p2, self.p3])       # Player queue should be an empty list [] which would be falsy
    
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
    
    def test_receivingCards(self):
        deck2 = Deck()
        self.p1.receive(deck2.get('As'))
        self.assertEqual(self.p1.hand()[-1], deck2.get('As'), 'Player hand does not match what is received')
    
    def test_clearingHand(self):
        self.p1.receive(self.table.deck.get('As'))
        self.p1.clear_hand()
        self.assertFalse(self.p1.hand(), 'Clearing player hand does not function properly')
    
    def test_activePlayersFold(self):
        self.table.pre_flop()
        self.p4.fold()
        self.assertListEqual(self.table.player_queue, [self.p1, self.p2, self.p3])
    
    def test_activePlayers(self):
        self.table.pre_flop()
        self.assertListEqual(self.table.active_players(), [self.p1, self.p2, self.p3, self.p4])



# ---
class TestAdvancedBotMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1','moderate', self.table)
        self.p2 = AdvancedBot('p2','loose', self.table)
        self.p3 = AdvancedBot('p3','moderate', self.table)
        self.p4 = AdvancedBot('p4','tight', self.table)
    
    def tearDown(self):
        self.table.end()
    
    def test_get_income_rate1(self):
        '''Test the get_income_rate method to check if it returns the correct IR.'''
        self.p1.receive([self.deck.get('As'), self.deck.get('Ks')])
        self.assertEqual(self.p1.get_income_rate(), 655, 'Incorrect IR')
    
    def test_get_income_rate_edgeCase1(self):
        '''Top left of self.income_rates'''
        self.p1.receive([self.deck.get('2s'), self.deck.get('2d')])
        self.assertEqual(self.p1.get_income_rate(), -121, 'Incorrect IR')

    def test_get_income_rate_edgeCase2(self):
        '''Top right of self.income_rates'''
        self.p1.receive([self.deck.get('As'), self.deck.get('2d')])
        self.assertEqual(self.p1.get_income_rate(), 16, 'Incorrect IR')

    def test_get_income_rate_edgeCase3(self):
        '''Bottom left of self.income_rates'''
        self.p1.receive([self.deck.get('As'), self.deck.get('2s')])
        self.assertEqual(self.p1.get_income_rate(), 175, 'Incorrect IR')

    def test_get_income_rate_edgeCase4(self):
        '''Bottom right of self.income_rates'''
        self.p1.receive([self.deck.get('As'), self.deck.get('Ad')])
        self.assertEqual(self.p1.get_income_rate(), 1554, 'Incorrect IR')
    
    def test_botPositionCase1(self):
        '''Check if player threshold position is well computed'''
        self.table.pre_flop()
        self.p2.update_player_position()
        self.assertEqual(self.p2.thresholds_position, 1)
        self.assertEqual(self.p3.thresholds_position, 0)
        self.assertEqual(self.p4.thresholds_position, 3)
        self.assertEqual(self.p1.thresholds_position, 2)

    def test_botPositionFail(self):
        '''Check if func works if board is not set'''
        self.assertRaises(ValueError, lambda: self.p4.update_player_position())     # Use lambda as wrapper
    
    def test_strategyThresholdsModerate(self):
        # p4 has been defined as a moderate bot in the setUp()
        # threshold position of p4 should be 3
        self.table.pre_flop()
        self.p4.update_player_position()        # Threshold position should be 3
        self.p4.update_strategy_thresholds()
        with self.subTest('case 1: make1'):
            self.assertEqual(self.p4.strategy_thresholds['make1'], 100)
        with self.subTest('case 2: make2'):
            self.assertEqual(self.p4.strategy_thresholds['make2'], 200)
        with self.subTest('case 3: make4'):
            self.assertEqual(self.p4.strategy_thresholds['make4'], 300)

    def test_strategyThresholdsTight(self):
        # p1 has been defined as a tight bot in the setUp()
        # threshold position of p1 should be 2
        self.table.pre_flop()
        self.p1.update_player_position()
        self.p1.update_strategy_thresholds()
        with self.subTest('case 1: make1'):
            self.assertEqual(self.p1.strategy_thresholds['make1'], 50)
        with self.subTest('case 2: make2'):
            self.assertEqual(self.p1.strategy_thresholds['make2'], 250)
        with self.subTest('case 3: make4'):
            self.assertEqual(self.p1.strategy_thresholds['make4'], 300)

    def test_strategyThresholdsLoose(self):
        # p3 has been defined as a loose bot in the setUp()
        # threshold position of p3 should be 0 (because they are the last player)
        self.table.pre_flop()
        self.p3.update_player_position()
        self.p3.update_strategy_thresholds()
        with self.subTest('case 1: make1'):
            self.assertEqual(self.p3.strategy_thresholds['make1'], -50)
        with self.subTest('case 2: make2'):
            self.assertEqual(self.p3.strategy_thresholds['make2'], 0)
        with self.subTest('case 3: make4'):
            self.assertEqual(self.p3.strategy_thresholds['make4'], 300)
    


# --- Testing game situations and playing methods
@unittest.skipIf(AdvancedBot.preflop_strategy_values!={
        'tight': {'make1': (50, 50), 'make2': (200, 50), 'make4': (580,0)},
        'moderate': {'make1': (50, 25), 'make2': (200, 25), 'make4': (580,0)},
        'loose': {'make1': (50, 10), 'make2': (200, 10), 'make4': (580,0)}
    },'modifying thresholds renders these tests useless')    # skipping for now because modifying thresholds
class TestAdvancedBotMethods(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'moderate', self.table)
        self.p2 = AdvancedBot('p2', 'moderate', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = AdvancedBot('p4', 'moderate', self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()

    def test_call_1_case1(self):
        '''Test call1 method when another player has bet on the table + bot is the last to play. Bot should call'''
        self.p4.bet(20)
        self.assertEqual(self.p1.call1(),'call')

    def test_call_1_case2(self):
        '''Test call1 method when two other players have bet on the table + bot is the last to play. Bot should fold'''
        self.p4.bet(100)
        self.p1.bet(110)
        self.assertEqual(self.p2.call1(), 'fold')       # Two players have bet, and call1 specifies to fold if there are more than or equal to two bets on the board.

    def test_call_1_case3(self):
        '''Test call1 method when no other players have bet on the table + bot is the last to play. Bot should call (because there is minimum payment)'''
        # Technically, bot should check if they are big blind. However, that has not been added yet, so this will suffice. Please remove this comment and modify test when big blind is integrated
        self.p4.call()
        self.p1.call()
        self.assertEqual(self.p2.call1(), 'call') 

    def test_make1_case1(self):
        '''Test make1 method when no players have bet on the table + bot is the last to play. Bot should bet'''
        self.p4.call()
        self.p1.call()
        self.assertEqual(self.p2.make1(), 'bet')

    def test_make1_case2(self):
        '''Test make1 method when one player has bet on the table + bot is the last to play. Bot should call'''
        self.p4.call()
        self.p1.bet(100)
        self.assertEqual(self.p2.make1(), 'call')
    
    def test_make1_case3(self):
        '''Test make1 method when two players have bet on the table + bot is the last to play. Bot should fold'''
        self.p4.bet(20)
        self.p1.bet(10)
        self.assertEqual(self.p2.make1(), 'fold')

    def test_call2_case1(self):
        '''Test make1 method when two players have bet on the table + bot is the last to play. Bot should call'''
        self.p4.bet(20)
        self.p1.bet(10)
        self.assertEqual(self.p2.call2(), 'call')

    def test_call2_case2(self):
        '''Test make1 method when one player has bet on the table + bot is the last to play. Bot should call'''
        self.p4.call()
        self.p1.bet(20)
        self.assertEqual(self.p2.call2(), 'call')
        
    def test_make2_case1(self):
        '''Test make2 method when no one has bet + bot is the last to play. Bot should bet'''
        self.p4.check()
        self.p1.check()
        self.assertEqual(self.p2.make2(), 'bet')

    def test_make2_case1(self):
        '''Test make2 method when one bot has bet + bot is the last to play. Bot should bet'''
        self.p4.fold()
        self.p1.bet(10)
        self.assertEqual(self.p2.make2(), 'bet')
    
    def test_make4_case1(self):
        self.p4.call()
        self.p1.bet(20)
        self.assertEqual(self.p2.make2(), 'bet')
        self.p3.call()
        self.p4.bet(100)
        self.assertEqual(self.p1.make4(), 'bet')
    
    def test_blindRotation_case1(self):
        self.p4.call()
        self.p1.call()
        self.assertEqual(self.p2.position, 1, 'p2 should be small blind here')
    
    def test_blindRotation_case2(self):
        '''Test player positions after certain rounds are played'''
        self.table.pre_flop()
        self.p4.call()
        self.p1.call()
        self.p2.call()
        self.p3.check()
        self.table.reset()
        self.table.pre_flop()
        self.assertEqual(self.p1.position,1)
        self.assertEqual(self.p2.position,2)
        self.assertEqual(self.p3.position,3)
        self.assertEqual(self.p4.position,0)
        self.p3.call()
        self.p4.call()
        self.p1.call()
        self.p2.check()
        self.table.reset()
        self.table.pre_flop()
        self.assertEqual(self.p1.position,2)
        self.assertEqual(self.p2.position,3)
        self.assertEqual(self.p3.position,0)
        self.assertEqual(self.p4.position,1)
        self.p2.call()
        self.p3.call()
        self.p4.call()
        self.p1.check()
        self.table.reset()
        self.table.pre_flop()
        self.assertEqual(self.p1.position,3)
        self.assertEqual(self.p2.position,0)
        self.assertEqual(self.p3.position,1)
        self.assertEqual(self.p4.position,2)



# ---
@unittest.skipIf(AdvancedBot.preflop_strategy_values!={
        'tight': {'make1': (50, 50), 'make2': (200, 50), 'make4': (580,0)},
        'moderate': {'make1': (50, 25), 'make2': (200, 25), 'make4': (580,0)},
        'loose': {'make1': (50, 10), 'make2': (200, 10), 'make4': (580,0)}
    },'modifying thresholds renders these tests useless')
class TestAdvancedBotPlaySituations(unittest.TestCase):
    '''Test game cases'''
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = AdvancedBot('p1', 'moderate', self.table)
        self.p2 = AdvancedBot('p2', 'moderate', self.table)
        self.p3 = AdvancedBot('p3', 'moderate', self.table)
        self.p4 = AdvancedBot('p4', 'moderate', self.table)
        self.table.pre_flop()

    def tearDown(self):
        self.table.end()

    def test_smallBlindPreFlopPlayMake0(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        2 7 offsuit IR = -432
        Make 0 threshold: under call1, or <= -75'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('2s'), deck2.get('7d')])
        self.assertEqual(self.p2.play(),'make0') 

    def test_smallBlindPreFlopPlayCall1(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Call 1 threshold: fixed, 75 >= x >= -75
        5 J suited IR = -12'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('5s'), deck2.get('Js')])
        self.assertEqual(self.p2.play(),'call1')

    def test_smallBlindPreFlopPlayMake1(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make1 threshold: 225 >= x >= 75
        6 A unsuited IR = 99'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('As'), deck2.get('6d')])
        self.assertEqual(self.p2.play(),'make1')

    def test_smallBlindPreFlopPlayCall2(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Call2 threshold (fixed): 225 >= x >= 200
        A 3 suited IR = 211'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('As'), deck2.get('3s')])
        self.assertEqual(self.p2.play(),'call2')

    def test_smallBlindPreFlopPlayMake2(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make2 threshold: 580 >= x >= 225
        A 4 suited IR = 237'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('As'), deck2.get('4s')])
        self.assertEqual(self.p2.play(),'make2') 

    def test_smallBlindPreFlopPlayMake4(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make4 threshold: x >= 580
        A A IR = 1554'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('As'), deck2.get('Ad')])
        self.assertEqual(self.p2.play(),'make4') 

    def test_smallBlindPreFlopOtherTests1(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        6 5 suited IR = -52'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.clear_hand()
        self.p2.receive([deck2.get('5s'), deck2.get('6s')])
        self.assertEqual(self.p2.play(),'call1')

    def test_Make0(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make0: 
        6 5 suited IR = -52'''
        deck2 = Deck()
        self.table.pre_flop()
        self.p4.clear_hand()
        self.p4.receive([deck2.get('5s'), deck2.get('6s')])
        self.assertEqual(self.p4.play(),'make0') 

    def test_bigBlindPreFlopMake0(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make0 = x <= 50
        6 5 suited IR = -52'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.call()
        self.p3.clear_hand()
        self.p3.receive([deck2.get('5s'), deck2.get('6s')])
        self.assertEqual(self.p3.play(),'make0') 

    def test_bigBlindPreFlopMake1(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make1 = 200 > x >= 50
        7 8 suited IR = 66'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.call()
        self.p3.clear_hand()
        self.p3.receive([deck2.get('7s'), deck2.get('8s')])
        self.assertEqual(self.p3.play(),'make1')

    def test_bigBlindPreFlopMake2(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make2 = 200 <= x < 580
        9 A suited IR = 381'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.call()
        self.p3.clear_hand()
        self.p3.receive([deck2.get('9s'), deck2.get('As')])
        self.assertEqual(self.p3.play(),'make2')

    def test_bigBlindPreFlopMake4(self):
        '''
        Moderate bot
        Queue: p3,p4,p1,p2
        Sb: p1
        Bb: p2
        Make2 = x >= 580
        A Q suited IR = 594'''
        deck2 = Deck()
        self.p4.call()
        self.p1.call()
        self.p2.call()
        self.p3.clear_hand()
        self.p3.receive([deck2.get('Qs'), deck2.get('As')])
        self.assertEqual(self.p3.play(),'make4')

    def test_onlyBets(self):
        '''Specific testing for make4 strat'''
        # Queue: p4,p1,p2,p3
        print('GAMEEEEEEEEEEEEEE start ----------------------')
        deck2 = Deck()
        self.p4.clear_hand()
        self.p4.receive([deck2.get('As'), deck2.get('Ks')])
        self.p3.clear_hand()
        self.p3.receive([deck2.get('Ad'), deck2.get('Kd')])
        self.p2.clear_hand()
        self.p2.receive([deck2.get('Ac'), deck2.get('Kc')])
        self.p1.clear_hand()
        self.p1.receive([deck2.get('Ah'), deck2.get('Kh')])
        self.table.play()
        print(self.table.round_stats)
        print('game end -------------------------')

    def test_fullGame(self):
        '''Specific testing for make4 strat'''
        # Queue: p4,p1,p2,p3
        print('GAMEEEEEEEEEEEEEE start ----------------------')
        self.table.play()
        print(self.table.round_stats)
        print('game end -------------------------')
        

# ------------------------- #
# --- HAND EVAL TESTING --- #
# ------------------------- #
class TestHandEval(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table(self.deck)
        self.p1 = Player('test', False, self.table)
        self.p2 = Player('p2', False, self.table)
        self.p3 = Player('p3', False, self.table)

    def test_RoyalFlush(self):
        with self.subTest('case 1'):
            cards = ['4d', '6s', 'Kd', 'Qd', 'Ad', 'Td', 'Jd']
            expectedResult = (10, [self.deck.get(card) for card in ['Ad', 'Kd', 'Qd', 'Jd', 'Td']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['4c', 'Qd', 'Ad', 'Kd', '7h', 'Td', 'Jd']
            expectedResult = (10, [self.deck.get(card) for card in ['Ad', 'Kd', 'Qd', 'Jd', 'Td']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['5d', 'Ac', 'Tc', 'Kc', 'Qc', 'Jc', '9h']
            expectedResult = (10, [self.deck.get(card) for card in ['Ac', 'Kc', 'Qc', 'Jc', 'Tc']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['Jh', 'Th', 'Kh', 'Qh', 'Ah', '2s', '5c']
            expectedResult = (10, [self.deck.get(card) for card in ['Ah', 'Kh', 'Qh', 'Jh', 'Th']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['Qd', 'Ad', 'Kd', 'Td', 'Jd', '7h', '4c']
            expectedResult = (10, [self.deck.get(card) for card in ['Ad', 'Kd', 'Qd', 'Jd', 'Td']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)
    
    def test_StraightFlush(self):
        with self.subTest('case 1'):
            cards = ['3d', '4d', '6d', '5d', '7d', '9h', '2c']
            expectedResult = (9, [self.deck.get(card) for card in ['7d', '6d', '5d', '4d', '3d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['9d', '3c', '5s', '7s', '4s', '6s', '8s']
            expectedResult = (9, [self.deck.get(card) for card in ['8s', '7s', '6s', '5s', '4s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['Ts', '6s', '7s', '3h', '9s', '2d', '8s']
            expectedResult = (9, [self.deck.get(card) for card in ['Ts', '9s', '8s', '7s', '6s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['Qc', '8c', '9c', 'Jc', '6s', '4h', 'Tc']
            expectedResult = (9, [self.deck.get(card) for card in ['Qc', 'Jc', 'Tc', '9c', '8c']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['6c', 'Ah', '4h', '2h', '5h', '3h', 'Qc']
            expectedResult = (9, [self.deck.get(card) for card in ['5h', '4h', '3h', '2h', 'Ah']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_FourOfAKind(self):
        with self.subTest('case 1'):
            cards = ['As', 'Ad', 'Ac', 'Ah', 'Qd', 'Ks', 'Js']
            expectedResult = (8, [self.deck.get(card) for card in ['As', 'Ad', 'Ac', 'Ah', 'Ks']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['7c', 'Ks', '7d', '7h', 'Js', '7s', 'Qd']
            expectedResult = (8, [self.deck.get(card) for card in ['7d', '7h', '7c', '7s', 'Ks']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['2h', '9c', '5d', '9h', '9s', '9d', 'Qd']
            expectedResult = (8, [self.deck.get(card) for card in ['9c', '9d', '9h', '9s', 'Qd']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['Td', 'Tc', '5s', 'Th', 'Ks', 'Qd', 'Ts']
            expectedResult = (8, [self.deck.get(card) for card in ['Td', 'Tc', 'Th', 'Ts', 'Ks']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['7c', 'Kh', '7h', '7s', '7d', 'Ks', 'Kd']
            expectedResult = (8, [self.deck.get(card) for card in ['7c', '7d', '7h', '7s', 'Ks']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_FullHouse(self):
        with self.subTest('case 1'):
            cards = ['Td', 'Tc', '5s', 'Th', '5d', 'Qd', 'Qs']
            expectedResult = (7, [self.deck.get(card) for card in ['Td', 'Th', 'Ts', 'Qd', 'Qs']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['7c', '5d', '8s', '7s', '8d', '7h', 'Qd']
            expectedResult = (7, [self.deck.get(card) for card in ['7c', '7d', '7h', '8s', '8d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['3d', 'Jc', '3s', '3h', 'Ks', 'Kc', 'Kd']
            expectedResult = (7, [self.deck.get(card) for card in ['Ks', 'Kc', 'Kd', '3s', '3d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['9c', '2h', '9d', '9h', '2s', '2s', 'Qd']
            expectedResult = (7, [self.deck.get(card) for card in ['9c', '9d', '9h', '2h', '2s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['5s', '5d', '2s', '2d', '2h', 'Qs', 'As']
            expectedResult = (7, [self.deck.get(card) for card in ['2s', '2d', '2h', '5s', '5d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 6'):
            cards = ['6s', 'Ks', 'Kd', '6d', '6h', 'Qh', '3c']
            expectedResult = (7, [self.deck.get(card) for card in ['6s', '6d', '6h', 'Ks', 'Kd']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_Flush(self):
        with self.subTest('case 1'):
            cards = ['4d', '6d', '7d', 'Qd', '2d', '5s', '9c']
            expectedResult = (6, [self.deck.get(card) for card in ['Qd', '7d', '6d', '4d', '2d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['8c', '2c', 'Kc', '7c', '3c', 'Kh', 'Kd']
            expectedResult = (6, [self.deck.get(card) for card in ['Kc', '8c', '7c', '3c', '2c']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['5h', '3h', '7h', 'Ah', 'Th', '4d', '2h']
            expectedResult = (6, [self.deck.get(card) for card in ['Ah', 'Th', '7h', '5h', '3h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['5h', '3h', '7h', 'Ah', 'Th', '4d', '2h']
            expectedResult = (6, [self.deck.get(card) for card in ['Ah', 'Th', '7h', '5h', '3h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['7s', '9s', 'Qs', '2d', 'Ks', 'Js', 'Th']
            expectedResult = (6, [self.deck.get(card) for card in ['Ks', 'Qs', 'Js', '9s', '7s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_Straight(self):
        with self.subTest('case 1'):
            cards = ['2s', '3d', '6c', '4h', '5s', '7d', '8h']
            expectedResult = (5, [self.deck.get(card) for card in ['8h', '7d', '6c', '5s', '4h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['4d', '7c', '4s', '5c', '5d', '6d', '8c']
            expectedResult = (5, [self.deck.get(card) for card in ['8c', '7c', '6d', '5c', '4d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['8d', '9h', 'Js', 'Th', 'Jd', 'Jh', '7h']
            expectedResult = (5, [self.deck.get(card) for card in ['Js', 'Ts', '9h', '8d', '7h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['2h', '9d', '4c', '8s', '5h', '3s', 'Ad']
            expectedResult = (5, [self.deck.get(card) for card in ['5h', '4c', '3s', '2h', 'Ad']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['5d', '9c', '7h', '4c', 'Td', '6s', '8h']
            expectedResult = (5, [self.deck.get(card) for card in ['Td', '9c', '8h', '7h', '6s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_ThreeOfAKind(self):
        with self.subTest('case 1'):
            cards = ['4d', '6s', '4c', 'Kd', 'Ad', '4s', 'Jd']
            expectedResult = (4, [self.deck.get(card) for card in ['4d', '4c', '4s', 'Ad', 'Kd']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['6h', '7s', '9s', '9d', '9h', '8c', '3d']
            expectedResult = (4, [self.deck.get(card) for card in ['9s', '9h', '9d', '8c', '7s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['As', '2c', 'Ad', '4d', 'Ac', '9s', '8h']
            expectedResult = (4, [self.deck.get(card) for card in ['As', 'Ad', 'Ac', '9s', '8h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['Ts', '3h', '4d', '8c', '4c', '4s', 'Qd']
            expectedResult = (4, [self.deck.get(card) for card in ['4d', '4c', '4s', 'Qd', 'Ts']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['Qd', 'Kc', '3h', 'Jc', 'Ks', 'Kd', '8c']
            expectedResult = (4, [self.deck.get(card) for card in ['Kc', 'Ks', 'Kd', 'Qd', 'Jc']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)
    
    def test_TwoPairs(self):
        with self.subTest('case 1'):
            cards = ['2s', '6h', '4d', '7c', '8d', '2c', '7s']
            expectedResult = (3, [self.deck.get(card) for card in ['7c', '7s', '2s', '2c', '8d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['3h', '4s', 'Qd', 'As', 'Jc', '4c', '3s']
            expectedResult = (3, [self.deck.get(card) for card in ['4s', '4c', '3h', '3s', 'As']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['Jh', 'Ad', '5s', '7c', 'Td', '5h', '7d']
            expectedResult = (3, [self.deck.get(card) for card in ['7c', '7d', '5s', '5h', 'Ad']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['5d', '6s', '5h', 'Kc', 'Js', '6h', 'Kd']
            expectedResult = (3, [self.deck.get(card) for card in ['Kc', 'Kd', '6s', '6h', 'Js']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['8s', '3h', '2d', 'Qh', 'Ts', '3c', '8d']
            expectedResult = (3, [self.deck.get(card) for card in ['8s', '8d', '3h', '3c', 'Qh']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def test_OnePair(self):
        with self.subTest('case 1'):
            cards = ['2d', '6s', 'Kh', 'Qd', 'Ad', 'Ks', 'Td']
            expectedResult = (2, [self.deck.get(card) for card in ['Kd', 'Ks', 'Ad', 'Qd', 'Td']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['Jd', '4h', '5c', '9s', '2h', '6c', '5h']
            expectedResult = (2, [self.deck.get(card) for card in ['5c', '5h', 'Jd', '9s', '6c']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['9s', '3d', '8h', '6d', 'Kd', '8d', '2c']
            expectedResult = (2, [self.deck.get(card) for card in ['8h', '8d', 'Kd', '9s', '6d']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['8h', '7d', '4c', '3d', '7c', '2h', '6d']
            expectedResult = (2, [self.deck.get(card) for card in ['7d', '7c', '8h', '6d', '4c']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['6d', 'Ac', '2h', '7d', '5h', '3s', '7s']
            expectedResult = (2, [self.deck.get(card) for card in ['7d', '7s', 'Ac', '6d', '5h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

    def testHighCard(self):
        with self.subTest('case 1'):
            cards = ['2h', 'Qd', 'As', '3c', '5s', '8d', 'Jh']
            expectedResult = (1, [self.deck.get(card) for card in ['As', 'Qd', 'Jh', '8d', '5s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 2'):
            cards = ['3s', 'Jd', '9c', '2h', '8h', '6s', 'Td']
            expectedResult = (1, [self.deck.get(card) for card in ['Jd', 'Td', '9c', '8h', '6s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 3'):
            cards = ['9h', '6c', 'Ts', 'Qc', '7d', 'Kh', 'Ad']
            expectedResult = (1, [self.deck.get(card) for card in ['Ad', 'Kh', 'Qc', 'Ts', '9h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 4'):
            cards = ['8h', '7c', '5d', '4s', '3h', '2c', '9h']
            expectedResult = (1, [self.deck.get(card) for card in ['9h', '8h', '7c', '5d', '4s']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)

        with self.subTest('case 5'):
            cards = ['Ts', '2c', '5d', '3d', '4h', '7d', '9h']
            expectedResult = (1, [self.deck.get(card) for card in ['Ts', '9h', '7d', '5d', '4h']])
            result = self.p1.handEval([self.deck.get(card) for card in cards])
            self.assertTupleEqual(result, expectedResult)


if __name__ == "__main__":
    unittest.main()
