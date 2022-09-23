import pygame
import random
import math
import sys
from pygame.locals import *
import numpy as np


background_colour = (255, 255, 255)
drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.001)
touching = False




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
    touching = False
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

    if pygame.Rect.colliderect(pygame.Rect(px, py, particle.radius, particle.radius), pygame.Rect(min(xend, xstart), min(yend, ystart), abs(xend-xstart), abs(yend-ystart))): #checks if particle is actually colliding with line and not a ghost line
        if height <= particle.radius:
            touching = True
        if touching == True: #computes the particle's new direction
            lineXCompenent = line.xend - line.xstart
            lineYCompenent = line.yend - line.ystart
            lineAngle = math.degrees(math.atan(lineYCompenent/lineXCompenent))

            particleAngle = math.degrees(particle.angle)

            angleDifferences = particleAngle - lineAngle
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

    def bounce(self, width, height):
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


player = Particle(500, 500, 20)


class Line():
    def __init__(self, xstart, ystart, xend, yend):
        self.xstart = xstart
        self.ystart = ystart
        self.xend = xend
        self.yend = yend
        self.thickness = 5
        self.color = (0, 0, 0)
        start = []
        end = []
    def draw(self, screen):
        pygame.draw.line(screen, self.color, (int(self.xstart), int(self.ystart)), (int(self.xend), int(self.yend)), self.thickness)

lines = []
#eventually import lines coords from Main here
lines.append(Line(400, 400, 300, 200))
lines.append(Line(50, 50, 200, 200))
touchedLine = []
for x in range(len(lines)):
    touchedLine.append(0)

player = Particle(500, 500, 20)
running = True
def contourToLineArr(contours, width, height):
    print(contours[0])
    print(contours[0][0])
    print(contours[0][0][0])
    print(contours[0][0][0][0])


    # xStart = []
    # yStart = []
    # xEnd = []
    # yEnd = []

    # x = []
    # y = []
    # for i in range(0, len(contours)):

    #     for r in range(len(contours[i])):
    #         x.append(contours[i][r][0][0])
    #         y.append(contours[i][r][0][1])

    # tmp = []
    # for i in range(len(xStart)):
    #     print((xStart[i], yStart[i], xEnd[i], yEnd[i]))
    #     tmp.append(Line(xStart[i], yStart[i], xEnd[i], yEnd[i]))
    return []
def gameStep(screen, width, height, selected_particle, lines):
    for event in pygame.event.get():
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

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5 * math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.005

    screen.fill(background_colour)

    for i, Line in enumerate(lines):
        collideLine(player, lines[i])
        lines[i].draw(screen)

    player.move()
    player.bounce(width, height)
    player.display(screen)

    pygame.display.flip()
    return selected_particle
