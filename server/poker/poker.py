from flask import ( Blueprint, session, request )
import pickle

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
  table.add_player(AdvancedBot('loose_bot', 'moderate'))

  session['table'] = pickle.dumps(table)  

  return table.toJSON()

@bp.post('/start')
def start():
  '''Beings the pre-flop phase of the game. Deals 3 cards on the table and a hand to each player.'''
  req = request.get_json()
  if 'table' in session:
    table: Table = pickle.loads(session['table'])
  else:
    player = Player(req['name'], False)

    deck = Deck()
    table = Table(deck)

    table.add_player(player)
    table.add_player(AdvancedBot('moderate_bot', 'moderate'))
    table.add_player(AdvancedBot('tight_bot', 'moderate'))
    table.add_player(AdvancedBot('loose_bot', 'moderate'))

  table.pre_flop()
  table.play()

  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/call')
def call():
  '''Player calls, matching the current bet.'''
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  player.call()

  table.play()

  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/check')
def check():
  'Player checks, passing the turn without betting.'
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  player.check()

  table.play()

  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/fold')
def fold():
  'Player folds, giving up their current hand.'
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  player.fold()

  if table.state != 4: table.play()

  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/bet')
def bet():
  'Player bets, raising the required bet to stay in for the entire table.'
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  player.bet(req['amount'])

  table.play()

  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/go_next')
def go_next():
  table: Table = pickle.loads(session['table'])
  table.play()
  session['table'] = pickle.dumps(table)

  return table.toJSON()

@bp.post('/clear')
def clear():
  '''Clears all session variables for the session.'''
  session.pop('count', None)
  session.pop('table', None)
  session.pop('player', None)

  return str(204)