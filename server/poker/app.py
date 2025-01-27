from flask import Flask
from flask_socketio import SocketIO

# Initialize the socketio instance globally
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)  # Create and configure the server
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Secret key for session cookies

    # Initialize socketio with app
    socketio.init_app(app)

    return app
