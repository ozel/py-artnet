from matrix import matrix_height, matrix_width
from Tools.Graphics import Graphics, BLACK
import png


def getPngPixelData(image):
    pngobj = png.Reader(image)
    data = pngobj.asRGBA8()
    palette = []
    for d in data[2]:
        palette.append(d)
    size = data[3]['size']
    colordata = []
    for color in palette:
        colordata.append(color[:3])
    return (colordata, size,)


class DisplayPng(object):
    def __init__(self):
        # image = '/home/robert/py-artnet/hacked.png'
        # self.data = getPngPixelData(image)
        # self.pixeldata = self.data[0]
        self.graphics = Graphics(matrix_width, matrix_height)

    def generate(self):
        self.graphics.fill(BLACK)
        return self.graphics.getSurface()
