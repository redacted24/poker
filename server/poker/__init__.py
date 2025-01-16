from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import requests

from random import randint, choice

from poker.classes.cards import *
from poker.classes.game import *
from poker.classes.bots import *

socketio = SocketIO(cors_allowed_origins="*")

games = {}

def create_app():
    app = Flask(__name__)                               # create and configure the server
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'            # sets secret key for signing session cookies (will change later)

    # import poker logic into the server
    from . import poker 
    app.register_blueprint(poker.bp)
    socketio.init_app(app)

    return app



@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print("client has connected")


def get_unique_name(name, player_names):
    if name in player_names:
        original_name = name
        i = 1
        while name in player_names:
            name = f'{original_name} ({i})'
            i += 1

    return name
    


@socketio.event
def host(data):
    '''Host a server for other players to join.'''
    table_id = hex(randint(0, 16777215))[2:].zfill(6).upper()
    join_room(table_id)

    player = Player(data['name'], False)

    table = Table(table_id)
    table.add_player(player)

    games[table_id] = table

    send(table.toJSON(data['name']))



@socketio.event
def join(data):
    '''Joins an existing game'''
    table_id = data['table_id']

    join_room(table_id)
    table = games[table_id]

    player_names = [p.name for p in table.players]
    name = get_unique_name(data["name"], player_names)

    player = Player(name, False)
    table.add_player(player)

    if (data["name"] != name): emit("change_username", name)

    send(table.toJSON(), to=table_id)
    emit("player_joined", name, to=table_id)


@socketio.event
def add_bot(data):
    '''Adds a bot to an existing game'''

    bots = {
        "better": Better,
        "caller": RingRingItsTheCaller,
        "scary_cat": ScaryCat,
        "copy_cat": CopyCat,
        "tight_bot": lambda name: AdvancedBot(name, "tight"),
        "moderate_bot": lambda name: AdvancedBot(name, "moderate"),
        "loose_bot": lambda name: AdvancedBot(name, "loose"),
    }

    table_id = data['table_id']
    table = games[table_id]

    player_names = [p.name for p in table.players]
    bot_name = get_unique_name(data["bot_type"], player_names)

    bot = bots.get(data["bot_type"], choice(list(bots.values())))(bot_name)

    table.add_player(bot)

    send(table.toJSON(), to=table_id)
    emit("player_joined", bot_name, to=table_id)


@socketio.event
def remove_player(data):
    '''Remove a player from an existing game'''
    table_id = data['table_id']
    table = games[table_id]

    table.remove_player(data['name'])

    send(table.toJSON(), to=table_id)
    emit("player_left", data['name'], to=table_id)


@socketio.event
def set_settings(data):
    table_id = data['table_id']
    table = games[table_id]

    table.initial_balance = data['startingBalance']

    for player in table.players:
        player.balance = data['startingBalance']

    table.small_blind_amount = data['smallBlindAmount']
    table.big_blind_amount = data['smallBlindAmount'] * 2

    table.blind_interval = data['blindInterval']
    
    table.auto_rebuy = data['autoRebuy']
    table.display_game_stats = data['gameStats']
    table.dynamic_table = data['dynamicTable']

    table.show_all_bot_cards = data['showAllBotCards']
    table.show_all_cards = data['showAllCards']

    send(table.toJSON(), to=table_id)
    emit("start_game", to=table_id)


@socketio.event
def disconnect(data):
    """event listener when client disconnects to the server"""
    table_id = data["table_id"]
    leave_room(data["table_id"])

    emit("player_left", data['name'], to=table_id)





@socketio.event
def get_table(data):
    """Grabs the table instance of a given table id"""
    table_id = data["table_id"]
    table = games[table_id]

    send(table.toJSON())


@socketio.event
def start(data):
    '''Beings the pre-flop phase of the game. Deals 3 cards on the table and a hand to each player.'''
    table_id = data["table_id"]
    table = games[table_id]

    table.state = 0
    table.pre_flop()

    while table.play():
        send(table.toJSON(data["name"]))

    send(table.toJSON(data["name"]))


@socketio.event
def call(data):
    '''Player calls, matching the current bet.'''
    table_id = data["table_id"]
    table = games[table_id]

    player = next(player for player in table.players if player.name == data['name'])

    player.call()

    send(table.toJSON(data["name"]))
    while table.play():
        send(table.toJSON(data["name"]))

    send(table.toJSON(data["name"]))


@socketio.event
def check(data):
    'Player checks, passing the turn without betting.'
    table_id = data["table_id"]
    table = games[table_id]

    player = next(player for player in table.players if player.name == data['name'])

    player.check()

    send(table.toJSON(data["name"]))
    while table.play():
        send(table.toJSON(data["name"]))

    send(table.toJSON(data["name"]))


@socketio.event
def fold(data):
    'Player folds, giving up their current hand.'
    table_id = data["table_id"]
    table = games[table_id]

    player = next(player for player in table.players if player.name == data['name'])

    player.fold()

    send(table.toJSON(data["name"]))
    while table.play():
        send(table.toJSON(data["name"]))

    send(table.toJSON(data["name"]))


@socketio.event
def bet(data):
    'Player bets, raising the datauired bet to stay in for the entire table.'
    table_id = data["table_id"]
    table = games[table_id]

    player = next(player for player in table.players if player.name == data['name'])

    player.bet(data['amount'])

    send(table.toJSON(data["name"]))
    while table.play():
        send(table.toJSON(data["name"]))

    send(table.toJSON(data['name']))


@socketio.on("next")
def go_next(data):
    table_id = data["table_id"]
    table = games[table_id]

    table.play()

    send(table.toJSON(data['name']))


if __name__ == '__main__':
    app = create_app()
    socketio.run(app)