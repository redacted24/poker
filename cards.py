class Cards:
    def __init__(self, fullName, suit, value):
        self.fullName = fullName
        self.suit = suit
        self.value = value

    def __repr__(self):
        return self.fullName + ' ' + str(self.value)


    
allCards = {}
cards = ['As','Ks','Qs','Js','Ts','9s','8s','7s','6s','5s','4s','3s','2s','Ac','Kc','Qc','Jc','Tc','9c','8c','7c','6c','5c','4c','3c','2c','Ah','Kh','Qh','Jh','Th','9h','8h','7h','6h','5h','4h','3h','2h', 'Ad','Kd','Qd','Jd','Td','9d','8d','7d','6d','5d','4d','3d','2d']
cardNames = ['Ace', 'King',' Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two']
suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

cardsIndex = 0
value = 14

for i in suits:
    for j in cardNames:
        allCards[cards[cardsIndex]] = Cards(j+' of '+i, i, value)
        value -= 1
        cardsIndex += 1
    value = 14
