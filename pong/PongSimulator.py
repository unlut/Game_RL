from macros import *
import pong
from pong import *
import pygame
from pygame.locals import *
import random

class PongSimulator():
    def __init__(self):
        self.gameObject = None
        self.opponentAI = None
        self.whichPlayer = 0
        self.displayMode = 0
        self.terminated = False
        
        #  define which player Ismagil going to play as
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
    
    
    def Restart(self):
        oldOpponentAI = self.opponentAI
        oldDisplayMode = self.displayMode
        
        #  call init
        self.__init__()
        
        #  simulate start
        self.gameObject = Pong()
        self.opponentAI = oldOpponentAI
        self.displayMode = oldDisplayMode
        return self.gameObject.start_ismagil(oldOpponentAI)
    


    def Action(self, act):
        result = self.gameObject.action_ismagil(act, self.whichPlayer, self.displayMode)
        
        #  next state after one action
        s = self.gameObject.GetGameScreen()
        
        
        #  no intermediate reward for ismagil
        r = 0
        
        
        #  whether game is finished or not
        d = 0
        if (result == RESULT_PLAYER_1_WIN or result == RESULT_PLAYER_2_WIN):
            self.terminated = True
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
    
    
    def SetDisplayMode(self, dispMode):
        #global pong.gameDisplay
        
        if (dispMode == 0):
            pong.gameDisplay = pygame.Surface((display_width, display_height))
            self.displayMode = dispMode
        elif (dispMode == 1):
            pong.gameDisplay = pygame.display.set_mode((display_width, display_height))
            self.displayMode = dispMode
            
