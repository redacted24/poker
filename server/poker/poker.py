from flask import ( Blueprint, session )

# define /api/poker to be the point of contact for backend logic
bp = Blueprint('poker', __name__, url_prefix='/api/poker')


@bp.route('/count')
def count():
  '''Test function for server/site communication and session variables'''

  session['count'] = session.get('count', 0) + 1          # increment session variable 'count' by 1
  return str(session['count'])