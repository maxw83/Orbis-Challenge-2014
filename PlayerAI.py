import random
import Enums
from tronclient.Client import *


def is_passable_ignore_tunnel(game_map, x, y):
    passable = False
    if game_map[x][y] == EMPTY or game_map[x][y] == POWERUP:
        passable = True
    return passable


def is_passable(game_map, x, y, my_direction):
    test1 = False
    test2 = False
    # checks if x,y is a valid square. if so, test1 passed.
    if game_map[x][y] == EMPTY or game_map[x][y] == POWERUP:
        test1 = True

        # checks if entering tunnel. if not, test2 passed.
        try:
            if ((my_direction == Direction.UP or my_direction == Direction.DOWN) and
                ((game_map[x - 1][y] == EMPTY or game_map[x - 1][y] == POWERUP) or
                 (game_map[x + 1][y] == EMPTY or game_map[x + 1][y] == POWERUP))):

                test2 = True
        except IndexError:
            test2 = True
        try:
            if ((my_direction == Direction.RIGHT or my_direction == Direction.LEFT) and
                ((game_map[x][y + 1] == EMPTY or game_map[x][y + 1] == POWERUP) or
                 (game_map[x][y - 1] == EMPTY or game_map[x][y - 1] == POWERUP))):

                test2 = True
        except IndexError:
            test2 = True
    passable = test1 and test2
    return passable


def wall_hug(game_map, player_lightcycle):
    global init_pos
    my_position = player_lightcycle['position']
    my_x = my_position[0]
    my_y = my_position[1]
    my_direction = player_lightcycle['direction']

    if init_pos[0] < 5:

        intended_dir = Direction.UP
        if is_passable(game_map, my_x, my_y - 1, intended_dir):
            return PlayerActions.MOVE_UP
        if True:
            intended_dir = Direction.RIGHT
        if is_passable(game_map, my_x + 1, my_y, intended_dir):
            return PlayerActions.MOVE_RIGHT
        if True:
            intended_dir = Direction.DOWN
        if is_passable(game_map, my_x, my_y + 1, intended_dir):
            return PlayerActions.MOVE_DOWN
        if True:
            intended_dir = Direction.LEFT
        if is_passable(game_map, my_x - 1, my_y, intended_dir):
            return PlayerActions.MOVE_LEFT

        # if no direction seems possible, allow tunneling to happen

        if is_passable_ignore_tunnel(game_map, my_x, my_y - 1):
            return PlayerActions.MOVE_UP
        if is_passable_ignore_tunnel(game_map, my_x + 1, my_y):
            return PlayerActions.MOVE_RIGHT
        if is_passable_ignore_tunnel(game_map, my_x, my_y + 1):
            return PlayerActions.MOVE_DOWN
        return PlayerActions.MOVE_LEFT

    else:
        intended_dir = Direction.UP
        if is_passable(game_map, my_x, my_y - 1, intended_dir):
            return PlayerActions.MOVE_UP
        if True:
            intended_dir = Direction.LEFT
        if is_passable(game_map, my_x - 1, my_y, intended_dir):
            return PlayerActions.MOVE_LEFT
        if True:
            intended_dir = Direction.DOWN
        if is_passable(game_map, my_x, my_y + 1, intended_dir):
            return PlayerActions.MOVE_DOWN
        if True:
            intended_dir = Direction.RIGHT
        if is_passable(game_map, my_x + 1, my_y, intended_dir):
            return PlayerActions.MOVE_RIGHT

        #if none of them work, ignore tunneling
        if is_passable_ignore_tunnel(game_map, my_x, my_y - 1):
            return PlayerActions.MOVE_UP
        if is_passable_ignore_tunnel(game_map, my_x - 1, my_y):
            return PlayerActions.MOVE_LEFT
        if is_passable_ignore_tunnel(game_map, my_x, my_y + 1):
            return PlayerActions.MOVE_DOWN
        return PlayerActions.MOVE_RIGHT


class PlayerAI():
    init_pos = (0, 0)

    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        global init_pos
        init_pos = player_lightcycle['position']
        return

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):
        return wall_hug(game_map, player_lightcycle)


'''

8888888 8888888888 8 888888888o.      ,o888888o.     b.             8 
      8 8888       8 8888    `88.  . 8888     `88.   888o.          8 
      8 8888       8 8888     `88 ,8 8888       `8b  Y88888o.       8 
      8 8888       8 8888     ,88 88 8888        `8b .`Y888888o.    8 
      8 8888       8 8888.   ,88' 88 8888         88 8o. `Y888888o. 8 
      8 8888       8 888888888P'  88 8888         88 8`Y8o. `Y88888o8 
      8 8888       8 8888`8b      88 8888        ,8P 8   `Y8o. `Y8888 
      8 8888       8 8888 `8b.    `8 8888       ,8P  8      `Y8o. `Y8 
      8 8888       8 8888   `8b.   ` 8888     ,88'   8         `Y8o.` 
      8 8888       8 8888     `88.    `8888888P'     8            `Yo
      
                                Quick Guide
                --------------------------------------------
                      Feel free to delete this comment.

        1. THIS IS THE ONLY .PY OR .BAT FILE YOU SHOULD EDIT THAT CAME FROM THE ZIPPED STARTER KIT

        2. Any external files should be accessible from this directory

        3. new_game is called once at the start of the game if you wish to initialize any values

        4. get_move is called for each turn the game goes on

        5. game_map is a 2-d array that contains values for every board position.
                example call: game_map[2][3] == POWERUP would evaluate to True if there was a powerup at (2, 3)

        6. player_lightcycle is your lightcycle and is what the turn you respond with will be applied to.
                It is a dictionary with corresponding keys: "position", "direction", "hasPowerup", "isInvincible", "powerupType"
                position is a 2-element int array representing the x, y value
                direction is the direction you are travelling in. can be compared with Direction.DIR where DIR is one of UP, RIGHT, DOWN, or LEFT
                hasPowerup is a boolean representing whether or not you have a powerup
                isInvincible is a boolean representing whether or not you are invincible
                powerupType is what, if any, powerup you have

        7. opponent_lightcycle is your opponent's lightcycle. Same keys and values as player_lightcycle

        8. You ultimately are required to return one of the following:
                                                PlayerAction.SAME_DIRECTION
                                                PlayerAction.MOVE_UP
                                                PlayerAction.MOVE_DOWN
                                                PlayerAction.MOVE_LEFT
                                                PlayerAction.MOVE_RIGHT
                                                PlayerAction.ACTIVATE_POWERUP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_UP
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_DOWN
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_LEFT
                                                PlayerAction.ACTIVATE_POWERUP_MOVE_RIGHT
                
        9. If you have any questions, contact challenge@orbis.com

        10. Good luck! Submissions are due Sunday, September 21 at noon. You can submit multiple times and your most recent submission will be the one graded.
 
'''
