import gamePhysics
import vision

import time

def main():
    #initialize vision
    camera = gamePhysics.initCamera()
    width = gamePhysics.getWidth(camera)
    height = gamePhysics.getHeight(camera)
    screen = gamePhysics.initScreen(width, height)
    #This is the array of contours that will be used in-game
    contours = []

    #initialize game

    #Run vision until capture taken or program quit
    runGame = False
    while not runGame:
        runGame, contours = gamePhysics.visionStep(screen, camera, contours)
    
    #Run game until guy dies or quit key pressed

    #Either back to vision or quit
    print("finished")


main()