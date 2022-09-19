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
    #Removes "noise" from image
    frame = cv.medianBlur(frame, 3)
    #Inverts image so no longer upside-down
    frame = frame.swapaxes(0, 1)
    return frame
    

def applyCameraFilters(frame):
    #Changes color gamut to RGB
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return frame

def prepareFrame(frame, savedContours):
    #Applies transformations on frame to prepare it for next steps
    frame = processFrame(frame)
    #Find contours
    contours = findContours(frame)
    #Apply filters to webcam frame
    frame = applyCameraFilters(frame)
    #Draws live contours onto frame
    cv.drawContours(frame, contours, -1, (0, 255, 0), 3)
    #Draws saved contours onto frame
    cv.drawContours(frame, savedContours, -1, (255, 0, 0), 3)
    return frame, contours

#draws an image onto the screen
def drawFrame(frame, screen): 
    #Prepares image for display on pygame screen
    frame = pygame.surfarray.make_surface(frame)
    #Draw frame onto screen
    screen.blit(frame, (0, 0))
    #Update screen
    pygame.display.update()

#Called every frame of the vision stage
def visionStep(screen, camera, savedContours):
    currentFrame = getImage(camera)
    currentFrame, contours = prepareFrame(currentFrame, savedContours)
    drawFrame(currentFrame, screen)
    events = getEvents()
    savedContours = checkSaveNewContours(savedContours, contours, events)
    return checkExit(events), savedContours

def findContours(frame):
    contourFrame = frame.copy()
    #Contours are better detected on a grayscale image
    contourFrame = cv.cvtColor(contourFrame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(contourFrame, 127, 1000, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return contours

def getEvents():
    return pygame.event.get()

#Checks if new a set of contours were saved
def checkSaveNewContours(savedContours, contours, events):
    for e in events:
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                return contours
    return savedContours
        
#Detects "X" button, "Esc" key, and "Q" key
#Quits if they are triggered
def checkExit(events):
    for e in events:
        if e.type == pygame.QUIT:
                return True
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE or e.key == K_q:
                sys.exit(0)
            elif e.key == K_RETURN:
                sys.exit(0)
    return False