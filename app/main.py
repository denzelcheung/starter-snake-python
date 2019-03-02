import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

variable = 0

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


def getBoardInfo(data):
    boardInfo = data
    board = [0] * boardInfo['board']['width']
    for i in range(boardInfo['board']['width']):
        board[i] = [0] * boardInfo['board']['height']

    for food in boardInfo['board']['food']:
        board[food['y']][food['x']] = 5

    for snake in boardInfo['board']['snakes']:
        for body in snake['body']:
            board[body['y']][body['x']] = 2
        board[snake['body'][0]['y']][snake['body'][0]['x']] = 1
        board[snake['body'][-1]['y']][snake['body'][-1]['x']] = 3

    for body in data['you']['body']:
        board[body['y']][body['x']] = 20

    board[data['you']['body'][0]['y']][data['you']['body'][0]['x']] = 10
    board[data['you']['body'][-1]['y']][data['you']['body'][-1]['x']] = 30
    return board

@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    directions = ['up', 'left', 'down', 'right']
        #direction = random.choice(directions)
    global variable
    if variable == 4:
        variable = 0
    print(variable)
    direction = directions[variable]
    variable = variable + 1
    #direction = directions[1]
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
