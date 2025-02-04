from itertools import combinations
from time import time

from poker.classes.cards import Deck, Cards
from poker.classes.game import Player

class eval():
    def __init__(self, hand, board_cards):
        self.hand = hand
        self.board_cards = board_cards


    def hand_strength(self):
        '''Determine the hand strength of your current cards + cards on the board'''
        p1 = Player('player')
        p1.receive(self.hand)
        p1_rank = p1.handEval(self.board_cards)

        d = Deck(shuffle=False, bad_cards=self.hand + self.board_cards)
        print(d)
        
        win = tie = loss = 0
        for i, c1 in enumerate(d.deck):
            for c2 in d.deck[i+1:]:
                p2 = Player('opponent')
                p2.receive([c1, c2])
                p2_rank = p2.handEval(self.board_cards)

                if p1_rank > p2_rank:
                    win += 1
                elif p1_rank == p2_rank:
                    tie += 1
                else:
                    loss += 1
        
        # print(win, tie, loss)
        return (win + 0.5 * tie) / sum([win, tie, loss])
    
    @staticmethod
    def check_possible_flush(cards):
        suits = {}
        for card in cards:
            suits[card.suit] = suits.get(card.suit, 0) + 1

        return max([suit for suit in suits.values()]) >= 3

    def potential_hand_strength(self, look_ahead, only_ppot=False):
        start = 0
        '''Compute potential hand strength. look_ahead is an integer that specifies the number of cards to look ahead for. On turn, it should be one, and on flop, it should be 2.'''      
        hand_potentials = [[0] * 3 for _ in range(3)]
        
        p1 = Player('player')
        p2 = Player('opponent')

        p1.receive(self.hand)

        p1_rank_5 = p1.handEval(self.board_cards)
        flush_possible_p1 = eval.check_possible_flush(list(self.hand) + self.board_cards)

        d = Deck(shuffle=False, bad_cards=self.hand + self.board_cards)
        computed_p1_ranks = {}
        computed_p2_ranks = {}

        for p2_hand in combinations(d.deck, 2):
            p2.clear_hand()
            p2.receive(list(p2_hand))

            p2_rank_5 = p2.handEval(self.board_cards)
            flush_possible_p2 = eval.check_possible_flush(list(p2_hand) + self.board_cards)

            if p1_rank_5 > p2_rank_5:
                if only_ppot: continue    # ppot does not need cases were we are winning
                
                i = 0           # We are ahead
            elif p1_rank_5 == p2_rank_5:
                i = 1           # We are tied
            else:
                i = 2           # We are behind

            new_d = Deck(shuffle=False, deck=d.deck, bad_cards=list(p2_hand))

            for new_board_cards in combinations(new_d.deck, look_ahead):
                predicted_board_cards = self.board_cards + list(new_board_cards)

                start_i = time()
                hash_p1 = Cards.hash_list(new_board_cards, flush_possible_p1)
                hash_p2 = Cards.hash_list(p2_hand + new_board_cards, flush_possible_p2)
                start += time() - start_i

                if hash_p1 in computed_p1_ranks:
                    p1_rank_7 = computed_p1_ranks[hash_p1]
                else:
                    p1_rank_7 = p1.handEval(predicted_board_cards)
                    computed_p1_ranks[hash_p1] = p1_rank_7

                if hash_p2 in computed_p2_ranks:
                    p2_rank_7 = computed_p2_ranks[hash_p2]
                else:
                    p2_rank_7 = p2.handEval(predicted_board_cards)
                    computed_p2_ranks[hash_p2] = p2_rank_7


                if p1_rank_7 > p2_rank_7:
                    hand_potentials[i][0] += 1
                elif p1_rank_7 == p2_rank_7:
                    hand_potentials[i][1] += 1
                else:
                    hand_potentials[i][2] += 1


        print(hand_potentials)

        try:
            ppot = (hand_potentials[2][0] + hand_potentials[2][1] / 2 + hand_potentials[1][0]) / (sum(hand_potentials[2]) + sum(hand_potentials[1]) / 2)
            if only_ppot:
                npot = 0
            else:
                npot = (hand_potentials[0][2] + hand_potentials[0][1] / 2 + hand_potentials[1][2]) / (sum(hand_potentials[0]) + sum(hand_potentials[1]) / 2)
        except:
            print(self.hand, self.board_cards)
            ppot = 0
            npot = 0
            
        print(start)
        return ppot, npot


if __name__ == "__main__":
    d = Deck()

    hand = [d.get('7h'), d.get('9h')]
    board = [d.get('8h'), d.get('6c'), d.get('4h')]

    e = eval(hand, board)

    # print(e.hand_strength())

    start_ii = time()

    # print(e.potential_hand_strength(1))
    # print(e.potential_hand_strength(2, only_ppot=True))
    print(e.potential_hand_strength(2))


    print(time() - start_ii)
