from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, send, emit

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

    send(table.toJSON(None), to=table_id)
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

    send(table.toJSON(None), to=table_id)
    emit("player_joined", bot_name, to=table_id)



@socketio.event
def remove_player(data):
    '''Remove a player from an existing game'''
    table_id = data['table_id']
    table = games[table_id]

    table.remove_player(data['name'])

    send(table.toJSON(None), to=table_id)
    emit("player_left", data['name'], to=table_id)


@socketio.event
def disconnect(data):
    """event listener when client disconnects to the server"""
    table_id = data["table_id"]
    leave_room(data["table_id"])

    emit("player_left", data['name'], to=table_id)



if __name__ == '__main__':
    app = create_app()
    socketio.run(app)