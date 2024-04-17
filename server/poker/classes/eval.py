try:
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

    def potential_hand_strength(self):
        p1 = Player('player', True)
        p2 = Player('opponent', True)

        p1.receive(self.hand)

        d = Deck()
        computed_ranks = {}

        filtered_deck = self.remove_cards(d, self.hand + self.board_cards)
        
        win = tie = loss = 0
        for i, c1 in enumerate(filtered_deck):
            for c2 in filtered_deck[i+1:]:
                predicted_board_cards = self.board_cards + [c1, c2]
                p1_rank = p1.handEval(predicted_board_cards)

                new_deck = self.remove_cards(filtered_deck, [c1, c2])

                for k, c3 in enumerate(new_deck):
                    for c4 in new_deck[k+1:]:
                        p2.clear_hand()
                        p2.receive([c3, c4])
                        str_cards = ''.join(sorted([c.shortName for c in [c1, c2, c3, c4]]))
                        if str_cards in computed_ranks:
                            p2_rank = computed_ranks[str_cards]
                        else:
                            p2_rank = p2.handEval(predicted_board_cards)
                            computed_ranks[str_cards] = p2_rank

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

print(e.potential_hand_strength())