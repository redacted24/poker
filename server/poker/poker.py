from flask import ( Blueprint, session, request )
import pickle, requests

from poker.classes.cards import *
from poker.classes.game import *
from poker.classes.bots import *

# define /api/poker to be the point of contact for backend logic
bp = Blueprint('poker', __name__, url_prefix='/api/poker')


@bp.post('/count')
def count():
  '''Test function for server/site communication and session variables'''

  session['count'] = session.get('count', 0) + 1          # increment session variable 'count' by 1
  return str(session['count'])


@bp.post('/init')
def init():
  '''Initializes the poker table logic. Runs at the start of each session.'''
  req = request.get_json()
  player = Player(req['name'], False)

  deck = Deck()
  table = Table(deck)

  table.add_player(player)
  table.add_player(AdvancedBot('moderate_bot', 'moderate'))
  table.add_player(AdvancedBot('tight_bot', 'moderate'))
  table.add_player(RingRingItsTheCaller('caller', True))

  res = requests.post('http://localhost:3003/api/session', json={ 'table': pickle.dumps(table).decode('latin1') })

  table = pickle.loads(res.json()['table'].encode('latin1'))

  table.id = res.json()['id']

  requests.put(f'http://localhost:3003/api/session/{table.id}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/start')
def start():
  '''Beings the pre-flop phase of the game. Deals 3 cards on the table and a hand to each player.'''
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  table.pre_flop()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/get-table')
def get_table():
  '''Get the current state of the table'''
  req = request.get_json()
  print(req)
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  return table.toJSON()

@bp.post('/call')
def call():
  '''Player calls, matching the current bet.'''
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  player = next(player for player in table.players if player.name == req['name'])

  player.call()

  table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/check')
def check():
  'Player checks, passing the turn without betting.'
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  player = next(player for player in table.players if player.name == req['name'])

  player.check()

  table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/fold')
def fold():
  'Player folds, giving up their current hand.'
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  player = next(player for player in table.players if player.name == req['name'])

  player.fold()

  if table.state != 4: table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/bet')
def bet():
  'Player bets, raising the required bet to stay in for the entire table.'
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  player = next(player for player in table.players if player.name == req['name'])

  player.bet(req['amount'])

  table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/go_next')
def go_next():
  req = request.get_json()
  res = requests.get(f'http://localhost:3003/api/session/{req["id"]}')
  table: Table = pickle.loads(res.json()['table'].encode('latin1'))

  table.play()

  requests.put(f'http://localhost:3003/api/session/{req["id"]}', json={ 'table': pickle.dumps(table).decode('latin1') })

  return table.toJSON()

@bp.post('/clear')
def clear():
  '''Clears all session variables for the session.'''
  session.pop('count', None)
  
  req = request.get_json()

  requests.delete(f'http://localhost:3003/api/session/{req["tableId"]}')

  return str(204)
