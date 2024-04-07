import random

class Cards:
    def __init__(self, fullName, shortName,suit, value):
        self.fullName = fullName
        self.shortName = shortName
        self.suit = suit
        self.value = value

    def __repr__(self):
        return self.shortName

class Deck:
    class DeckStack(list):
        def prepend(self, card):
            '''Add card to front of list'''
            self.append(card)
        
        def delete(self):
            '''Remove top card of deck and return it'''
            return self.pop()
        
        def top(self):
            '''Check top card of deck'''
            return self[-1]

    def __init__(self):
        self.cards_list = {} # [As:{object}, Ks:{object},...] where A = ace and s = spades.
        self.deck = self.DeckStack() # [] stack where last element is the top of deck
        self.original = self.DeckStack() # Original deck (putting all cards back)

        cards = ['As','Ks','Qs','Js','Ts','9s','8s','7s','6s','5s','4s','3s','2s','Ac','Kc','Qc','Jc','Tc','9c','8c','7c','6c','5c','4c','3c','2c','Ah','Kh','Qh','Jh','Th','9h','8h','7h','6h','5h','4h','3h','2h', 'Ad','Kd','Qd','Jd','Td','9d','8d','7d','6d','5d','4d','3d','2d']
        cardNames = ['Ace', 'King',' Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two']
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        cardsIndex = 0
        value = 14
        for i in suits:
            for j in cardNames:
                self.cards_list[cards[cardsIndex]] = Cards(j+' of '+i, cards[cardsIndex], i, value)
                value -= 1
                cardsIndex += 1
            value = 14
        for val in self.cards_list.values():
            self.deck.prepend(val)
            self.original.prepend(val)

    def __repr__(self):
        return str(self.deck)
    
    def _(self, name):
        '''Returns the specific card object'''
        return self.cards_list.get(name)

    def shuffle(self):
        '''Shuffles the deck'''
        random.shuffle(self.deck)
    
    def draw(self):
        '''Returns top card of deck, and removes it from deck'''
        return self.deck.delete()
    
    def burn(self):
        '''Removes top card of deck, doesn't return anything.'''
        self.deck.delete()
    
    def reset(self):
        '''Resets the deck, all discarded and played cards are put back into the deck.'''
        self.deck = self.original.copy()
