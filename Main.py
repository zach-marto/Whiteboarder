# CONTROLS:
# 'Q'/Esc - Quit Game
# Space - Capture current Drawing
# Enter/Return - Toggle drawing and game

# from sqlite3 import ProgrammingError
import gamePhysics
import vision

import time

def main():
    #initialize vision and screen
    camera = vision.initCamera()
    width = vision.getWidth(camera)
    height = vision.getHeight(camera)
    screen = vision.initScreen(width, height)
    #This is the array of contours that will be used in-game
    contours = []

    #initialize game

    #Run vision until capture taken or program quit
    while True:
        runGame = False
        while not runGame:
            runGame, contours = vision.visionStep(screen, camera, contours)
        lines = gamePhysics.contourToLineArr(contours, width, height)
        while runGame:   
            tmp = None
            tmp = gamePhysics.gameStep(screen, width, height, tmp, lines)
            if (tmp == False):
                runGame = False
        
    
    #Run game until guy dies or quit key pressed

    #Either back to vision or quit
    print("finished")


main()