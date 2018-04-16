import pygame
from pygame.locals import *
import time
import random
import math    #  trigonometry functions


#  to export game screen buffer
from PIL import Image
import numpy as np



pygame.init()


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


BALL_INITIAL_MIN_SPEED = 3
BALL_INITIAL_MAX_SPEED = 4
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
USED_PHYSICS_MODEL = 2

#  model 1 constants
COLLISION_VERTICAL_SPEED_CHANGE = True
COLLISION_VERTICAL_SPEED_MULTIPLIER = 2
COLLISION_VERTICAL_SLOW_MULTIPLIER = 2


#  model 2 constants
COLLISION_MAX_BOUNCE_ANGLE = 60.0  #  +- 15 due to ball radius





#  oyuncularin topa vurdugu seyler icin obje
class PlayerObject:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = y
        #  helper variables for collision
        self.left = x
        self.right = x + PLAYER_WIDTH
        self.top = y
        self.bottom = y + PLAYER_HEIGHT
        self.color = color
        
        self.goingUp = False
        self.goingDown = False
        
        
    """
    def move_player(self, newx, newy, newdx, newdy):
        self.x = newx
        self.y = newy
        self.dx = newdx
        self.dy = newdy
        self.left = newx
        self.right = newx + PLAYER_WIDTH
        self.top = newy
        self.bottom = newy + PLAYER_HEIGHT
        
    def move_player(self, newx, newy):
        self.x = newx
        self.y = newy
        self.left = self.x
        self.right = self.x + PLAYER_WIDTH
        self.top = self.y
        self.bottom = self.y + PLAYER_HEIGHT
    """
    
    def move_player_vertical(self, speedY):
        self.y = self.y + speedY
        self.top = self.y
        self.bottom = self.y + PLAYER_HEIGHT
        
        if (speedY > 0):
            self.goingDown = True
            self.goingUp = False
        elif (speedY < 0):
            self.goingDown = False
            self.goingUp = True
        else:
            self.goingUp = False
            self.goingDown = False
        
    
    def Draw(self):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))


#  bi class
class PlayerInput:
    def __init__(self, up, down, bitir):
        self.up = up
        self.down = down
        self.bitir = bitir



p1_obj = PlayerObject(0+PLAYER_HORIZONTAL_OFFSET, display_height/2, 0, 0, red)
p2_obj = PlayerObject(display_width - PLAYER_HORIZONTAL_OFFSET, display_height/2, 0, 0, blue)
p1_input = PlayerInput(0, 0, 0)
p2_input = PlayerInput(0, 0, 0)



#  line intersection detection
#  line1: (x1, y1) to (x2, y2)
#  line2: (x3, y3) to (x4, y4)
def Intercept(x1, y1, x2, y2, x3, y3, x4, y4, d):
    denom = ((y4-y3) * (x2-x1)) - ((x4-x3) * (y2-y1))
    if (denom != 0):
        ua = (((x4-x3) * (y1-y3)) - ((y4-y3) * (x1-x3))) / denom
        if ((ua >= 0) and (ua <= 1)):
            ub = (((x2-x1) * (y1-y3)) - ((y2-y1) * (x1-x3))) / denom
            if ((ub >= 0) and (ub <= 1)):
                x = x1 + (ua * (x2-x1))
                y = y1 + (ua * (y2-y1))
                print("interception detected")
                return (x, y, d)
    return None


def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    else:
        return 0
    


class Ball:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.x = display_width/2
        self.y = display_height/2
        self.accel = BALL_INITIAL_ACCELERATION
        self.radius = BALL_INITIAL_RADIUS
        self.color = white

    def GiveRandomDirection(self):
        vx = random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
        vy = random.randint(BALL_INITIAL_MIN_SPEED, BALL_INITIAL_MAX_SPEED)
        toss = random.randint(0, 1)
        
        if (toss == 0):
            #  to left
            vx = -vx
        else:
            # to right
            vx = vx
        self.dx = vx
        self.dy = vy
    
    
    #  check if ball hits paddle
    def BallInterceptPaddle(self, targetPlayer, nx, ny):
        pt = None
        
        if (nx < 0):
            pt = Intercept(self.x, self.y, self.x + nx, self.y + ny, 
                           targetPlayer.right + self.radius,
                           targetPlayer.top - self.radius,
                           targetPlayer.right + self.radius,
                           targetPlayer.bottom + self.radius, "R")
        elif (nx > 0):
            pt = Intercept(self.x, self.y, self.x + nx, self.y + ny,
                           targetPlayer.left - self.radius,
                           targetPlayer.top - self.radius,
                           targetPlayer.left - self.radius,
                           targetPlayer.bottom + self.radius, "L")
        
        if (pt == None):
            if (ny < 0):
                pt = Intercept(self.x, self.y, self.x + nx, self.y + ny, 
                               targetPlayer.left - self.radius,
                               targetPlayer.bottom + self.radius,
                               targetPlayer.right + self.radius,
                               targetPlayer.bottom + self.radius, "B")
            elif (ny > 0):
                pt = Intercept(self.x, self.y, self.x + nx, self.y + ny, 
                               targetPlayer.left - self.radius,
                               targetPlayer.top - self.radius,
                               targetPlayer.right + self.radius,
                               targetPlayer.top - self.radius, "T")
    
        return pt
    
    def Roll(self):
        ball_event = BALL_EVENT_NOTHING
        
        #dt = clock.tick() / 1000
        #print(dt)
        #dt = 1
        dt = BALL_TIMESTEP
        
        
        #  calculate next position of ball
        #  deltaX = V*t + 0.5 * a * t^2
        newx = self.x + (dt * self.dx) + (self.accel * dt * dt * 0.5)
        newy = self.y + (dt * self.dy) + (self.accel * dt * dt * 0.5)
        
        #  calculate next speed of the ball
        #speed only changes with acceleration
        newdx = self.dx + (self.accel * dt) * (1 if self.dx > 0 else -1)
        newdy = self.dy + (self.accel * dt) * (1 if self.dy > 0 else -1)
        
        #  buna comment yazarsam uzun olur simdi ben biliyom
        nx = newx - self.x
        ny = newy - self.y
        
        
        
        #  check if ball will bounce from screen boundaries
        #  bottom
        if ((newdy > 0) and (newy > display_height)):
            newy = display_height
            newdy = -newdy
            ball_event = BALL_EVENT_BOUNCE_BOTTOM
        # up
        elif ((newdy < 0) and (newy < 0)):
            newy = 0
            newdy = -newdy
            ball_event = BALL_EVENT_BOUNCE_TOP
        
        
        #  decide which player ball can collide with
        #ball hits p1 when going left and p2 when going right
        targetPlayer = None
        if (newdx > 0):
            #  going right
            targetPlayer = p2_obj
            #print("target p2")
        else:
            #  going left
            targetPlayer = p1_obj
            #print("target p1")
        
        
        
        #  check if ball hits player    
        #  targetPlayer, nx, ny
        pt = self.BallInterceptPaddle(targetPlayer, nx, ny)
        
        
        
        #  check pt
        if (pt):
            print("Hit??")
            direction = pt[2]
            ptx = pt[0]
            pty = pt[1]
            
            if (USED_PHYSICS_MODEL == 1):
                #  Find the direction of collision
                if (direction == "L" or direction == "R"):
                    newx = ptx
                    newdx = -newdx
                    print("Horizontal hit?")
                    if targetPlayer == p1_obj:
                        ball_event = BALL_EVENT_P1_HORIZONTAL
                    else:
                        ball_event = BALL_EVENT_P2_HORIZONTAL
                    
                elif (direction == "T" or direction == "B"):
                    newy  = pty
                    newdy = -newdy
                    print("Vertical Hit?")
                    if targetPlayer == p1_obj:
                        ball_event = BALL_EVENT_P1_VERTICAL
                    else:
                        ball_event = BALL_EVENT_P2_VERTICAL
                
                #  change speed of ball based on the direction of paddle and ball at collision moment
                if (COLLISION_VERTICAL_SPEED_CHANGE):
                    oldDy = newdy
                    if (targetPlayer.goingUp):
                        if (newdy < 0):
                            newdy = newdy * COLLISION_VERTICAL_SPEED_MULTIPLIER
                            print("increased ball speed from {0} to {1}".format(oldDy, newdy))
                        else:
                            newdy = newdy // COLLISION_VERTICAL_SLOW_MULTIPLIER
                            print("decreased ball speed from {0} to {1}".format(oldDy, newdy))
                    elif (targetPlayer.goingDown):
                        if (newdy < 0):
                            newdy = newdy // COLLISION_VERTICAL_SLOW_MULTIPLIER
                            print("decreased ball speed from {0} to {1}".format(oldDy, newdy))
                        else:
                            newdy = newdy * COLLISION_VERTICAL_SPEED_MULTIPLIER
                            print("increased ball speed from {0} to {1}".format(oldDy, newdy))
            elif (USED_PHYSICS_MODEL == 2):
                
            
                print("player y: {0}, intersect y: {1}".format(targetPlayer.y, pty))
                
                relativeIntersectY = (targetPlayer.y + (PLAYER_HEIGHT/2)) - pty
                print("relativeIntersectY: {0}".format(relativeIntersectY))
                
                normalizedRelativeIntersectionY = (relativeIntersectY/(PLAYER_HEIGHT/2))
                bounceAngle = normalizedRelativeIntersectionY * COLLISION_MAX_BOUNCE_ANGLE
                bounceAngleRadians = math.radians(bounceAngle)
                print("norm:{0},  bounce angle: {1}".format(normalizedRelativeIntersectionY,bounceAngle))
                
                
                #  does not change total ball speed, just change direction
                print("old speeds: ({0}, {1})".format(newdx, newdy))
                currentSpeed = math.sqrt(newdx * newdx + newdy * newdy)
                newdx = -sign(newdx) * currentSpeed * math.cos(bounceAngleRadians)
                newdy = -currentSpeed * math.sin(bounceAngleRadians)
                print("new speeds: ({0}, {1})".format(newdx, newdy))
                
                """
                #  position of the ball before this frame
                oldX = self.x
                oldY = self.y
                
                #  position of the ball without collision
                nextX = newx
                nextY = newy
                """
                
                
                
        
        #  update ball 
        self.x = newx
        self.y = newy
        self.dx = newdx
        self.dy = newdy


        return ball_event


    def Draw(self):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.radius, self.radius))

#gameDisplay = pygame.display.set_mode((display_width, display_height))
#gameDisplay = pygame.Surface((display_width, display_height))
clock = pygame.time.Clock()



def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action= None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)











      
class Pong():
    def __init__(self):
        self.ball = Ball()
        
        #  tracker variables for keyboard keys (keyboard key ???)
        self.W_PRESSED = 0
        self.S_PRESSED = 0
        self.UP_PRESSED = 0
        self.DOWN_PRESSED = 0
        
        
        #  which AIs computer player are going to use
        self.COMPUTER_1_AI = INPUT_TYPE_COMPUTER_KURALBAZ
        self.COMPUTER_2_AI = INPUT_TYPE_COMPUTER_KURALBAZ
    
        
    
    def SaveGameScreen(self, outFileName='out.png'):
        view = pygame.surfarray.pixels3d(gameDisplay)
        #  TO DO: check if this transpose is neccesary
        #  f
        view = view.transpose([1, 0, 2])
        #print(view.shape);
        
        img = Image.fromarray(view, 'RGB')
        img.save(outFileName)
    
    def GetGameScreen(self):
        return pygame.surfarray.pixels3d(gameDisplay)
    
    
    """  AI INPUT FUNCTIONS  """
    def RandomComputerAI(self, ):
        c = PlayerInput(0, 0, 0)
        toss = random.randint(0, 1)
        if (toss == 0):
            #  up
            c.up = 1
        else:
            # down
            c.down = 1
        
        return c
   
    def KuralbazComputerAI(self, playerObject):
        c = PlayerInput(0, 0, 0)
        ballY = self.ball.y
        playerY = playerObject.y
        diff = ballY - playerY
        direction = 0
        
        #print(diff)
        
        if (diff > 0):
            direction = 1
            c.down = 1
        else:
            direction = -1
            c.up = 1
        
        return c
        
        
        
        
        
        


    def ReadComputerInput(self, input_type, playerObject):
        if (input_type == INPUT_TYPE_COMPUTER_RANDOM):
            return self.RandomComputerAI()
        elif (input_type == INPUT_TYPE_COMPUTER_KURALBAZ):
            return self.KuralbazComputerAI(playerObject)
        else:
            return PlayerInput(0, 0, 0)
    
    
    
    
    
    def ReadInputs(self, p1_input_type, p2_input_type):
        c1 = PlayerInput(0, 0, 0)
        c2 = PlayerInput(0, 0, 0)
        p1 = PlayerInput(0, 0, 0)
        p2 = PlayerInput(0, 0, 0)
        
        #  read player inputs
        #  belki bu ifi koyarim
        #if p1_input_type == INPUT_TYPE_PLAYER_1 or p2_input_type == INPUT_TYPE_PLAYER_2:
        
        
        for e in pygame.event.get():
            if e.type == QUIT:
                p1.bitir = p2.bitir = c1.bitir = c2.bitir = 1
                return (p1, p2)
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    p1.bitir = p2.bitir = c1.bitir = c2.bitir = 1
                    return (p1, p2)
                elif e.key == K_w:
                    #p1.up = 1
                    self.W_PRESSED = 1
                elif e.key == K_s:
                    #p1.down = 1
                    self.S_PRESSED = 1
                elif e.key == K_UP:
                    #p2.up = 1
                    self.UP_PRESSED = 1
                elif e.key == K_DOWN:
                    #p2.down = 1
                    self.DOWN_PRESSED = 1
            elif e.type == KEYUP:
                if e.key == K_w:
                    #p1.up = 0
                    self.W_PRESSED = 0
                elif e.key == K_s:
                    #p1.down = 0
                    self.S_PRESSED = 0
                elif e.key == K_UP:
                    #p2.up = 0
                    self.UP_PRESSED = 0
                elif e.key == K_DOWN:
                    #p2.down = 0
                    self.DOWN_PRESSED = 0
        
        
        #  process player 1 inputs
        if self.W_PRESSED:
            p1.up = 1
        elif self.S_PRESSED:
            p1.down = 1
        
        #  process player 2 inputs
        if self.UP_PRESSED:
            p2.up = 1
        elif self.DOWN_PRESSED:
            p2.down = 1
        
        #  read computer inputs
        if p1_input_type != INPUT_TYPE_PLAYER_1:
            c1 = self.ReadComputerInput(p1_input_type, p1_obj)
        if p2_input_type != INPUT_TYPE_PLAYER_2:
            c2 = self.ReadComputerInput(p2_input_type, p2_obj)
        
        
        #  detect null inputs
        if (p1_input_type == INPUT_TYPE_NULL):
            c1 = PlayerInput(0, 0, 0)
        if (p2_input_type == INPUT_TYPE_NULL):
            c2 = PlayerInput(0, 0, 0)
            
        
        #  decide which inputs to return pp, pc, cp, cc
        if (p1_input_type == INPUT_TYPE_PLAYER_1 and p2_input_type == INPUT_TYPE_PLAYER_2):
            return (p1, p2)
        elif (p1_input_type == INPUT_TYPE_PLAYER_1 and p2_input_type != INPUT_TYPE_PLAYER_2):
            return (p1, c2)
        elif (p1_input_type != INPUT_TYPE_PLAYER_1 and p2_input_type == INPUT_TYPE_PLAYER_2):
            return (c1, p2)
        else:
            return (c1, c2)
        
    
    
    
    def UpdateGame(self, input1, input2):
        
        #global p1_obj
        #global p2_obj
        #  check if finished
        if (input1.bitir or input2.bitir):
            quit()
        
        #  process inputs of player 1
        p1Dir = 0
        if (input1.up == 1):
            p1Dir += -1
        if (input1.down == 1):
            p1Dir += 1
        
        #  process inputs of player 2
        p2Dir = 0
        if (input2.up == 1):
            p2Dir += -1
        if (input2.down == 1):
            p2Dir += 1
        
        #  move player objects
        p1_obj.move_player_vertical(p1Dir*PLAYER_SPEED)
        p2_obj.move_player_vertical(p2Dir*PLAYER_SPEED)
        
        """
        p1_obj.y += p1Speed
        p2_obj.y += p2Speed
        """
        
        #  move the ball (calculate next position of the ball)
        ball_event = self.ball.Roll()
        
                
        #  check if ball hit something
        if ball_event == BALL_EVENT_NOTHING:
            #  if no collision occured, check for goal
            if (self.ball.x > display_width):
                print("P1_SCORE")
                #pygame.time.wait(5000)
                return RESULT_PLAYER_1_WIN
            elif (self.ball.x < 0):
                print("P2_SCORE")
                #pygame.time.wait(5000)
                return RESULT_PLAYER_2_WIN
        else:
            if ball_event == BALL_EVENT_P1_HORIZONTAL or ball_event == BALL_EVENT_P1_VERTICAL:
                #  ball hit player 1
                print("Ball hit player 1")
                return RESULT_PLAYER_1_HIT
            elif ball_event == BALL_EVENT_P2_HORIZONTAL or ball_event == BALL_EVENT_P2_VERTICAL:
                #  ball hit player 2
                print("Ball hit player 2")
                return RESULT_PLAYER_2_HIT
        
        
        #  continue game
        return RESULT_GAME_CONTINUE
        


    def Draw(self):
        #  Completely redraw the surface, starting with background
        #main_surface.fill((0, 200, 255))
        #pygame.draw.rect(gameDisplay, (0, 200, 255),(0,0,display_width,display_height))
        gameDisplay.fill(black)
        
        #  draw players
        p1_obj.Draw()
        p2_obj.Draw()
        
        #  draw ball
        self.ball.Draw()
        
        #  update screen
        pygame.display.update()
    
    def DrawInternal(self):
        gameDisplay.fill(black)
        
        #  draw players
        p1_obj.Draw()
        p2_obj.Draw()
        
        #  draw ball
        self.ball.Draw()
        


    def play_mode_pvp(self):
        self.ball.GiveRandomDirection()
        while True:
            #  read player inputs
            (input1, input2) = self.ReadInputs(INPUT_TYPE_PLAYER_1, INPUT_TYPE_PLAYER_2)
            #  physics falan
            self.UpdateGame(input1, input2)
            #  draw
            self.Draw()
            #  wait
            clock.tick(FPS)
    
    def play_mode_pvc(self):
        self.ball.GiveRandomDirection()
        while True:
            #  read player inputs
            (input1, input2) = self.ReadInputs(INPUT_TYPE_PLAYER_1, self.COMPUTER_2_AI)
            #  physics falan
            self.UpdateGame(input1, input2)
            #  draw
            self.Draw()
            #  wait
            clock.tick(FPS)
    
    def play_mode_cvc(self):
        self.ball.GiveRandomDirection()
        #gameDisplay.get_view()
        
        while True:
            #  read player inputs
            (input1, input2) = self.ReadInputs(self.COMPUTER_1_AI, self.COMPUTER_2_AI)
            #  physics falan
            self.UpdateGame(input1, input2)
            #  draw
            self.Draw()
            #  wait
            clock.tick(FPS)

    
    
    def start_ismagil(self, opponent_ai):
        global gameDisplay
        gameDisplay = pygame.Surface((display_width, display_height))
        
        self.ball.GiveRandomDirection()
        self.DrawInternal()
        self.Computer_1_AI = opponent_ai
        self.Computer_2_AI = opponent_ai
        
        
        return self.GetGameScreen()
    
    def action_ismagil(self, action, whichPlayer):
        
        #  Read ismagil's input
        ismagilInput = PlayerInput(0, 0, 0)
        if (action == -1):
            ismagilInput.down = 1
        elif (action == 0):
            print("asd")
        elif (action == 1):
            ismagilInput.up = 1
        else:
            raise ValueError
        
        
        #  read opponent AI's input
        AIInput = None
        if (whichPlayer == 1):
            (input1, input2) = self.ReadInputs(INPUT_TYPE_NULL, self.Computer_2_AI)
            AIInput = input2
        elif (whichPlayer == 2):
            (input1, input2) = self.ReadInputs(self.Computer_1_AI, INPUT_TYPE_NULL)
            AIInput = input1
        
        
        #  Execute moves
        result = None
        if (whichPlayer == 1):
            result = self.UpdateGame(ismagilInput, AIInput)
        elif (whichPlayer == 2):
            result = self.UpdateGame(AIInput, ismagilInput)
        
        
        #  draw to buffer
        self.DrawInternal()
        #self.Draw()
        
        
        return result
        


    def play_menu(self):
        pMenu = True

        while pMenu:

            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            #largeText = pygame.font.SysFont("comicsansms", 115)
            #TextSurf, TextRect = text_objects("Buyuk Proje", largeText)
            #TextRect.center = ((display_width / 2), (display_height / 6))
            #gameDisplay.blit(TextSurf, TextRect)
            
            #pygame.draw.circle(gameDisplay, red, (100, 100), 50, 5);

            button("2 Players", 350, 50, 100, 50, white, white, self.play_mode_pvp)
            button("Player vs Computer", 350, 125, 100, 50, white, white, self.play_mode_pvc)
            button("Computer vs Computer", 350, 200, 100, 50, white, white, self.play_mode_cvc)
            button("Computer vs Computer (FAST)", 350, 275, 100, 50, white, white)
            button("Multiplayer(LAN)", 350, 350, 100, 50, white, white)
            button("Back to Title", 350, 500, 100, 50, white, white, self.game_intro)

            pygame.display.update()
            clock.tick(15)


    def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            gameDisplay.fill(white)
            largeText = pygame.font.SysFont("comicsansms", 115)
            TextSurf, TextRect = text_objects("Buyuk Proje PONG", largeText)
            TextRect.center = ((display_width / 2), (display_height / 6))
            gameDisplay.blit(TextSurf, TextRect)

            button("Play", 350, 250, 100, 50, green, bright_green, self.play_menu)
            button("Options", 350, 350, 100, 50, red, bright_red)
            button("Exit", 350, 450, 100, 50, red, bright_red, pygame.quit)

            pygame.display.update()
            clock.tick(15)




if __name__ == '__main__':
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    game = Pong()
    game.game_intro()
    pygame.quit()
    quit()



class Simulator():
    def __init__(self):
        self.gameObject = None
        self.opponentAI = None
        self.whichPlayer = 0
        
        #  defice which player Ismagil going to play as
        toss = random.randint(0, 1)
        if (toss == 0):
            #  Player 1
            self.whichPlayer = 1
        else:
            #  Player 2
            self.whichPlayer = 2
        
        
    

    def Start(self, opponent_ai = INPUT_TYPE_COMPUTER_KURALBAZ):
        self.gameObject = Pong()
        self.opponentAI = opponent_ai
        return self.gameObject.start_ismagil(opponent_ai)
    


    def Action(self, act):
        result = self.gameObject.action_ismagil(act, self.whichPlayer)
        
        #  next state after one action
        s = self.gameObject.GetGameScreen()
        
        
        #  no intermediate reward for ismagil
        r = 0
        
        
        #  whether game is finished or not
        d = 0
        if (result == RESULT_PLAYER_1_WIN or result == RESULT_PLAYER_2_WIN):
            d = 1
            
            if (result == RESULT_PLAYER_1_WIN and self.whichPlayer == 1):
                r = 1
            elif (result == RESULT_PLAYER_2_WIN and self.whichPlayer == 2):
                r = 1
            else:
                r = -1
            
            
  
        
        return (s, r, d)
        
        
    def Visualize(self):
        raise NotImplementedError
        #print("Visualize_Ismagil() --- This function will not be implemented")
        

    def SaveScreen(self, imageFileName="outIsmail.png"):
        self.gameObject.SaveGameScreen(imageFileName)
