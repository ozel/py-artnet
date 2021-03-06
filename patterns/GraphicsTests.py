from Tools.Graphics import Graphics, BLACK, GREEN, RED, CYAN, YELLOW
from matrix import matrix_width, matrix_height
import random


class GraphicsPixelTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = GREEN
        self.pos = (random.randint(1, matrix_width - 1),
                    random.randint(1, matrix_height - 1))
        self.speed = 1
        self.deltax, self.deltay = self.speed, self.speed

    def generate(self):
        self.graphics.fill(BLACK)
        x, y = self.pos
        self.graphics.drawPixel(x, y, self.color)
        if x >= matrix_width - 1 or x <= 0:
            self.deltax *= -1
        if y >= matrix_height - 1 or y <= 0:
            self.deltay *= -1
        self.pos = x + self.deltax, y + self.deltay
        return self.graphics.getSurface()


class GraphicsLineTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = YELLOW
        self.pos = 0, 0

    def generate(self):
        self.graphics.fill(BLACK)
        x, y = self.pos
        self.graphics.drawLine(matrix_width - x, matrix_height - y,
                               x, y, self.color)
        if x >= matrix_height:
            x = 0
            y = 0
        self.pos = x + 1, y
        return self.graphics.getSurface()


class GraphicsRectTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = CYAN
        self.rect_size = matrix_width
        self.pos = 0, 0

    def generate(self):
        # clear the drawing surface
        self.graphics.fill(BLACK)
        # put a rectangle on the surface
        x, y = self.pos
        if x >= matrix_width:
            x = 0
        if y >= matrix_height:
            y = 0
        self.graphics.drawRect(x, y, matrix_width - x,
                               matrix_height - y, self.color)
        self.pos = x + 1, y + 1
        # get te surface drawn
        return self.graphics.getSurface()


class GraphicsCircleTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.radius = 0
        self.direction = 1
        self.color = RED

    def generate(self):
        # clear the drawing surface
        self.graphics.fill(BLACK)
        # put a circle on our surface
        self.graphics.drawCircle(matrix_width / 2, matrix_height / 2,
                                 self.radius, self.color)

        # circle grows and shrinks based on direction.
        if self.direction:
            self.radius += 1
        else:
            self.radius -= 1

        # if the circle is to big or to small inverse growth direction.
        if self.radius >= (matrix_height / 2) or self.radius <= 0:
            self.direction = not self.direction

        # get the surface drawn
        return self.graphics.getSurface()


class GraphicsDotTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = (123, 111, 222)

    def generate(self):
        self.graphics.fill(BLACK)
        for i in range(0, 5):
            self.graphics.drawPixel(i, i, self.color)
        return self.graphics.getSurface()
