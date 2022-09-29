import pygame
import random
import math
import sys
from pygame.locals import *
import numpy as np


background_colour = (255, 255, 255)
drag = 0.999
elasticity = .5
gravity = (math.pi, 0.001)
touching = False
constantBuffer = 2



def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x - x, p.y - y) <= p.radius:
            return p
    return None


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)
    if dist < p1.radius + p2.radius:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


def collideLine(particle, line): #checks if particle is touching a line
    px = particle.x
    py = particle.y

    xstart = line.xstart
    ystart = line.ystart
    xend = line.xend
    yend = line.yend

    side1 = math.sqrt(((xstart-px)*(xstart-px))+((ystart-py)*(ystart-py)))
    side2 = math.sqrt(((xend-xstart)*(xend-xstart))+((yend-ystart)*(yend-ystart)))
    side3 = math.sqrt(((xend - px) * (xend - px)) + ((yend - py) * (yend - py)))
    semi = int((side1+side2+side3)/2)
    area = math.sqrt(abs((semi)*(semi-side1)*(semi-side2)*(semi-side3)))
    height = int((2*area)/side2)
    poke = 3 # named 3/29/2022 Zachary Marto
    if pygame.Rect.colliderect(pygame.Rect(px-particle.radius+poke, py-particle.radius+poke, 2*particle.radius-2*poke, 2*particle.radius-2*poke), pygame.Rect(min(xend, xstart)-constantBuffer, min(yend, ystart)-constantBuffer, abs(xend-xstart)+2*constantBuffer, abs(yend-ystart)+2*constantBuffer)): #checks if particle is actually colliding with line and not a ghost line
        if height <= particle.radius:
            lineXCompenent = line.xend - line.xstart
            lineYCompenent = line.yend - line.ystart
            lineAngle = math.degrees(math.atan(lineYCompenent/lineXCompenent))
            particleAngle = math.degrees(particle.angle)
            newAngle = 180 + lineAngle - particleAngle
            particle.angle = math.radians(newAngle)
            return True
        return False


class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0

    def display(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.radius, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self, width, height): # bounces ball of screen edges
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.radius:
            self.x = 2 * self.radius - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.radius:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.radius:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


player = Particle(500, 500, 20) # ball creation


class Line():
    def __init__(self, xstart, ystart, xend, yend):
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.thickness = 6
        self.color = (0, 0, 0)
    def draw(self, screen):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)

lines = [] # list of lines to be drawn
#eventually import lines coords from Main here
# touchedLine = []
# for x in range(len(lines)):
#     touchedLine.append(0)

player = Particle(500, 500, 20)
running = True
def contourToLineArr(contours, width, height):
    #contours = [[[[1][1]],[[400][400]]]]


    xStart = []
    yStart = []
    xEnd = []
    yEnd = []
    tmp = []
    for i in range(0, len(contours)):
        x = []
        y = []
        for r in range(len(contours[i])):
            x.append(contours[i][r][0][1])
            y.append(contours[i][r][0][0])

        minX = np.argmin(x)
        maxX = np.argmax(x)
        minY = np.argmin(y)
        maxY = np.argmax(y)
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
        
        if (not (abs(minX-maxX)**2 +  abs(minY-maxY)**2)**.5 > 15):
            continue
        if (minX < 20 or minX > width-20 or minY < 20 or maxY > height-20):
            continue
        tmp.append(Line(minX, minY, maxX, maxY))
    return tmp

def keyActions(events): # actions on key pressed
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_q:
                sys.exit(0)
            elif event.key == K_RETURN:
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = player
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
def gameStep(screen, width, height, selected_particle, lines):
    keyActions(pygame.event.get())
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.005

    screen.fill(background_colour)

    for i in lines:
        collideLine(player, i)
        #pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(player.x-player.radius, player.y-player.radius, 2*player.radius, 2*player.radius))
        #pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(min(i.xend, i.xstart)-constantBuffer, min(i.yend, i.ystart)-constantBuffer, abs(i.xend-i.xstart)+2*constantBuffer, abs(i.yend-i.ystart)+2*constantBuffer))

        i.draw(screen)

    player.move()
    player.bounce(width, height)
    player.display(screen)

    pygame.display.flip()
    return selected_particle
