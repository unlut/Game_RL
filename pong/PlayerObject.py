import pygame
from pygame.locals import *
from macros import *



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
        
    
    def Draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))
