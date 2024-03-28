from cards import *
from game import *

deck = Deck()
table = Table(deck)

print(deck)
deck.shuffle()
print(deck)