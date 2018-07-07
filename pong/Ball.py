import pygame
from pygame.locals import *
from macros import *
import random
from utils import *
import math

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
    
    def Roll(self, p1_obj, p2_obj):
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
            #print("Hit??")
            direction = pt[2]
            ptx = pt[0]
            pty = pt[1]
            
            if (USED_PHYSICS_MODEL == 1):
                #  Find the direction of collision
                if (direction == "L" or direction == "R"):
                    newx = ptx
                    newdx = -newdx
                    #print("Horizontal hit?")
                    if targetPlayer == p1_obj:
                        ball_event = BALL_EVENT_P1_HORIZONTAL
                    else:
                        ball_event = BALL_EVENT_P2_HORIZONTAL
                    
                elif (direction == "T" or direction == "B"):
                    newy  = pty
                    newdy = -newdy
                    #print("Vertical Hit?")
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


    def Draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.radius, self.radius))
