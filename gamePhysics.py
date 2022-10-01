import pygame
import math
import sys
from pygame.locals import *
import numpy as np

#Background color of the screen
background_color = (255, 255, 255)
#Player slows down in space due to drag
drag = 0.999
#Determines how strong a bounce is
elasticity = .5
gravity = (math.pi, 0.001)

#Every platform in the game is a line
class Line():
    #xstart and ystart are the first point on the line
    #xend and yend are the second point on the line
    def __init__(self, xstart, ystart, xend, yend):
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.thickness = 6
        self.color = (0, 0, 0)
    def draw(self, screen):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)

#A particle is a circle effected by gravity and collisions
class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    #Draws the particle onto the screen
    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, self.thickness)

    #Moves the particle according to its angle and speed
    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    #Bounces particle off of the screen edges
    def bounce(self, width, height):
        #Right wall
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = - self.angle
            self.speed *= elasticity
        #Left wall
        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = - self.angle
            self.speed *= elasticity
        #Top
        if self.y > height - self.radius:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        
        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

#The player is a particle
player = Particle(500, 500, 20)

#Adds two vectors together
def addVectors(angle1, length1, angle2, length2):
    #Sum of the X compenent of both vectors
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    #Sum of the Y component of both vectors
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)
    return (angle, length)

#Define rectangular hitbox around the player
def buildPlayerHitbox(particle, playerHitboxBuffer):
    px = particle.x
    py = particle.y
    #(px1, py1) is the point at the top left of the hitbox
    #(px2, py2) is the point at the bottom right of the hitbox
    px1 = px - particle.radius + playerHitboxBuffer
    py1 = py - particle.radius + playerHitboxBuffer
    px2 = 2*(particle.radius - playerHitboxBuffer)
    py2 = 2*(particle.radius - playerHitboxBuffer)
    return pygame.Rect(px1, py1, px2, py2)

#Build hitbox for one line
def buildLineHitbox(line, lineHitboxBuffer):
    xstart = line.xstart
    ystart = line.ystart
    xend = line.xend
    yend = line.yend

    #(lx1, ly1) is the point at the top left of the hitbox
    #(lx2, ly2) is the point at the bottom right of the hitbox
    lx1 = min(xend, xstart) - lineHitboxBuffer
    ly1 = min(yend, ystart) - lineHitboxBuffer
    lx2 = abs(xend-xstart) + 2*lineHitboxBuffer
    ly2 = abs(yend-ystart) + 2*lineHitboxBuffer
    return pygame.Rect(lx1, ly1, lx2, ly2)

#If the player's hitbox is in the line's hitbox
def isPlayerInLineHitbox(particle, line, player_hitbox, line_hitbox):
    return pygame.Rect.colliderect(player_hitbox, line_hitbox)

#Checks if the player is colliding with a line
def collideLine(particle, line, player_hitbox, line_hitbox):
    #If the player is outside of the line hitbox, no need to perform any more checks
    #This check is much faster than checking if the player is specifically touching the line
    if not isPlayerInLineHitbox(player, line, player_hitbox, line_hitbox):
        return
    
    px = particle.x
    py = particle.y

    xstart = line.xstart
    ystart = line.ystart
    xend = line.xend
    yend = line.yend

    #To check the distance from the line, we create a triangle with the three vertices:
    #1: the beginning of the line
    #2: the end of the line
    #3: the center of the particle
    side1 = math.sqrt(((xstart-px)*(xstart-px))+((ystart-py)*(ystart-py)))
    side2 = math.sqrt(((xend-xstart)*(xend-xstart))+((yend-ystart)*(yend-ystart)))
    side3 = math.sqrt(((xend - px) * (xend - px)) + ((yend - py) * (yend - py)))
    #Find semiperimeter of the triangle using Heron's formula
    semi = int((side1+side2+side3)/2)
    #Find area of the triangle using the semiperimeter
    area = math.sqrt(abs((semi)*(semi-side1)*(semi-side2)*(semi-side3)))
    #Find the height of the triangle from the area
    height = int((2*area)/side2)

    #The height of the triangle is the distance between the center of the player
    #and the line. We can use this to determine if a player is colliding with the line
    if height <= particle.radius:
        #Determingle the angle of the line
        lineXCompenent = line.xend - line.xstart
        lineYCompenent = line.yend - line.ystart
        lineAngle = math.degrees(math.atan(lineYCompenent/lineXCompenent))
        #Get the angle of the particle
        particleAngle = math.degrees(particle.angle)
        #Set the new angle of the particle after the collision
        newAngle = 180 + lineAngle - particleAngle
        particle.angle = math.radians(newAngle)

#Converts an array of contours into an array of Lines
def contourToLineArr(contours, width, height):
    lines = []
    #For every contour in the contour array
    for i in range(0, len(contours)):
        x = []
        y = []
        #Copy all x and y points in a contour into a new array
        for r in range(len(contours[i])):
            x.append(contours[i][r][0][1])
            y.append(contours[i][r][0][0])

        #Find the smallest and largest x and y points
        minX = np.argmin(x)
        maxX = np.argmax(x)
        minY = np.argmin(y)
        maxY = np.argmax(y)
        #The axis with the greater distance in between the maximum and minimum
        #points is the axis we want to use to determine the line's endpoints
        if abs(minX-maxX) > abs(minY-maxY):
            minY = y[minX]
            maxY = y[maxX]
            minX = x[minX]
            maxX = x[maxX]
        else:
            minX = x[minY]
            maxX = x[maxY]
            minY = y[minY]
            maxY = y[maxY]
        
        #If the line is too small, probably background noise and can
        #eliminate from the array
        if (not (abs(minX-maxX)**2 +  abs(minY-maxY)**2)**.5 > 15):
            continue
        if (minX < 20 or minX > width-20 or minY < 20 or maxY > height-20):
            continue
        #Create line from contour coordiantes and add to array
        lines.append(Line(minX, minY, maxX, maxY))
    return lines

def movePlayerTowardMouse():
    (mouseX, mouseY) = pygame.mouse.get_pos()
    #Distance from player to mouse
    dx = mouseX - player.x
    dy = mouseY - player.y
    #Angle between player and mouse
    player.angle = 0.5 * math.pi + math.atan2(dy, dx)
    #Determine speed amount
    #Greater distance between player and mouse = higher speed
    player.speed = math.hypot(dx, dy) * 0.005

#Checks for keyboard or mouse inputs from the user
def keyActions(events, player_held):
    for event in events:
        #X button in top-left corner
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            #Quit on Escape or 'Q' key pressed
            if event.key == K_ESCAPE or event.key == K_q:
                sys.exit(0)
            #Switch back to vision mode when return key pressed
            elif event.key == K_RETURN:
                return False
        #If the player clicks the mouse, move player toward the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player_held = True
        #Stop moving player toward mouse when released
        elif event.type == pygame.MOUSEBUTTONUP:
            player_held = False
    return True, player_held

def updateEntities(lines, width, height):
    playerHitbox = buildPlayerHitbox(player, 3)
    #Check for collisions between lines and the player
    for l in lines:
        line_hitbox = buildLineHitbox(l, 2)
        collideLine(player, l, playerHitbox, line_hitbox)
    #Update player position
    player.move()
    #Bounce player off walls if necessary
    player.bounce(width, height)

def drawScreen(screen, lines, width, height):
    #Draw background
    screen.fill(background_color)
    #Draw lines
    for l in lines:
        l.draw(screen)
    #Draw player
    player.display(screen)
    #Update screen
    pygame.display.flip()

def gameStep(screen, width, height, lines, player_held):
    #Checks if the user has made any inputs with their keyboard or mouse
    continue_game, player_held = keyActions(pygame.event.get(), player_held)
    #Returns false if the user wishes to switch back to vision mode
    if not continue_game:
        return False, False
    #Move player toward mouse if they click
    if(player_held):
        movePlayerTowardMouse()
    #Collide entities if necessary and update positions
    updateEntities(lines, width, height)
    #Draw player and lines onto the screen & update screen
    drawScreen(screen, lines, width, height)
    #Returns true to signal the game is still running
    #Returns player_held to signal if the mouse is currently holding
    #the player
    return True, player_held