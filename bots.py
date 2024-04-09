from game import *

# Meme bots
class Better(Player):
    '''A bot that always bets 99$, or all of his balance if it is less than 99$.'''
    def play(self):
        if self.balance >= 99:      # Check if balance is less than 99.
            self.bet(99)            # Bet 99 if it is more or equal to 99.
        elif self.balance == 0:
            raise ValueError('you broke ahh')       # If bot doesn't have anymore money, they lose.
        else:
            self.bet(self.balance)  # Otherwise, bet the remaining balance of the bot, as an all-in.

class ScaryCat(Player):
    '''A bot that always if a single opponent bets. Otherwise, checks.'''
    def play(self):
        pass

class Joker(Player):
    '''A bot that only does random actions. Can bet a random multiplier of the small blind'''

# Real playstyles
class TightPassive(Player):
    '''A bot that plays very few hands and is usually always checking, calling, or folding most of the time.'''
    # Currently working on implementing always checking/calling unless required bet is more than half of its own balance.
    def play(self):
        pass


# ----------------------------------------    
# Tests

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
    better.play()           # Better bot plays (bets 99)
    better.play()           # Better bot plays (bets 99)
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
    print(table.players)

    # --- Test 2 ---



    # --- End tests ---
    print('################')
    print('All tests passed')
