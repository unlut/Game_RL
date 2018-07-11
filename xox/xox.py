from PIL import Image
from PIL import ImageDraw

import time
import pickle
import os.path
import random
from collections import defaultdict
import numpy as np


def DrawGameState(state):
    if (len(state) != 9):
        print("Invalid state!, length of state string must be 9!")

    width = 300
    height = 300
    numRows = 3
    numCols = 3

    #  create empty image
    img = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 255))
    
    #  initialize drawer object
    draw = ImageDraw.Draw(img)

    y_start = 0
    y_end = height
    y_step = int(height / numRows)
    
    x_start = 0
    x_end = width
    x_step = int(width / numCols)


    #  draw horizontal lines
    for y in range(y_start, y_end, y_step):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill=(0, 0, 0, 255))
    
    #  draw vertical lines
    for x in range(x_start, x_end, x_step):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill=(0, 0, 0, 255))
    
    for index, letter in enumerate(state):
        if (letter == "-"):
            continue
        else:
            print(index)
            topLeftX = (width/3) * (index % 3)
            topLeftY = (height/3) * int(index / 3)
            print("({}, {})".format(topLeftX, topLeftY))
            centerX = topLeftX + width/6
            centerY = topLeftY + height/6
            botRightX = topLeftX + width/3
            botRightY = topLeftY + height/3
            if (letter == "X" or letter == "x"):
                #  draw a cross
                draw.line((topLeftX, topLeftY, botRightX, botRightY), fill=(255, 0, 0, 255))
                draw.line((topLeftX+width/3, topLeftY, topLeftX, topLeftY+height/3), fill=(255, 0, 0, 255))
            elif (letter == "O" or letter == "o"):
                #  draw a circle
                radius = width/6-2
                draw.ellipse((topLeftX, topLeftY, botRightX, botRightY), fill=(255, 255, 255, 255), outline=(0, 0, 255, 255))

    img.show()

if __name__ == '__main__':
    #QTable = InitializeQTable()
    gameState = "---------"


    DrawGameState(gameState)