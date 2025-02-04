from random import shuffle
import copy

class Cards:
    def __init__(self, fullName: str, shortName: str, suit: str, value: int, num: int):
        self.fullName = fullName            # Fullname of the card, e.g. Ace of Spades
        self.shortName = shortName          # Shortname of the card, e.g. As (for Ace of Spades)
        self.suit = suit                    
        self.value = value
        self.hex_value = hex(value)[2:].upper()
        self.num = num

    def __repr__(self):
        return self.shortName
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __lt__(self, other):
        return self.value < other.value
    
    def __gt__(self, other):
        return self.value > other.value
    
    @staticmethod
    def hash_list(cards: list, flush_possible: bool=True):
        if (flush_possible) :
            return ''.join(sorted([card.shortName for card in cards]))
        
        return ''.join(sorted(card.hex_value for card in cards))

class Deck:
    class DeckStack(list[Cards]):
        def prepend(self, card: Cards):
            '''Add card to front of list'''
            self.append(card)
        
        def delete(self):
            '''Remove top card of deck and return it'''
            return self.pop()
        
        def clear(self):
            '''Clears the deck'''
            self.clear()
        
        def top(self):
            '''Check top card of deck'''
            return self[-1]


    __CLASSIC_DECK = DeckStack()

    cards = ['As', 'Ks', 'Qs', 'Js', 'Ts', '9s', '8s', '7s', '6s', '5s', '4s', '3s', '2s',
                'Ac', 'Kc', 'Qc', 'Jc', 'Tc', '9c', '8c', '7c', '6c', '5c', '4c', '3c', '2c',
                'Ah', 'Kh', 'Qh', 'Jh', 'Th', '9h', '8h', '7h', '6h', '5h', '4h', '3h', '2h',
                'Ad', 'Kd', 'Qd', 'Jd', 'Td', '9d', '8d', '7d', '6d', '5d', '4d', '3d', '2d']
    ranks = ['Ace', 'King', 'Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two']
    suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

    for idx, card in enumerate(cards):
        rank_idx = idx % 13
        suit_idx = idx // 13
        __CLASSIC_DECK.prepend(Cards(f'{ranks[rank_idx]} of {suits[suit_idx]}',
                                   card,
                                   suits[suit_idx],
                                   14 - rank_idx,
                                   (13 - rank_idx) + suit_idx * 13))

    __CARD_LOOKUP = {}
    for card in __CLASSIC_DECK:
        __CARD_LOOKUP[card.shortName] = copy.copy(card)
    

    @classmethod
    def get(self, shortName: str):
        return self.__CARD_LOOKUP[shortName]


    def __init__(self, shuffle=True, deck=None, bad_cards=[]):
        bad_cards_nums = [card.num for card in bad_cards]

        self.deck = [card for card in deck or Deck.__CLASSIC_DECK if card.num not in bad_cards_nums]

        if shuffle: self.shuffle()

    def __repr__(self):
        return str(self.deck)

    def __len__(self):
        return len(self.deck)

    def shuffle(self):
        '''Shuffles the deck'''
        shuffle(self.deck)

    def draw(self):
        '''Returns top card of deck, and removes it from deck'''
        return self.deck.delete()
    
    def burn(self):
        '''Removes top card of deck, doesn't return anything.'''
        self.deck.delete()
    
    def remove_card(self, cards: list[Cards]):
        card_nums = [card.num for card in cards]
        self.deck = [card for card in self.deck if card.num not in card_nums]
    
    def reset(self):
        '''Resets the deck, all discarded and played cards are put back into the deck.'''
        self.deck = copy.deepcopy(Deck.__CLASSIC_DECK)


if __name__ == "__main__":
    deck = Deck()
    
    x = Cards('Nine of Spades', '9s', 'Spades', 9, 9)
    y = Cards('Ten of Spades', '10s', 'Spades', 10, 10)
    z = Cards('Ten of Hearts', '10h', 'Hearts', 10, 36)
    assert x < y
    assert not x > y
    assert y == z

    print('All tests passed.')