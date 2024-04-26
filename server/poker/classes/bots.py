try:
    from poker.classes.game import *
    from poker.classes.eval import *
except:
    from game import *      # type: ignore
    from eval import *      # type: ignore
from random import random

class AdvancedBot(Player):
    # --- Pre-Flop Betting Strategy --- #
    # Income rates for pre-flop. Used to determine what strategy to play
    # From left to right, each column goes from 2 to A
    # From top to bottom, each row goes from 2 to A
    # Suited hand's IR is calculated for row>column, otherwise an unsuited hand's IR will be calculated as column<row
    income_rates = [
        [-121, -440, -409, -382, -411, -432, -394, -357, -301, -259, -194, -116, 16 ],
        [-271, -42,  -345, -312, -340, -358, -371, -328, -277, -231, -165, -87,  54 ],
        [-245, -183,  52,  -246, -269, -287, -300, -308, -252, -204, -135, -55,  84 ],
        [-219, -151, -91,   152, -200, -211, -227, -236, -227, -169, -104, -24,  118],
        [-247, -177, -113, -52,   256, -145, -152, -158, -152, -145, -74,   9,   99 ],
        [-261, -201, -129, -65,   3,    376, -76,  -79,  -68,  -66,  -44,  48,   148],
        [-226, -204, -140, -73,  -2,    66,   503,  0,    15,   24,   45,  84,   194],
        [-191, -166, -147, -79,  -5,    68,   138,  647,  104,  113,  136, 177,  241],
        [-141, -116, -91,  -69,  -4,    75,   150,  235,  806,  226,  255, 295,  354],
        [-89,  -67,  -41,  -12,   7,    82,   163,  248,  349,  965,  301, 348,  410],
        [-29,  -3,    22,   51,   80,   108,  185,  274,  379,  423,  1141,403,  473],
        [47,    76,   101,  128,  161,  199,  230,  318,  425,  473,  529, 1325, 541],
        [175,   211,  237,  266,  249,  295,  338,  381,  491,  539,  594, 655, 1554]
    ]

    # Expert-defined values to calculate strategy thresholds. There are technically different thresholds, but we'll use the ones for 3-4 players for the sake of simplicity.
    # Dictionnary values are as:
    # 'tightness': [(make1 values), (make2 values), (make3 values)] where values are a tuple (base, increment)
    # The values for 'call1' and 'make1' are the same, as well as the values for 'call2' and 'make2'
    preflop_strategy_values = {
        'tight': {'make1': (75, 50), 'make2': (225, 50), 'make4': (600,0)},
        'moderate': {'make1': (25, 25), 'make2': (200, 25), 'make4': (580,0)},
        'loose': {'make1': (25, 10), 'make2': (175, 10), 'make4': (480,0)}
    }
    # The values for the thresholds of effective hand strength used to determine post-flop strategies. All vary by 0.05, depending on the tightness.
    ehs = {
        'tight': {'make2': 0.90, 'make1': 0.55},
        'moderate': {'make2': 0.85, 'make1': 0.50},
        'loose': {'make2': 0.80, 'make1': 0.45}
    }
    # The values for which the bots would bluff.
    bluff_percentage = {
        'tight': 0.04,
        'moderate': 0.07,
        'loose': 0.10
    }

    def __init__(self, name, tightness, table=None):
        '''The general class for an advanced bot. Contains all the necessary information for advanced play. Children class will have specific methods that tweak information in this class in order to play.
        
        - Name (str)
        - Table (table object)

        There is no is_computer parameter since it is put as True by default in AdvancedBot class.'''
        Player.__init__(self, name, True, table)
        self.tightness = tightness
        self.chosen_pre_flop_strategy = AdvancedBot.preflop_strategy_values[tightness]        # Chosen strategy is moderate by default. The variable is a dictionnary. See preflop_strategy_values
        self.thresholds_position = 0       # The number of players to play before it goes back to the player who started the round (small blind in most rounds except pre-flop)
        self.strategy_thresholds = {
            'make1': 0,
            'make2': 0,
            'make4': 0
        }
        self.ehs_thresholds = {
            'make1': AdvancedBot.ehs[self.tightness]['make1'],
            'make2': AdvancedBot.ehs[self.tightness]['make2'],
        }
        self.bluff_threshold = AdvancedBot.bluff_percentage[self.tightness]
        self.semi_bluff_threshold = self.bluff_threshold
        self.IR = 0     # IR rate, used to calculate preflop strategy
        self.fake_ehs = 0.90        # EHS used when bluffing
        self.fake_IR = 700          # IR used when bluffing
        self.number_of_play_actions = 0    # Helps for the are_we_bluffing() func. Makes it only triggers when the play function for the bot runs the first time    
        self.bluffing = False
        self.semi_bluffing = False

    def play(self):
        '''Playing function for the bot.'''
        # from time import sleep
        # sleep(1)
        from time import sleep
        sleep(0.5)


        if self.table.state == 0:       # We are in pre-flop
            self.IR = self.get_income_rate()
            #
            #
            # ----- Comment this function out if you don't want bluffing
            if self.number_of_play_actions == 0:
                if self.are_we_bluffing():
                    print('(bluffing): ', end='')
                elif self.are_we_semi_bluffing():
                    print('(semi-bluffing): ', end='')
            # -----
            #
            #
            if self.table.required_bet == 10 and self.IR <= -100:       # Prevents bots from folding too early (before someone even puts a bet in preflop), unless their hand is horrendous.
                if self.position == 2:                                  # Big blind cannot call because they have already put the minimum amount in the pot. So we make big blind check here.
                    print('(minimum play):', end=' ')
                    self.check()
                    return 'check'
                print('(minimum play):', end=' ')
                self.call()
                return 'call'
            elif self.IR >= self.strategy_thresholds['make4']:
                self.make4()
                return 'make4'
            elif self.IR >= self.strategy_thresholds['make2']:
                self.make2()
                return 'make2'
            elif self.IR >= 200 and self.position == 1:     # Hard-coded value for small-blind. Only works if player is small blind
                self.call2()
                return 'call2'
            elif self.IR >= self.strategy_thresholds['make1']:
                self.make1()
                return 'make1'
            elif self.IR >= -75 and self.position == 1:      # Hard-coded value for small-blind. Only works if player is small blind.
                self.call1()
                return 'call1'
            else:
                self.make0()        # Default strategy
                return 'make0'
            
        elif 1 <= self.table.state <= 3:         # We are in flop and River
            if self.bluffing:
                pass
            elif self.semi_bluffing:
                pass
            elif self.tightness == 'tight':
                self.compute_ehs_sad()           # For tight bot, use pessimistic version of EHS computation func.
            else:
                self.compute_ehs_happy()         # For moderate and loose bot, use optimistic version of EHS computation func.

            if self.ehs >= self.ehs_thresholds['make2']:
                self.make2()
                return 'make2'
            elif self.ehs >= self.ehs_thresholds['make1']:
                self.make1()
                return 'make1'
            elif self.table.required_bet == 0:      # Means that bot should check before proceeding to the last option
                self.check()
                return 'check'
            elif self.ehs <= self.ehs_thresholds['make1']:
                self.make0()        # Temporary, before adding semi-bluffing, pot odds and showdown odds
                return 'make0'
        
    def are_we_bluffing(self):
        '''Checks, according to randomness, if the bot should be bluffing.'''
        rand = random()
        if rand < self.bluff_threshold:
            self.bluffing = True
            self.IR = self.fake_IR
            self.ehs = round(self.fake_ehs + random()/10, 4)
            return True
        else:
            self.bluff_threshold += AdvancedBot.bluff_percentage[self.tightness]/10      # Increment the bluff percentage threshold so that the bot has more chances of doing a bluff later on. Increment depends on bot playstyle; if loose, increments fast, if tight, increments slowly
            return False
    
    def are_we_semi_bluffing(self):
        '''Check, according to randomness, if the bot should be semi-bluffing. Returns a boolean'''
        rand = random()
        if rand < self.semi_bluff_threshold:
            self.semi_bluffing = True
            self.ehs = self.compute_ppot()
            return True
        else:
            self.semi_bluff_threshold += AdvancedBot.bluff_percentage[self.tightness]/10      # Increment the bluff percentage threshold so that the bot has more chances of doing a bluff later on. Increment depends on bot playstyle; if loose, increments fast, if tight, increments slowly
            return False

    def update_player_position(self):
        '''Compute the threshold position number of the player and updates it. Does not return anything.'''
        # Calculated by number of active players - (the index of the player in queue + 1).
        # e.g. [p1, p2, p3, p4] on Pre-Flop where p4 starts playing. Threshold pos of p4 = 3 because there are 3 turns to play before it is their turn again
        if self.table.active_players() and self.table.player_queue:
            self.thresholds_position = int(len(self.table.active_players())-(self.table.player_queue.index(self)+1))        # The threshold position of the first player in queue should be length of players - 1.
        else:
            raise ValueError('Cannot update player position if game has not been started/set.')
        
    def update_strategy_thresholds(self):
        '''Update threshold values for all strategies (make1, make2, make4)'''
        self.strategy_thresholds['make1'] = self.chosen_pre_flop_strategy['make1'][0] + self.chosen_pre_flop_strategy['make1'][1]*self.thresholds_position
        self.strategy_thresholds['make2'] = self.chosen_pre_flop_strategy['make2'][0] + self.chosen_pre_flop_strategy['make2'][1]*self.thresholds_position
        self.strategy_thresholds['make4'] = self.chosen_pre_flop_strategy['make4'][0] + self.chosen_pre_flop_strategy['make4'][1]*self.thresholds_position
    
    def compute_ppot(self):
        '''Compute the PPOT of the hand. Used for semi-bluffing''' 
        a = eval(self.hand(), self.table.board.cards())
        return a.potential_hand_strength(2, True)[0]

    def compute_ehs_happy(self):
        '''Compute ehs using the happier version of the effective hand strength, i.e. the optimistic one that only accounts for PPOT (potential of winning) and ignoring NPOT (potential of losing). Modifies the ehs value of the class instance. Mostly used for aggressive playstyles'''
        a = eval(self.hand(), self.table.board.cards())
        # You're about to witness the worst piece of code ever coded
        if self.table.state == 1:       # Flop
            look_ahead = 2
        elif self.table.state == 2:     # Turn
            look_ahead = 1
        else:
            return
        hsn = a.hand_strength()
        self.ehs = round(hsn+(1-hsn)*a.potential_hand_strength(look_ahead, only_ppot=True)[0], 4)

    def compute_ehs_sad(self):
        '''Compute ehs using the sadder version of the effective hand strength, i.e. the pessimistic one that accounts for PPOT (potential of winning) and NPOT (potential of losing). Modifies the ehs value of the class instance. Mostly used for passive playstyles'''
        a = eval(self.hand(), self.table.board.cards())
        # You're about to witness the worst piece of code ever coded
        if self.table.state == 1:       # Flop
            look_ahead = 2
        elif self.table.state == 2:     # Turn
            look_ahead = 1
        else:
            return
        hsn = a.hand_strength()
        pots = a.potential_hand_strength(look_ahead)
        self.ehs = round(hsn+(1-hsn)*pots[0]-hsn*pots[1], 4)


    def get_income_rate(self):
        '''Return the IR rate of the bot's hand.'''
        temp = sorted(self.hand(), key=lambda x:x.value)
        if self.hand()[0].suit == self.hand()[1].suit:
            return AdvancedBot.income_rates[temp[1].value-2][temp[0].value-2]
        else:
            return AdvancedBot.income_rates[temp[0].value-2][temp[1].value-2]
    
    def find_bet_amount(self):
        '''Compute an amount to bet based on different factors. Returns the bet amount'''

        def _find_bet_amount():
            '''Helper function'''
            if amount-self.table.required_bet < self.table.required_raise:      # If the amount bet - table bet is smaller than the minimum raise, then we have to bet at least the table bet + the minimum raise 
                return self.table.required_bet + self.table.required_raise
            else:
                return amount
            
        if self.table.state == 0:                                                   # Preflop
            if self.tightness == 'loose':                                           # Unique interaction reserved for loose bots!
                lowest = min(self.table.active_players(), key=lambda p:p.balance)
                if lowest.balance * 2 < self.balance and self.IR >= 500:            # If the lowest balance player on the table has less than half of the current bot's balance, and the bot has a pretty good hand, it will try to force a fold or knockout the player by forcing them to all-in.
                    return lowest.balance
            amount = int((((self.IR + 432)/1986)/10)*self.balance) + self.current_bet
            return _find_bet_amount()

        else:                                                                       # Postflop
            if self.tightness == 'loose':                                           # Unique interaction reserved for loose bots!
                lowest = min(self.table.active_players(), key=lambda p:p.balance)
                if lowest.balance * 2 < self.balance and self.ehs >= 0.93:          # Same thing here, but with EHS instead of IR because it is after preflop
                    return lowest.balance
            amount = int(((self.ehs*0.1)*self.balance)) + self.current_bet
            return _find_bet_amount()

    # Strategies
    def make0(self):
        '''Fold if it costs more than zero to play. i.e.: folds every round'''
        print("(make0):", end=' ')
        self.fold()
        
    def call1(self):
        '''Fold if it costs more than 1 bet to continue playing and the bot hasn't put money into the pot this round yet, otherwise check/call. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        # Not really used except for small blind, who has different thresholds for it
        if self.table.round_stats['bet'] > 1:
            print("(call1):", end=' ')
            self.fold()
            return 'fold'
        else:
            if self.current_bet == self.table.required_bet:     # Player is big blind. So, player would check.
                print("(call1):", end=' ')
                self.check()
                return 'check'
            else:
                print("(call1):", end=' ')
                self.call()     # Player is not big blind, so player has to put in the minimum
                return 'call'
        
    def make1(self):
        '''If no bets have been made this round, then bet. Fold if two or more bets are required to continue. Otherwise check/call. THIS STRATEGY SHOULD NOT BE CALLED IF BOT IS THE BIG BLIND (it shouldn't happen). Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        if self.table.round_stats['bet'] > 1:
            print("(make1):", end=' ')
            self.fold()
            return 'fold'
        elif self.table.round_stats['bet'] == 0:
            print("(make1):", end=' ')
            self.bet(self.find_bet_amount())
            return 'bet'
        else:       # Else is when bet stat is == 1
            if self.current_bet == self.table.required_bet:     # Player is big blind.
                print("(make1):", end=' ')
                self.check()
                return 'check'
            else:       # Player is not big blind.
                print("(make1):", end=' ')
                self.call()
                return 'call'

    def call2(self):
        '''Always check/call, whatever bet is on the table. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        # Not really used except for small blind
        if self.current_bet == self.table.required_bet:
            print("(call2):", end=' ')
            self.check()
            return 'check'
        else:
            print("(call2):", end=' ')
            self.call()
            return 'call'
  
    def make2(self):
        '''Bet/raise if less than two bets/raises have been made this round, otherwise call. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        if self.table.round_stats['bet'] < 2:
            print("(make2):", end=' ')
            self.bet(self.find_bet_amount())
            return 'bet'
        else:
            print("(make2):", end=' ')
            self.call()
            return 'call'

    def make4(self):
        '''Bet/raise until betting is capped, or player goes all-in. Returns the computed action that will be played in the game, as a string. e.g."bet"'''
        print("(make4):", end=' ')
        self.bet(self.find_bet_amount())
        return 'bet'

    def reset(self):
        '''Resets the bot. Overrides parent class reset method.'''
        self.current_bet = 0
        self.active = True
        self.clear_hand()
        self.position = None
        self.previous_step = []
        self.bluffing = False
        self.semi_bluffing = False
        self.bluff_threshold = AdvancedBot.bluff_percentage[self.tightness]
        self.semi_bluff_threshold = self.bluff_threshold
        self.number_of_play_actions = 0
        self.ehs = 0

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
    '''A bot that always folds if a single opponent bets. Otherwise, checks.'''
    def play(self):
        # Preflop
        if self.table.required_bet == 10 and self.current_bet == 10:
            self.check()
            return 'check'
        # Postflop
        else:
            self.fold()
            return 'fold'

    def update_player_position(self):
        pass
    
    def update_strategy_thresholds(self):
        pass

class RingRingItsTheCaller(Player):
    '''A bot that always calls whatever bet is on the table.'''
    def play(self):
        # Preflop
        if self.table.required_bet == self.current_bet:
            self.check()
            return 'check'
        # Postflop
        else:
            self.call()
            return 'call'

    def update_player_position(self):
        pass
    
    def update_strategy_thresholds(self):
        pass

class CopyCat(Player):
    '''A bot that copies whatever the last move was. If they are the first to play, they would check/call depending if they are BB or not.'''
    def play(self):
        '''Play function for the bot.'''
        if self.table.last_move:
            if self.table.last_move[1] == 'call':
                self.call()
            elif self.table.last_move[1] == 'fold':
                self.fold()
            elif self.table.last_move[1] == 'bet':
                self.bet(30)
            elif self.table.last_move[1] == 'check':
                self.check()
        else:
            if self.position == 2:              # If player is big blind, they must check
                self.check()
                return 'check'
            self.call()
            return 'call'

    def update_player_position(self):
        '''Not needed'''
        pass
    
    def update_strategy_thresholds(self):
        '''Not needed'''
        pass
