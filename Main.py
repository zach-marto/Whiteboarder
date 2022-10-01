# CONTROLS:
# 'Q'/Esc - Quit Game
# Space - Capture current Drawing
# Enter/Return - Toggle drawing and game

import gamePhysics
import vision

def main():
    #initialize vision and screen
    camera = vision.initCamera()
    width = vision.getWidth(camera)
    height = vision.getHeight(camera)
    screen = vision.initScreen(width, height)
    #This is the array of contours that will be used in-game
    contours = []

    #Run the vision and game until user quits:
    while True:
        #Determines whether we are in vision mode or game mode
        runGame = False
        #Run vision until capture taken or program quit
        while not runGame:
            runGame, contours = vision.visionStep(screen, camera, contours)
        
        #Process contours into Lines for game to use
        lines = gamePhysics.contourToLineArr(contours, width, height)
        #Stores whether the player is being held by mouse or not
        player_held = False

        #Run game until quit or switch back to vision mode
        while runGame:
            runGame, player_held = gamePhysics.gameStep(
                    screen, width, height, lines, player_held)

main()