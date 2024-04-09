from flask import ( Blueprint, session )

bp = Blueprint('poker', __name__, url_prefix='/api/poker')

@bp.route('/hi')
def hi():
  session['test'] = session.get('test', 0) + 1
  return str(session['test'])