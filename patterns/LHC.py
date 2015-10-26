"""
complete LHC cycle, from H2 injection to LHC
Oliver Keller, CERN
"""
from matrix import matrix_width, matrix_height
from Tools.Graphics import *
import math
import random

BOT_BEGIN = 0
BOT_END = 19
DUO_BEGIN = 19
DUO_END = 40
LIN_BEGIN = 0
LIN_END = 100
SPS_BEGIN = 0
SPS_END = 170
LHC_BEGIN = 0
LHC_END = 170

bot_pat = [(0,0,127),BLUE,(127,0,0),RED]
duo_pat = [BLACK,BLACK,(107,0,0),RED,(127,0,0)]
lin_pat = [RED,RED,RED]
sps_pat = [(100,100,100),WHITE,(100,100,100)]
lhc_pat = [(127,127,0),YELLOW,(127,127,0)]
global_i = 0

def repeat(times, func, *args, **kwargs):
    for _ in xrange(times):
        yield func(*args, **kwargs)

def parabola (x):
    return x*x

class Bunch():

    def __init__(self, graphics, pattern, min_x, max_x, acc, y, mode=0):
        self.graphics = graphics
        self.pattern = pattern
        self.x = min_x+1
        self.min_x = min_x
        self.max_x = max_x
        self.range = max_x - min_x
        self.y = y
        self.acc = acc
        self.alive = True
        self.mode = mode # lin, sps, lhc  

#    def __del__(self):
        #print('bunch deleted')
        # self.graphics = 0
        # self.pattern = []
        # self.x = 0
        # self.min_x = 0
        # self.max_x = 0
        # self.range = 0
        # self.y = 0
        # self.acc = 0
        # self.alive = False

    def isAlive(self):    
        return self.alive

    def travel(self):
        global global_i

        #self.x = self.min_x + 1*(global_i%self.range) + (self.acc*(global_i%self.range)*(global_i%self.range))/2
        if global_i % 1 == 0:
            self.x =  self.min_x + ((self.x+1) * self.acc)
        #print(self.x)
        if self.x > self.max_x:
            #self.x = self.min_x
            self.alive = False

    def draw(self, cur_x):
        global global_i
        #i = 0
        
        if self.mode == 3:
            offset = LHC_END
            sign = +1
        else:
            offset = 0
            sign = -1
         
        #for color in self.pattern:
        #color = self.pattern[(int(-global_i)%len(self.pattern))]
        self.graphics.drawPixel(self.y, offset-(sign*self.x), self.pattern[1])
        if self.mode >= 2 or (self.mode == 1 and self.x > 20):
            self.graphics.drawPixel(self.y, offset-(sign*self.x-1), self.pattern[2])
            self.graphics.drawPixel(self.y, offset-(sign*self.x+1), self.pattern[0])

        
        # if self.x in list([((x-cur_x)*(x-cur_x)) for x in range(self.min_x, self.max_x)]):
        #     self.graphics.drawPixel(self.y, self.x, RED)
        # else:
        #     self.graphics.drawPixel(self.y, self.x, BLACK)

        # if i-global_i in [(x*x) for x  in xrange(200)]: #in list([((x-i)*(x-i)) for x in xrange(LIN_END)]) :
        #     self.graphics.drawPixel(self.y, pixel, RED) #pattern[(pixel-self.i)%len(pattern)])
        # else:
        #     self.graphics.drawPixel(self.y, pixel, BLACK)
        #i += 



class LHC(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.state = 0  #global state counter
        self.bot_pos = BOT_BEGIN
        self.duo_pos = DUO_BEGIN
        self.lin_pos = LIN_BEGIN
        self.sps_pos = SPS_BEGIN
        self.lhc_pos = LHC_BEGIN
        self.bot_done = False
        self.duo_done = False
        self.lin_done = False
        self.sps_done = False
        self.lhc_done = False
        self.debug = False
        self.graphics.fill(BLACK)
        #self.sqrtable = list(repeat(100,parabola, 1, 100))
        #self.sqrtable = list([x*x/2 for x in xrange (170)])
        self.lin_bunches = list()
        self.sps_bunches = list()
        self.lhc_bunches = list()


    def animateSrtripe(self,pattern, x, min_x, max_x, acc, y):
        global global_i
        
        for pixel in range(min_x,max_x):
            # pixel = math.floor(pixel * acc)
            # pixel = int(pixel)
            # pixel = min(pixel, max_x)
            if x < max_x and x < pixel:
                color = BLACK
            else:
                color = pattern[(pixel-global_i)%len(pattern)]
            self.graphics.drawPixel(y, pixel, color)

    def updateBottle(self):
        self.animateSrtripe(bot_pat, self.bot_pos, BOT_BEGIN, BOT_END,0.5,0) 
        self.bot_pos += 3
        if self.bot_pos >= BOT_END:
            self.bot_done = True
        if self.debug:
            print(self.bot_pos)

    def updateDuoplasmatron(self):
        if self.bot_done : 
            self.animateSrtripe(duo_pat, self.duo_pos,DUO_BEGIN,DUO_END,1,0) 
            self.duo_pos += 1
            if self.duo_pos >= DUO_END:
                self.duo_done = True
            if self.debug:
                print(self.duo_pos)

    def updateLINAC(self, pattern):
        global global_i
        if self.duo_done :
            del_bunches = list()
            for index, bnch in enumerate(self.lin_bunches):
                if bnch.isAlive():
                    #print('ALIVE')
                    bnch.draw(self.lin_pos)    
                    bnch.travel()
                else:
                    self.lin_done = True
                    new_bunch = Bunch(self.graphics, sps_pat, SPS_BEGIN,SPS_END,1,2,1)
                    self.sps_bunches.append(new_bunch)
                    del_bunches.append(index)

            #print ("before bunches", len(self.bunches))                

            for index in sorted(del_bunches, reverse=True):
                del self.lin_bunches[index]
            
            #print ("after bunches", len(self.bunches))

            if  global_i % 10 == 0:
            #if global_i == 0:
                new_bunch = Bunch(self.graphics, pattern, LIN_BEGIN,LIN_END,1.2,1)
                self.lin_bunches.append(new_bunch)
                #print('NEW BUNCH', global_i % 10)

            # self.lin_pos += 1
            # if self.lin_pos >= LIN_END:
            #     self.lin_done = True
            #     self.lin_pos = 0

            if self.debug:
                print(self.lin_pos)
    
    def updateSPS(self,pattern):
        global global_i
        if self.lin_done : 
            # self.animateSrtripe(sps_pat, self.sps_pos,SPS_BEGIN,SPS_END,2,3) 
            # self.sps_pos += 1
            # if self.sps_pos >= SPS_END:
            #     self.sps_done = True
            # if self.debug:
            #     print(self.sps_pos)       
            del_bunches = list()
            for index, bnch in enumerate(self.sps_bunches):
                if bnch.isAlive():
                    #print('ALIVE')
                    bnch.draw(self.sps_pos)    
                    bnch.travel()
                else:
                    self.sps_done = True
                    new_bunch = Bunch(self.graphics, lhc_pat, LHC_BEGIN,LHC_END,1,3,2)
                    self.sps_bunches.append(new_bunch)
                    new_bunch = Bunch(self.graphics, lhc_pat, LHC_BEGIN,LHC_END,1,3,3)
                    self.sps_bunches.append(new_bunch)
                    del_bunches.append(index)

            #print ("before bunches", len(self.bunches))                

            for index in sorted(del_bunches, reverse=True):
                del self.sps_bunches[index]
            
            #print ("after bunches", len(self.bunches))

            # if  global_i % 10 == 0:
            # #if global_i == 0:
            #     new_bunch = Bunch(self.graphics, pattern, SPS_BEGIN,SPS_END,1.2,3)
            #     self.sps_bunches.append(new_bunch)
                #print('NEW BUNCH', global_i % 10)

            # self.lin_pos += 1
            # if self.lin_pos >= LIN_END:
            #     self.lin_done = True
            #     self.lin_pos = 0

            if self.debug:
                print(self.sps_pos)        

    def updateLHC(self,lr):
        global global_i
        if self.lhc_done : 
            del_bunches = list()
            for index, bnch in enumerate(self.lhc_bunches):
                if bnch.isAlive():
                    #print('ALIVE')
                    bnch.draw(self.lhc_pos)    
                    bnch.travel()
                else:
                    self.lhc_done = True
                    del_bunches.append(index)

            for index in sorted(del_bunches, reverse=True):
                del self.lhc_bunches[index]
            
            if self.debug:
                print(self.lhc_pos)  

    def generate(self):
        global global_i
        self.graphics.fill(BLACK)
        # self.bot_done = True
        # self.duo_done = True
        self.updateBottle()
        self.updateDuoplasmatron()
        self.updateLINAC(lin_pat)
        self.updateSPS(sps_pat)
        self.updateLHC(0)
        self.updateLHC(1)
        global_i += 1
        
        

        # if self.state >= 30:
        #     self.state = 0
        #     self.bot_pos = 0
        #     self.duo_pos = DUO_BEGIN
        #     self.lin_pos = 0

        return self.graphics.getSurface()
