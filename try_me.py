from cards import *
from game import *

deck = Deck()
table = Table(deck)


user = ''
name = input("Welcome to poker! What's your name?: ")
p1 = Player(name, table)
print('You start with 1000 chips.')
while user != 'wq':
    # Pre-flop
    table.pre_flop()
    print(f'The current board is: {table}')
    print(f'Your hand is: {p1.hand()}')
    user = input('Would you like to bet, call/check or raise? ')
    if user == 'bet':
        try:
            bet = int(input('Please enter the amount you would like to bet: '))
        except ValueError:
            print('Incorrect option, please retry')
            continue
        try:
            p1.bet(bet)
        except ValueError:
            continue
        
        print(f'{p1.name} has bet {bet}$, the pot is now {table.pot}$')
        print(f'{p1.name} has {p1.balance}$ in chips remaining')