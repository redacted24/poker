from flask import Flask

def create_app():
    app = Flask(__name__)                               # create and configure the server
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'            # sets secret key for signing session cookies (will change later)

    # import poker logic into the server
    from . import poker
    app.register_blueprint(poker.bp)

    return app