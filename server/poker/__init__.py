from .app import create_app, socketio
from .lobby import *

app = create_app()

if __name__ == '__main__':
    socketio.run(app)