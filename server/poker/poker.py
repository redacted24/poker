from flask import ( Blueprint, session, request )
import pickle, requests

from poker.classes.cards import *
from poker.classes.game import *
from poker.classes.bots import *

# define /api/poker to be the point of contact for backend logic
bp = Blueprint('poker', __name__, url_prefix='/api/poker')

def fetch_table(request):
  '''Get table table data with a given table ID'''

  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  return req, res, table

def send_table(table):
  '''Send table data in string form'''
  return requests.post('http://localhost:3003/api/session', json={ 'table': pickle.dumps(table).decode('latin1') })
  
def update_table(table, id):
  '''Update table data in string form'''
  return requests.put(f'http://localhost:3003/api/session/{id}', json={ 'table': pickle.dumps(table).decode('latin1') })

def load_table(res):
  '''Load table data from string form'''
  return pickle.loads(res.json()['table'].encode('latin1'))


@bp.post('/count')
def count():
  '''Test function for server/site communication and session variables'''

  session['count'] = session.get('count', 0) + 1          # increment session variable 'count' by 1
  return str(session['count'])

@bp.post('/init')
def init():
  req = request.get_json()
  player = Player(req['name'], False)
  
  deck = Deck()
  table = Table(deck)

  table.add_player(player)

  res = send_table(table)

  table = load_table(res)

  table.id = res.json()['id']

  update_table(table, table.id)

  return table.toJSON(req['name'])


@bp.post('/quick_start')
def quick_start():
  '''Quickly initializes the poker table logic and start the game.'''
  req = request.get_json()
  player = Player(req['name'], False)

  deck = Deck()
  table = Table(deck)

  table.add_player(player)
  table.add_player(AdvancedBot('moderate_bot', 'moderate'))
  table.add_player(AdvancedBot('tight_bot', 'moderate'))
  table.add_player(RingRingItsTheCaller('caller', True))

  res = send_table(table)

  table = load_table(res)

  table.id = res.json()['id']

  res = update_table(table, table.id)

  table = load_table(res)

  return table.toJSON(req['name'])

@bp.post('/join')
def join():
  '''Joins an existing game'''
  req, res, table = fetch_table(request)

  player = Player(req['name'], False)
  table.add_player(player)

  res = update_table(table, req['id'])

  table = load_table(res)

  return table.toJSON(req['name'])

@bp.post('/add_bot')
def add_bot():
  '''Adds a bot to an existing game'''
  req, res, table = fetch_table(request)

  bot = None

  match req['bot_type']:
    case 'better':
      bot = Better('better', True)
    case 'caller':
      bot = RingRingItsTheCaller('caller', True)
    case 'scary_cat':
      bot = ScaryCat('scary_cat', True)
    case 'copy_cat':
      bot = CopyCat('copy_cat', True)
    case 'tight_bot':
      bot = AdvancedBot('tight_bot', 'tight')
    case 'moderate_bot':
      bot = AdvancedBot('moderate_bot', 'moderate')
    case 'loose_bot':
      bot = AdvancedBot('loose_bot', 'loose')
    case 'random':
      from random import choice
      bot = choice(['better', 'caller', 'scary_cat', 'copy_cat', 'tight_bot', 'moderate_bot', 'loose_bot'])


  player_names = [p.name for p in table.players]

  if bot.name in player_names:
    original_name = bot.name
    i = 1
    while bot.name in player_names:
      bot.name = f'{original_name} ({i})'
      i += 1

  table.add_player(bot)

  res = update_table(table, req['id'])

  table = load_table(res)

  return table.toJSON(None)

@bp.post('/leave')
def leave():
  '''Leave an existing game'''
  req, res, table = fetch_table(request)

  table.remove_player(req['name'])

  res = update_table(table, req['id'])

  table = load_table(res)

  return table.toJSON(req['name'])

@bp.post('/start')
def start():
  '''Beings the pre-flop phase of the game. Deals 3 cards on the table and a hand to each player.'''
  req, res, table = fetch_table(request)

  if len(table.board) != 0: return table.toJSON(req['name'])

  table.state = 0
  table.pre_flop()

  update_table(table, req['id'])

  table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/get-table')
def get_table():
  '''Get the current state of the table'''
  req, res, table = fetch_table(request)

  return table.toJSON(req['name'])

@bp.post('/set-settings')
def set_settings():
  req, res, table = fetch_table(request)

  table.initial_balance = req['startingBalance']

  for player in table.players:
    player.balance = req['startingBalance']

  table.small_blind_amount = req['smallBlindAmount']
  table.big_blind_amount = req['smallBlindAmount'] * 2

  table.blind_interval = req['blindInterval']
  
  table.auto_rebuy = req['autoRebuy']
  print(f'Auto Rebuy: {table.auto_rebuy}')
  table.display_game_stats = req['gameStats']
  table.dynamic_table = req['dynamicTable']

  table.show_all_bot_cards = req['showAllBotCards']
  table.show_all_cards = req['showAllCards']

  res = update_table(table, req['id'])

  table = load_table(res)

  return table.toJSON(None)

@bp.post('/call')
def call():
  '''Player calls, matching the current bet.'''
  req, res, table = fetch_table(request)

  player = next(player for player in table.players if player.name == req['name'])

  player.call()

  table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/check')
def check():
  'Player checks, passing the turn without betting.'
  req, res, table = fetch_table(request)

  player = next(player for player in table.players if player.name == req['name'])

  player.check()

  table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/fold')
def fold():
  'Player folds, giving up their current hand.'
  req, res, table = fetch_table(request)

  player = next(player for player in table.players if player.name == req['name'])

  player.fold()

  if table.state != 4: table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/bet')
def bet():
  'Player bets, raising the required bet to stay in for the entire table.'
  req, res, table = fetch_table(request)

  player = next(player for player in table.players if player.name == req['name'])

  player.bet(req['amount'])

  table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/go_next')
def go_next():
  req, res, table = fetch_table(request)

  table.play()

  update_table(table, req['id'])

  return table.toJSON(req['name'])

@bp.post('/clear')
def clear():
  '''Clears all session variables for the session.'''
  session.pop('count', None)
  
  req = request.get_json()

  requests.delete(f'http://localhost:3003/api/session/{req["id"]}')

  return str(204)
