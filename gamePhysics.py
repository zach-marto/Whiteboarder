import pygame
from pygame.locals import *
import cv2 as cv
import sys

def testPrint():
    print("joe mama")

#sets up the cv camera, which is used to take images from the webcam
def initCamera():
    return cv.VideoCapture(0)

def getWidth(cam):
    frame = getImage(cam)
    return len(frame[0])

def getHeight(cam):
    frame = getImage(cam)
    return len(frame)

#creates pygame screen which will be used to display webcam + game images
def initScreen(width, height):
    pygame.init()
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    return pygame.display.set_mode([width, height])

#gets current image on the camera
def getImage(cam):
    retval, frame = cam.read()
    return frame

#flips an image
def flipImage(img):
    return cv.flip(img, 1)

#Image filters and transformations to prepare it for display on-screen
#and contour detection
def processFrame(frame):
    #Changes color gamut to RGB
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #Removes "noise" from image
    frame = cv.medianBlur(frame, 3)
    #Inverts image so no longer upside-down
    frame = frame.swapaxes(0, 1)
    #Prepares image for display on pygame screen
    frame = pygame.surfarray.make_surface(frame)
    return frame

#draws an image onto the screen
def drawFrame(frame, screen):
    frame = processFrame(frame)
    #Draw to pygame screen & redraw the screen
    screen.blit(frame, (0, 0))
    pygame.display.update()

#Called every frame of the vision stage
def visionStep(screen, camera):
    currentFrame = getImage(camera)
    drawFrame(currentFrame, screen)
    checkQuit()
    return True

#Detects "X" button, "Esc" key, and "Q" key
#Quits if they are triggered
def checkQuit():
     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                sys.exit(0)