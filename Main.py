import gamePhysics
import vision

import time

def main():
    #initialize vision
    camera = gamePhysics.initCamera()
    width = gamePhysics.getWidth(camera)
    height = gamePhysics.getHeight(camera)
    screen = gamePhysics.initScreen(width, height)

    #initialize game

    #Run vision until capture taken or program quit
    while gamePhysics.visionStep(screen, camera):
        pass
    #Run game until guy dies or quit key pressed

    #Either back to vision or quit
    print("finished")


main()