from cards import *
from game import *

deck = Deck()
table = Table(deck)

user = ''
name = input("Welcome to poker! What's your name?: ")
p1 = Player(name, table)
print('You start with 1000 chips.')

def deal_hands():
    '''Deal hands to a player or all players'''
    # WIP. Currently only deals hands to p1. (hardcoded)
    for i in range(2):
        p1.receive(table.deck.draw())
        table.deck.burn()

while user != 'wq' and table.state < 4:
    # Different actions for different table states.
    # Pre-flop: Hands are dealt, and cards on the table are not yet shown.
    # Flop: 3 first cards on the table are shown.
    # Turn (4th street): A card is burned (optional), and the 4th card is shown on the table.
    # River: A card is burned (optional), and the 5th card is shown on the table.
    
    # Pre-flop
    if table.state == 0:
        table.pre_flop()
        deal_hands()
        table.view_state()
        p1.look()

    # Flop
    elif table.state == 1:
        table.view_state()
        p1.look()

    # Turn (4th street)
    elif table.state == 2:
        table.burn()
        table.add_card()
        table.view_state()
        p1.look()

    # River
    elif table.state == 3:
        table.burn()
        table.add_card()
        table.view_state()
        p1.look()

    # Section for the actions the user can do every round.
    user = input('Would you like to bet, fold or call/check? ')
    if user == 'bet':
        bet = int(input('Please enter the amount you would like to bet: '))
        p1.bet(bet)
        print(f'{p1.name} has bet {bet}$, the pot is now {table.pot}$')
        print(f'{p1.name} has {p1.balance}$ in chips remaining')
        table.state += 1

    # Fold
    elif user == 'fold':
        p1.fold()
        break
    
    # Check
    elif user == 'check':
        p1.check()
        table.state += 1
    
    # Call (to be implemented when computer side is done)
    # elif user == 'call':
    
    else:
        print('Invalid action.')
        break
