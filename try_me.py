from cards import *
from game import *

deck = Deck()
table = Table(deck)

user = ''
name = input("Welcome to poker! What's your name?: ")
p1 = Player(name, table)
print('You start with 1000 chips.')

def deal_hands():
    '''Deal hands to player'''
    for i in range(2):
        p1.receive(table.deck.draw())
        table.deck.burn

while user != 'wq':
    if table.state == 0:
        # Pre-flop
        table.pre_flop()
        deal_hands()
        table.view_state()
        p1.look()
    elif table.state == 1:
        # Flop
        table.view_state()
        p1.look()
    elif table.state == 2:
        # Turn (4th street)
        table.add_card()
        table.view_state()
        p1.look()
    elif table.state == 3:
        # River
        table.add_card()
        table.view_state()
        p1.look()


    user = input('Would you like to bet, fold or call/check? ')
    if user == 'bet':
        try:
            bet = int(input('Please enter the amount you would like to bet: '))
        except ValueError:
            print('Incorrect option, please retry')
            continue
        try:
            p1.bet(bet)
        except ValueError:
            break # Temporary
        
        print(f'{p1.name} has bet {bet}$, the pot is now {table.pot}$')
        print(f'{p1.name} has {p1.balance}$ in chips remaining')

    elif user == 'fold':
        p1.fold()
        
    elif user == 'check':
        p1.check()
        
    table.state += 1