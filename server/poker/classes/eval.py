from cards import Deck
from game import Player

class eval():
    def __init__(self, hand, board_cards):
        self.hand = hand
        self.board_cards = board_cards
    
    def remove_cards(self, deck, cards_to_remove):
        new_deck = []
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

d = Deck()

hand = [d.get('Ad'), d.get('Qc')]
board = [d.get('3h'), d.get('4c'), d.get('Jh')]

e = eval(hand, board)

print(e.hand_strength())