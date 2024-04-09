import sys
sys.path.append('../poker')
from bots import *

if __name__ == "__main__":
    deck = Deck()
    table = Table(deck)
    scary_cat = ScaryCat('ScaryCat', table)
    better = Better('Better', table)
    assert scary_cat.name == 'ScaryCat'

    # --- Test 1 ---
    table.pre_flop()        # Pre-flop
    for i in range(2):
        scary_cat.receive(table.deck.draw())
        table.deck.burn
        better.receive(table.deck.draw())
    better.play()                           # Better bot plays (bets 99)
    better.play()                           # Better bot plays (bets 99)
    assert better.balance == 1000-99*2
    assert table.pot == 99*2
    for i in range(9):
        better.play()
    assert better.balance == 0              # Check if all stats match
    assert table.game_stats['bet'] == 10
    assert table.game_stats['all-in'] == 1
    assert better.stats['all-in'] == 1
    assert better.stats['bet'] == 10
    table.reset()
    assert table.round_stats['bet'] == 0        # Round stats should be reset.
    assert table.round_stats['all-in'] == 0
    assert table.game_stats['bet'] == 10        # Game stats shouldn't be reset.
    assert table.game_stats['all-in'] == 1
    table.end()
    assert not table.players

    # --- Test 2 ---
    table.pre_flop()
    assert len(table.board) == 3
    table.flop()
    assert len(table.board) == 3
    table.turn()
    assert len(table.board) == 4
    table.river()
    assert len(table.board) == 5        # Check if table has 5 cards after river
    table.end()

    # --- Test 3 ---
    


    # --- End tests ---
    print('################')
    print('All tests passed')
