from Tools.Graphics import Graphics, BLUE, BLACK
from matrix import matrix_width, matrix_height
import random

from pygame.locals import *
import pygame


class PixelScanner(object):
    # version before creating players that handle processing on thier own.
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = BLUE
        x = 0 #random.randint(1, matrix_width - 1)
        y = 0 #3random.randint(1, matrix_height - 1)
        self.pos = x, y
        self.speed = 1
        self.deltax, self.deltay = 0, 0
        self.body = []
        # add our head to our body :)
        self.body.append(self.pos)
        # self.player1 = TronPlayer(BLUE, self)
        # self.player1.update(self)
        # self.player1.draw()
        pygame.init()
        self.window = pygame.display.set_mode((80, 60))
        self.debug = False
        pygame.key.set_repeat(1000, 1000)

    def inputHandling(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.deltax = 0
            self.deltay = 1
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.deltax = 0
            self.deltay = -1
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.deltax = -1
            self.deltay = 0
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.deltax = 1
            self.deltay = 0

        if keys_pressed[pygame.K_e]:
            self.deltax = 5
            self.deltay = 0            
        if keys_pressed[pygame.K_q]:
            self.deltax = -5
            self.deltay = 0

    def update(self):
        x, y = self.pos
        # update position
        x += self.deltax
        y += self.deltay

        # if the tail goes offscreen it appears on the other side.
        if x >= matrix_width:
            x = 0
            self.pos = x, y
        elif x < 0:
            x = matrix_width - 1
            self.pos = x, y
        elif y >= matrix_height:
            y = 0
            self.pos = x, y
        elif y < 0:
            y = matrix_height - 1
            self.pos = x, y
        else:
            self.pos = x, y
        if self.debug:
            print(self.deltax, self.deltay)
            print(x, y)

        # look if our "tail is in the way" and only if we have a tail.
        if len(self.body) > 2:
            if len(self.body) != len(set(self.body)):
                print("GameOver!")
                self.body = [self.pos]
                self.deltax = 0
                self.deltay = 0
        # add current point to tail
        # only if we moved though
        if self.deltax or self.deltay:
            self.body[0] = self.pos
        self.deltay = 0
        self.deltax = 0
    def draw(self):
        for x, y in self.body:
            self.graphics.drawPixel(x, y, self.color)

    def generate(self):
        self.graphics.fill(BLACK)
        self.inputHandling()
        self.update()
        self.draw()
        #self.player1.draw()
        return self.graphics.getSurface()
