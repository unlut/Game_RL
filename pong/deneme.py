#  import our favorite game
import pong


#  stuff
import matplotlib.pyplot as plt
import time





#  initialize game simulator
simulator = pong.Simulator()



#  decide which AI you are going to play against
"""
  Available opponent AIs

INPUT_TYPE_COMPUTER_RANDOM = 101
INPUT_TYPE_COMPUTER_KURALBAZ = 102

"""
s0 = simulator.Start(opponent_ai = 102)

#  whichPlayer is 1 for player 1 (left/red)
#  2 for player 2 (right/blue)
whichPlayer = simulator.whichPlayer
print("Playing as player {0}".format(whichPlayer))


#  0 for hide screen
#  1 for show screen
simulator.SetDisplayMode(0)


#  save screenshot of current state
#simulator.Save_Screen("s0.png")


#  simulate a game
#  better loop while checking value of d

devam = True
i = 1
while devam:
    (si, ri, d) = simulator.Action(1)  #  1 UP, 0 stay, -1 down
    #print(si.shape)
    #plt.imshow(si)
    
    
    print("Timestep {0}, reward: {1}".format(i, ri))
    
    
    #  d is 0 for continue, 1 for end
    if d == 1:
        devam = False
        break
        
    
    #  for testing only
    #simulator.Save_Screen(imageFileName = str(i)+".png")
    
    i = i + 1
    
    #time.sleep()
    

