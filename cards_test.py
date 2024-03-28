from cards import *
from game import *

deck = Deck()
table = Table(deck)

player = Player('bob')
player.receive(deck.draw())
player.receive(deck.draw())
print(player.hand())
player.bet(500)
print(table.pot)