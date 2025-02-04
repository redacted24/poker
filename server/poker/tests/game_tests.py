import unittest
from poker.classes.bots import *
from poker.classes.cards import *
from poker.classes.game import *


# ------------------------- #
# --- HAND EVAL TESTING --- #
# ------------------------- #
class TestHandEval(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.table = Table()
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
