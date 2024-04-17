try:
    from itertools import combinations
    from poker.classes.cards import Deck
    from poker.classes.game import Player
except:
    from cards import Deck      # type: ignore
    from game import Player     # type: ignore

class eval():
    def __init__(self, hand, board_cards):
        self.hand = hand
        self.board_cards = board_cards
    
    def remove_cards(self, deck, cards_to_remove):
        new_deck = []
        if type(deck) == list:
            for card in deck:
                to_add = True
                for bad_card in cards_to_remove:
                    if card.shortName == bad_card.shortName:
                        to_add = False
                        break
                if to_add:
                    new_deck.append(card)
        else:
            for card in deck.deck:
                to_add = True
                for bad_card in cards_to_remove:
                    if card.shortName == bad_card.shortName:
                        to_add = False
                        break
                if to_add:
                    new_deck.append(card)

        return new_deck

    def hand_strength(self):
        p1 = Player('player', True)
        p1.receive(self.hand)
        p1_rank = p1.handEval(self.board_cards)

        d = Deck()
        filtered_deck = self.remove_cards(d, self.hand + self.board_cards)
        print(filtered_deck)
        
        win = tie = loss = 0
        for i, c1 in enumerate(filtered_deck):
            for c2 in filtered_deck[i+1:]:
                p2 = Player('opponent', True)
                p2.receive([c1, c2])
                p2_rank = p2.handEval(self.board_cards)

                if p1_rank > p2_rank:
                    win += 1
                elif p1_rank == p2_rank:
                    tie += 1
                else:
                    loss += 1
        
        print(win, tie, loss)
        return (win + 0.5 * tie) / sum([win, tie, loss])

    def potential_hand_strength(self, look_ahead):
        hand_potentials = [[0] * 3 for _ in range(3)]
        
        p1 = Player('player', True)
        p2 = Player('opponent', True)

        p1.receive(self.hand)

        p1_rank_5 = p1.handEval(self.board_cards)

        d = Deck()
        computed_p1_ranks = {}
        computed_p2_ranks = {}

        filtered_deck = self.remove_cards(d, self.hand + self.board_cards)

        for c1, c2 in list(combinations(filtered_deck, 2)):
            p2.clear_hand()
            p2.receive([c1, c2])

            p2_rank_5 = p2.handEval(self.board_cards)

            if p1_rank_5 > p2_rank_5:
                i = 0           # We are ahaed
            elif p1_rank_5 == p2_rank_5:
                i = 1           # We are tied
            else:
                i = 2           # We are behind

            new_filtered_deck = self.remove_cards(filtered_deck, [c1, c2])

            for new_board_cards in list(combinations(new_filtered_deck, look_ahead)):
                predicted_board_cards = self.board_cards + list(new_board_cards)
                str_cards_p1 = ''.join(sorted([c.shortName for c in new_board_cards]))
                str_cards_p2 = ''.join(sorted([c.shortName for c in (c1, c2) + new_board_cards]))

                if str_cards_p1 in computed_p1_ranks:
                    p1_rank_7 = computed_p1_ranks[str_cards_p1]
                else:
                    p1_rank_7 = p1.handEval(predicted_board_cards)
                    computed_p1_ranks[str_cards_p1] = p1_rank_7

                if str_cards_p2 in computed_p2_ranks:
                    p2_rank_7 = computed_p2_ranks[str_cards_p2]
                else:
                    p2_rank_7 = p2.handEval(predicted_board_cards)
                    computed_p2_ranks[str_cards_p2] = p2_rank_7
            
                if p1_rank_7 > p2_rank_7:
                    hand_potentials[i][0] += 1
                elif p1_rank_7 == p2_rank_7:
                    hand_potentials[i][1] += 1
                else:
                    hand_potentials[i][2] += 1

        ppot = (hand_potentials[2][0] + hand_potentials[2][1] / 2 + hand_potentials[1][0]) / (sum(hand_potentials[2]) + sum(hand_potentials[1]) / 2)
        npot = (hand_potentials[0][2] + hand_potentials[0][1] / 2 + hand_potentials[1][2]) / (sum(hand_potentials[0]) + sum(hand_potentials[1]) / 2)

        return ppot, npot

    

d = Deck()

hand = [d.get('Ad'), d.get('Qc')]
board = [d.get('3h'), d.get('4c'), d.get('Jh')]

e = eval(hand, board)

print(e.potential_hand_strength(1))
print(e.potential_hand_strength(2))