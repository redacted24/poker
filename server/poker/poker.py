from flask import ( Blueprint, session, request )
import pickle

from poker.classes.cards import *
from poker.classes.game import *

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
  table.add_player

  session['table'] = pickle.dumps(table)

  return { 'balance': player.balance }

@bp.post('/start')
def start():
  '''Beings the pre-flop phase of the game. Deals 3 cards on the table and a hand to each player.'''
  table: Table = pickle.loads(session['table'])

  table.pre_flop()

  hand = table.players[0].hand()
  table.players[0].table.board

  session['table'] = pickle.dumps(table)

  return {
    'hand': [c.shortName for c in hand],
    'required_bet': table.required_bet,
    'board': table.board,
    'pot': table.pot
  }

@bp.post('/call')
def call():
  '''Player calls, matching the current bet.'''
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  table.call(player)

  table.play()

  board = table.board

  session['table'] = pickle.dumps(table)

  return {
    'required_bet': table.required_bet,
    'pot': table.pot,
    'balance': player.balance,
    'hand': [c.shortName for c in player.hand()],
    'board': [c.shortName for c in board]
  }

@bp.post('/check')
def check():
  'Player checks, passing the turn without betting.'
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  table.check(player)

  table.play()

  board = table.board

  session['table'] = pickle.dumps(table)

  return {
    'required_bet': table.required_bet,
    'pot': table.pot,
    'balance': player.balance,
    'hand': [c.shortName for c in player.hand()],
    'board': [c.shortName for c in board]
    }

@bp.post('/bet')
def bet():
  'Player bets, raising the required bet to stay in for the entire table.'
  table: Table = pickle.loads(session['table'])

  req = request.get_json()

  player = next(player for player in table.players if player.name == req['name'])

  table.bet(player, req['amount'])

  table.play()

  board = table.board

  session['table'] = pickle.dumps(table)

  return {
    'required_bet': table.required_bet,
    'pot': table.pot,
    'balance': player.balance,
    'hand': [c.shortName for c in player.hand()],
    'board': [c.shortName for c in board]
    }

@bp.post('/clear')
def clear():
  '''Clears all session variables for the session.'''
  session.pop('count', None)
  session.pop('table', None)
  session.pop('player', None)

  return str(204)