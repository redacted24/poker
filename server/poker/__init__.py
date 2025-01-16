from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_cors import CORS

from flask import ( Blueprint, session, request )
import pickle, requests
from random import randint

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


@socketio.event
def host(data):
    '''Host a server for other players to join.'''
    print("hosting server")
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
    print('joining', table_id)

    join_room(table_id)
    table = games[table_id]

    player = Player(data['name'], False)
    table.add_player(player)

    send(table.toJSON(data['name']), to=table_id)



@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")


if __name__ == '__main__':
    app = create_app()
    socketio.run(app)