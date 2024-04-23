# the following tests are only for statistical and entertainment purposes only
# they should not be used as unit tests for bots.py

import sys, os

from poker.classes.bots import *
from poker.classes.game import *

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__


# Playing all on the same table
earnings = {}

print()
print()

for i in range(0):
  [sys.stdout.write("\x1b[1A\x1b[2K") for _ in range(2)]
  print(f"Playing all bots: game # {i}")
  print({ b: e / i+1 for b, e in earnings.items() })
  sys.stdout.flush()

  blockPrint()

  d = Deck()
  t = Table(d)


  b1 = AdvancedBot('tight_bot', 'tight', t)
  b2 = AdvancedBot('moderate_bot', 'moderate', t)
  b3 = AdvancedBot('loose_bot', 'loose', t)
  b4 = ScaryCat('cat', True, t)

  t.randomize

  t.pre_flop()
  t.play()

  for b in [b1, b2, b3, b4]:
    earnings[b.name] = earnings.get(b.name, 0) + b.balance - 1000

  enablePrint()

print()
print()
print()

# Playing against cat
earnings = {}
for tightness in ['tight', 'moderate', 'loose']:
  for i in range(0):
    [sys.stdout.write("\x1b[1A\x1b[2K") for _ in range(2)]
    sys.stdout.write(f"\rPlaying {tightness}_bot v cat: game # {i}")
    print({b: e / 2999 for b, e in earnings.items()})
    sys.stdout.flush()

    blockPrint()

    d = Deck()
    t = Table(d)

    b1 = AdvancedBot(f'{tightness}_bot', tightness, t)
    b2 = ScaryCat('cat', True, t)

    t.randomize()

    t.pre_flop()
    t.play()

    for b in [b1, b2]:
      earnings[b.name] = earnings.get(b.name, 0) + b.balance - 1000

    enablePrint()

print()
print()
print()

# Playing against each other
earnings = [[0] * 3 for _ in range(3)]
for i in range(100000):
  for j, t1 in enumerate(['tight', 'moderate', 'loose']):
    for k, t2 in enumerate(['tight', 'moderate', 'loose']):
      [sys.stdout.write("\x1b[1A\x1b[2K") for _ in range(6)]
      
      print(f"Playing {t1}_bot v {t2}_bot: game # {i}")
      print(f'         |  Tight  |   Mid   |  Loose  ')
      print(f'--------------------------------------')
      tightness = ['  Tight  ', '   Mid   ', '  Loose  ']
      for l, r in enumerate(earnings):
        print(f'{tightness[l]}', end='')
        for m, e in enumerate(r):
          print(f'| {(e / (i+1)):6.5f} ', end='')
        print()

      sys.stdout.flush()

      blockPrint()

      d = Deck()
      t = Table(d)

      b1 = AdvancedBot(f'{t1}_bot', t1, t)
      b2 = AdvancedBot(f'{t2}_bot', t2, t)

      t.randomize()

      t.pre_flop()
      t.play()

      enablePrint()
      earnings[j][k] += b1.balance - 1000


print()
print(f'         |  Tight  |   Mid   |  Loose  ')
print(f'--------------------------------------')
tightness = ['  Tight  ', '   Mid   ', '  Loose  ']
for i, r in enumerate(earnings):
  print(f'{tightness[i]}', end='')
  for e in r:
    print(f'| {e / 999:.5f} ', end='')
  print()
