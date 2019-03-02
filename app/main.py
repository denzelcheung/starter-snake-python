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

    board[data['you']['body'][0]['y']][data['you']['body'][0]['x']] = 10        #Head
    board[data['you']['body'][-1]['y']][data['you']['body'][-1]['x']] = 30      #Body
    return board

def getSnakeInfo(data):
    snake = {}
    snake['health'] = data['you']['health']
    snake['length'] = len(data['you']['body'])
    snake['head'] = data['you']['body'][0]
    snake['tail'] = data['you']['body'][-1]
    return snake

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

    board = getBoardInfo(data)
    snake = getSnakeInfo(data)
    head_x = snake['head']['x']
    head_y = snake['head']['y']
    width = data['board']['width']
    height = data['board']['height']

    if (board[head_x+1][head_y] == 0 or 5) and ((head_x+1) < width-1):
        return move_response(directions[3])
    elif (board[head_x][head_y+1] == 0 or 5) and ((head_y+1) < height-1):
        return move_response(directions[2])
    elif (board[head_x-1][head_y] == 0 or 5) and ((head_x-1) > 0):
        return move_response(directions[1])
    elif (board[head_x][head_y-1] == 0 or 5) and ((head_y-1) > 0):
        return move_response(directions[0])



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
