import pygame
from pygame.locals import *
import time
import random
import math    #  trigonometry functions

#  to export game screen buffer
from PIL import Image
import numpy as np

#  diger dosyalar
from PlayerObject import *
from macros import *
from Ball import *
from utils import *
from pygame_utils import *

#  initialize pygame
pygame.init()


#  bi class iste
class PlayerInput:
    def __init__(self, up, down, bitir):
        self.up = up
        self.down = down
        self.bitir = bitir


p1_obj = PlayerObject(0+PLAYER_HORIZONTAL_OFFSET, display_height/2, 0, 0, red)
p2_obj = PlayerObject(display_width - PLAYER_HORIZONTAL_OFFSET, display_height/2, 0, 0, blue)
p1_input = PlayerInput(0, 0, 0)
p2_input = PlayerInput(0, 0, 0)


#gameDisplay = pygame.display.set_mode((display_width, display_height))
#gameDisplay = pygame.Surface((display_width, display_height))
clock = pygame.time.Clock()
      
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
        ball_event = self.ball.Roll(p1_obj, p2_obj)
                
        #  check if ball hit something
        if ball_event == BALL_EVENT_NOTHING:
            #  if no collision occured, check for goal
            if (self.ball.x > display_width):
                #print("P1_SCORE")
                #pygame.time.wait(5000)
                return RESULT_PLAYER_1_WIN
            elif (self.ball.x < 0):
                #print("P2_SCORE")
                #pygame.time.wait(5000)
                return RESULT_PLAYER_2_WIN
        else:
            if ball_event == BALL_EVENT_P1_HORIZONTAL or ball_event == BALL_EVENT_P1_VERTICAL:
                #  ball hit player 1
                #print("Ball hit player 1")
                return RESULT_PLAYER_1_HIT
            elif ball_event == BALL_EVENT_P2_HORIZONTAL or ball_event == BALL_EVENT_P2_VERTICAL:
                #  ball hit player 2
                #print("Ball hit player 2")
                return RESULT_PLAYER_2_HIT
        
        #  continue game
        return RESULT_GAME_CONTINUE
        
    def Draw(self):
        #  Completely redraw the surface, starting with background
        #main_surface.fill((0, 200, 255))
        #pygame.draw.rect(gameDisplay, (0, 200, 255),(0,0,display_width,display_height))
        gameDisplay.fill(black)
        
        #  draw players
        p1_obj.Draw(gameDisplay)
        p2_obj.Draw(gameDisplay)
        
        #  draw ball
        self.ball.Draw(gameDisplay)
        
        #  update screen
        pygame.display.update()
    
    def DrawInternal(self):
        gameDisplay.fill(black)
        
        #  draw players
        p1_obj.Draw(gameDisplay)
        p2_obj.Draw(gameDisplay)
        
        #  draw ball
        self.ball.Draw(gameDisplay)
        
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
        while True:
            #  read player inputs
            (input1, input2) = self.ReadInputs(self.COMPUTER_1_AI, self.COMPUTER_2_AI)
            #  physics falan
            self.UpdateGame(input1, input2)
            #  draw
            self.Draw()
            #  wait
            clock.tick(FPS)
    
    def play_mode_cvc_fast(self):
        self.ball.GiveRandomDirection()
        while True:
            #  read player inputs
            (input1, input2) = self.ReadInputs(self.COMPUTER_1_AI, self.COMPUTER_2_AI)
            #  physics falan
            self.UpdateGame(input1, input2)
            #  draw
            self.Draw()
            #  wait
            #clock.tick(FPS)
    
    def start_ismagil(self, opponent_ai):
        global gameDisplay
        gameDisplay = pygame.Surface((display_width, display_height))
        
        self.ball.GiveRandomDirection()
        self.DrawInternal()
        self.Computer_1_AI = opponent_ai
        self.Computer_2_AI = opponent_ai
        
        return self.GetGameScreen()
    
    def action_ismagil(self, action, whichPlayer, dispMode):
        #  Read ismagil's input
        ismagilInput = PlayerInput(0, 0, 0)
        if (action == -1):
            ismagilInput.down = 1
        elif (action == 0):
            pass
            #print("asd")
        elif (action == 1):
            ismagilInput.up = 1
        else:
            raise ValueError
        
        #  read opponent AI's input
        AIInput = None
        if (self.Computer_1_AI == 0 and self.Computer_2_AI == 0):
            #  user wants to use custom AI
            pass
        else:            
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
        if (dispMode == 0):
            self.DrawInternal()
        elif (dispMode == 1):
            self.Draw()
        
        return result

    def play_menu(self):
        pMenu = True
        clock.tick(15)
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
            
            button(gameDisplay, "2 Players", 350, 50, 100, 50, white, white, self.play_mode_pvp)
            button(gameDisplay, "Player vs Computer", 350, 125, 100, 50, white, white, self.play_mode_pvc)
            button(gameDisplay, "Computer vs Computer", 350, 200, 100, 50, white, white, self.play_mode_cvc)
            button(gameDisplay, "Computer vs Computer (FAST)", 350, 275, 100, 50, white, white, self.play_mode_cvc_fast)
            button(gameDisplay, "Multiplayer(LAN)", 350, 350, 100, 50, white, white)
            button(gameDisplay, "Back to Title", 350, 500, 100, 50, white, white, self.game_intro)

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

            button(gameDisplay, "Play", 350, 250, 100, 50, green, bright_green, self.play_menu)
            button(gameDisplay, "Options", 350, 350, 100, 50, red, bright_red)
            button(gameDisplay, "Exit", 350, 450, 100, 50, red, bright_red, pygame.quit)

            pygame.display.update()
            clock.tick(15)


if __name__ == '__main__':
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    game = Pong()
    game.game_intro()
    pygame.quit()
    quit()
