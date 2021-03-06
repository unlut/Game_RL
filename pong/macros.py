#  GRAPHIC CONSTANTS
display_width = 800
display_height = 600    
FPS_MENU = 15
FPS = 30


#  INPUT TYPE CONSTANTS - ELLEME
INPUT_TYPE_NULL = 0
INPUT_TYPE_PLAYER_1 = 1
INPUT_TYPE_PLAYER_2 = 2
#INPUT_TYPE_COMPUTER_1 = 11
#INPUT_TYPE_COMPUTER_2 = 12
INPUT_TYPE_COMPUTER_RANDOM = 101
INPUT_TYPE_COMPUTER_KURALBAZ = 102
AI_TYPE_STRINGS = ["RANDOM", "KURALBAZ"]

RESULT_GAME_CONTINUE = 1000
RESULT_PLAYER_1_WIN = 1001
RESULT_PLAYER_2_WIN = 1002
RESULT_PLAYER_1_HIT = 1003
RESULT_PLAYER_2_HIT = 1004


#  COLOR CONSTANTS
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0, 0, 200)
bright_red = (255,0,0)
bright_green = (0,255,0)




#  PLAYER PADDLE CONSTANTS
PLAYER_HORIZONTAL_OFFSET = 20
PLAYER_WIDTH = 5
PLAYER_HEIGHT = 40
PLAYER_SPEED = 6
#PLAYER_1_COLOR = red
#PLAYER_2_COLOR = blue


#  BALL CONSTANTS
BALL_INITIAL_RADIUS = 5
BALL_INITIAL_ACCELERATION = 0
BALL_TIMESTEP = 1


BALL_INITIAL_MIN_SPEED = 8
BALL_INITIAL_MAX_SPEED = 8
#BALL_COLOR = white





#  BALL EVENT CONSTANTS - ELLEME
BALL_EVENT_NOTHING = 0
BALL_EVENT_BOUNCE_TOP = 1
BALL_EVENT_BOUNCE_BOTTOM = 2
BALL_EVENT_P1_VERTICAL = 3
BALL_EVENT_P1_HORIZONTAL = 4
BALL_EVENT_P2_VERTICAL = 5
BALL_EVENT_P2_HORIZONTAL = 6







#  PHYSICS CONSTANTS
"""
MODEL 1:
    soyle
    boyle
    
    
MODEL 2: https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
    soyle
    boyle
"""
USED_PHYSICS_MODEL = 1

#  model 1 constants
COLLISION_VERTICAL_SPEED_CHANGE = False
COLLISION_VERTICAL_SPEED_MULTIPLIER = 2
COLLISION_VERTICAL_SLOW_MULTIPLIER = 2


#  model 2 constants
COLLISION_MAX_BOUNCE_ANGLE = 60.0  #  +- 15 due to ball radius


