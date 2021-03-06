"""
complete LHC cycle, from H2 injection to LHC
Oliver Keller, CERN
"""
from matrix import matrix_width, matrix_height
from Tools.Graphics import *
import math
import random
import sys
import os
import serial
import liblo #for OSC messaging
import random
import numpy
from operator import sub
import time
import datetime

CW = 0
CCW = 1

# SPS to LHC TransFer lines, Left/Right
TFL = 0
TFR = 1

SHORT = 0
LONG = 1


BOT_BEGIN = 4
BOT_END   = 37
DUO_BEGIN = 38
DUO_END   = 68
LIN_BEGIN = 0
# #LIN_END   = 168+24+1
SPS_BEGIN = 13
#SPS_END   = 48
LHC_BEGIN = 4
# LHC_END   = 167



bot_pat = [(0,0,127),BLUE,(127,0,0),RED]
duo_pat = [BLACK,BLACK,(107,0,0),RED,(127,0,0)]
lin_pat = [(127,0,0),RED,(127,0,0)]
#sps_pat = [(100,100,100),WHITE,(100,100,100)]
sps_pat = [(30,30,0),(30,30,0),(30,30,0)]

lhc_pat = [(90,90,0),YELLOW,(90,90,0)]

lhc_pat_cw = [YELLOW,(30,30,0),(10,10,0)]
lhc_pat_ccw = [(10,10,0),(30,30,0),YELLOW]

LIN_SIZE = 168 + 24 + 1 + 1
lin_conf = [ LIN_SIZE, [0, [0,168]], [2, [0, 24]]  ]

SPS_SIZE = 48 - 10 + 1 + 4 + 2
sps_conf = [ SPS_SIZE, [4, [10, 48]], [3 ,[6,9]], [4 ,[53,54]], [4, [13,14]] ]

LHC_SIZE = 167 - 25 + 1 + 6 + 12
lhc_conf = [None]*2
lhc_conf[CW]  = [ LHC_SIZE, [3, [26, 167]], [3, [4, 9]], [4, [54, 65]], [3, [25, 26]]]
lhc_conf[CCW] = [ LHC_SIZE, [3, [157, 167]], [3, [4, 9]], [4, [54, 65]], [3, [25, 157]]]

ATLAS = 7 #- 5 + 167 - 27 + 2
ALICE = 28 # - 27 + 1
CMS = 90 #- 27 # + 1
LHCb = 151 #- 27 #+ 1

ATLASr = range(ATLAS-3,ATLAS+3)
ALICEr = range(ALICE-2,ALICE+3)
CMSr   = range(CMS-2,CMS+2)
LHCbr  = range(LHCb-2,LHCb+2)

tf_conf_left  = [ 20, [3, [6 , 25]] ] #was 21 6 26
tf_conf_right = [ 10,  [4, [67, 76]] ] #was 9 67 75

global_i = 0

g_atlas_col = 0
g_alice_col = 0
g_cms_col = 0
g_lhcb_col = 0
g_last_collision = 0

def repeat(times, func, *args, **kwargs):
    for _ in xrange(times):
        yield func(*args, **kwargs)

def parabola (x):
    return x*x

class Bunch():

    def __init__(self, graphics, config, pattern, acc, direction=0):
        self.graphics = graphics
        self.config = config
        self.pattern = pattern
        first_section = config[1]
        self.y = None #FIXME
        self.acc = acc
        self.cycles = 0
        self.mode = SHORT # lin, sps, lhc  
        self.section_base_x = config[1][1][0]
        self.max_x = config[0]
        self.dir=direction

        if self.dir == 0:
            # clockwise
            self.x = 0
        else:
            # counter clockwise
            self.x = self.max_x

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

    def cycles(self):    
        return self.cycles

    def travel(self, cur_x=0):
        global global_i

        #self.x = self.min_x + 1*(global_i%self.range) + (self.acc*(global_i%self.range)*(global_i%self.range))/2
        if self.acc > 1.0 and global_i % 2 == 0:
            self.x = (self.x*self.acc) + 0.35
        elif self.dir == 1:
            self.x -=1
        else:
            self.x +=1

        # if self.x <= 0:  
        #     self.x = 1
        
        #print(self.x)
        if self.x > self.max_x and self.dir == 0:
            self.x = cur_x / 3
            self.cycles += 1
        elif self.x < 0 and self.dir == 1:
            self.x = self.max_x - (cur_x / 3)
            self.cycles += 1

    def draw(self):
        global global_i
        #for color in self.pattern:
        #color = self.pattern[(int(-global_i)%len(self.pattern))]
        #self.graphics.drawPixel(offset-(sign*self.x), self.y, color)
        x = int(round(self.x))
        min_x = self.config[1][1][0]
        max_x = self.config[1][1][1]
        range_x = max_x - min_x
        self.section_base_x = 0
        for index,section in enumerate(self.config[1:]):
            #print("section", index)
            min_x = section[1][0]
            max_x = section[1][1]
            range_x = (max_x - min_x) + 1
            #print(min_x,max_x,self.section_base_x,range_x)
            #print(self.x,self.section_base_x,  self.section_base_x+range_x)
            self.y = section[0]
            if x in range(self.section_base_x, self.section_base_x+range_x):
                #print("in range")
                # if self.x in LHCbr:
                #     self.graphics.drawPixel(x-self.section_base_x+min_x, self.y, GREEN)
                # else:    
                self.graphics.drawPixel(x-self.section_base_x+min_x, self.y, self.pattern[1])
                #print(x,y)
                if self.mode == LONG:# and (self.x+1) > self.mode:
                    if self.x - 1 > self.section_base_x - min_x:
                        self.graphics.drawPixel(x-self.section_base_x+min_x-1,self.y, self.pattern[2])
                    if self.x + 1 < self.section_base_x + range_x:
                        self.graphics.drawPixel(x-self.section_base_x+min_x+1,self.y, self.pattern[0])
            self.section_base_x += range_x



class LHC(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.serialPort = None
        self.reset()

    def reset(self):
        self.bot_pos = BOT_BEGIN
        self.duo_pos = DUO_BEGIN
        self.lin_pos = LIN_BEGIN
        self.sps_pos = SPS_BEGIN
        self.lhc_pos = LHC_BEGIN
        
        #count number of produced bunches
        self.sps_bcnt = 0
        self.lhc_bcnt = 0
        
        self.bot_done = False
        self.duo_done = False
        self.lin_done = False
        self.sps_done = False
        self.lhc_done = False

        self.tfl_done = False
        self.tfr_done = False

        self.debug = False
        self.graphics.fill(BLACK)
        #self.sqrtable = list(repeat(100,parabola, 1, 100))
        #self.sqrtable = list([x*x/2 for x in xrange (170)])
        self.lin_bunches = list()
        self.sps_bunches = list()
        self.tfl_bunches = list()
        self.tfr_bunches = list()
        self.lhc_bunches = [[] for k in range(2)]
        self.collisions = list()
        self.alice_colcnt = 0


        self.restart = True
        if self.serialPort:
            self.serialPort.flushInput()
        self.osc_atlas = liblo.Address("mc-im-pc5",7777)
        self.osc_alice = liblo.Address("mc-im-pc6",7777)
        self.osc_cms = liblo.Address("mc-im-pc7",7777)
        self.osc_lhcb = liblo.Address("mc-im-pc8",7777)
        

    def checkCollision(self, b1x, b1y, other_dir):
        global g_atlas_col
        global g_alice_col
        global g_cms_col
        global g_lhcb_col
        global g_last_collision

        collision = False
        #if global_i > g_last_collision + 250:
        timePassed = True  
        #else:
        #    timePassed = False  
        for b2 in self.lhc_bunches[other_dir]:
                if b1x in range(b2.x-1,b2.x+1) and b1y == b2.y:
                    if b1x in ATLASr and g_atlas_col < 10000 and timePassed:
                        g_atlas_col +=1 
                        g_last_collision = global_i
                        self.collisions.append([ATLAS, b1y, 30])
                        try:
                            liblo.send(self.osc_atlas, "/collision", ('i',1))
                        except:
                            print("could not send ATALS trigger")
                        return True
                    if b1x in ALICEr and g_alice_col < 10000 and timePassed:
                        self.alice_colcnt +=1
                        # every third time only
                        if self.alice_colcnt % 4 == 0:
                            g_alice_col +=1
                            g_last_collision = global_i
                            self.collisions.append([ALICE, b1y, 30])
                            try:
                                liblo.send(self.osc_alice, "/collision", ('i',1))
                            except:
                                print("could not send ALICE trigger")
                            return True
                    if b1x in CMSr and g_cms_col < 100000 and timePassed: 
                        g_cms_col +=1
                        g_last_collision = global_i
                        self.collisions.append([CMS, b1y, 30])
                        try:
                            liblo.send(self.osc_cms, "/collision", ('i',1))
                        except:
                            print("could not send CMS trigger")
                        return True
                    if b1x in LHCbr and g_lhcb_col < 100000 and timePassed:
                        g_lhcb_col +=1
                        g_last_collision = global_i
                        self.collisions.append([LHCb, b1y, 30])
                        try:
                            liblo.send(self.osc_lhcb, "/collision", ('i',1))
                        except:
                            print("could not send LHCb trigger")
                        return True
        return collision

    def updateCollisions(self):
        global g_last_collision
        global global_i

        #col_pat=[[255,255,255], [50,50,50], [0,0,0], [255,255,255], [50,50,50],[255,0,0],[0,255,0],[0,0,255],[0,255,255]]
        col_pat=[WHITE, (50,50,50), (0,0,0), (255,255,255), (50,50,50),(255,0,0),(0,255,0),(0,0,255),(0,255,255)]

        # for testing
        # self.collisions.append([ATLAS, 3, 100])
        # g_last_collision = 1

        if g_last_collision > 0:
            del_collisions = list()

            for index,collision in enumerate(self.collisions):
                # if global_i%3 == 0:
                #     color = WHITE
                # elif global_i%3 == 1: 
                #     color = (50,50,50)
                # elif global_i%3 == 2: 
                #     color = BLACK

                color = col_pat[global_i%len(col_pat)]

                # border = map(sub,color,(200,200,200))
                # for i,col in enumerate(border):
                #     if col < 0:
                #         col = 1
                #         border[i]=col
                # border = tuple(border)

                self.graphics.drawPixel(collision[0]-1,collision[1],color)
                self.graphics.drawPixel(collision[0],collision[1],color)
                self.graphics.drawPixel(collision[0]+1,collision[1],color)

                # decrement life time counter
                collision[2] -= 1
            
                if collision[2] < 0:
                    del_collisions.append(index)

            # cleanup
            for index in sorted(del_collisions, reverse=True):
                del self.collisions[index]    

    
    def animateSrtripe(self,pattern, x, min_x, max_x, acc, y):
        global global_i
        
        for pixel in range(min_x,max_x):
            # pixel = math.floor(pixel * acc)
            # pixel = int(pixel)
            # pixel = min(pixel, max_x)
            if x < max_x and x < pixel:
                color = BLACK
            else:
                color = pattern[(pixel-(global_i/5))%len(pattern)]
            self.graphics.drawPixel(pixel, y, color)

    def updateBottle(self):
        self.animateSrtripe(bot_pat, self.bot_pos, BOT_BEGIN, BOT_END,0.5,1) 
        self.bot_pos += 3
        if self.bot_pos >= BOT_END:
            self.bot_done = True
        if self.debug:
            print(self.bot_pos)

    def updateDuoplasmatron(self):
        if self.bot_done : 
            self.animateSrtripe(duo_pat, self.duo_pos,DUO_BEGIN,DUO_END,1,1) 
            self.duo_pos += 1
            if self.duo_pos >= DUO_END:
                self.duo_done = True
            if self.debug:
                print(self.duo_pos)

    def updateLINAC(self, config, pattern):
        global global_i
        if self.duo_done :
            del_bunches = list()
            for index, bnch in enumerate(self.lin_bunches):
                if bnch.cycles == 0:
                    #print('ALIVE')
                    if bnch.x > 168:
                        bnch.mode = LONG
                    else:
                        bnch.mode = SHORT
                    bnch.draw()    
                    bnch.travel()
                else:
                    #print("creating SPS bunches")
                    self.lin_done = True
                    new_bunch = Bunch(self.graphics, sps_conf, sps_pat,1.0)
                    self.sps_bunches.append(new_bunch)
                    # new_bunch = Bunch(self.graphics, sps_conf, sps_pat,1,1)
                    # self.sps_bunches.append(new_bunch)
                    del_bunches.append(index)

            #print ("before bunches", len(self.bunches))                

            for index in sorted(del_bunches, reverse=True):
                del self.lin_bunches[index]
            
            #print ("after bunches", len(self.bunches))

            if  global_i % 8 == 0: #accelerate protons in linac 
            #if global_i == 0:
                new_bunch = Bunch(self.graphics, config, pattern,1.05)
                self.lin_bunches.append(new_bunch)
                #print('NEW BUNCH', global_i % 10)

            # self.lin_pos += 1
            # if self.lin_pos >= LIN_END:
            #     self.lin_done = True
            #     self.lin_pos = 0

            if self.debug:
                print(self.lin_pos)
    
    def updateSPS(self, config, pattern):
        global global_i
        if self.lin_done : 
            del_bunches = list()
            for index, bnch in enumerate(self.sps_bunches):
                if bnch.cycles == 0:
                    #print('ALIVE')
                    if bnch.x > 4:
                        bnch.mode = LONG
                    else:
                        bnch.mode = SHORT
                    bnch.draw()
                    bnch.travel()            
                    #print(bnch.x)         
                    if self.sps_bcnt >= 3*4 and self.sps_bcnt < 3*11:
                        if  global_i % 3 == 0:
                            if bnch.x == 20:
                                self.sps_done = True
                                #print("TF right")
                                new_bunch = Bunch(self.graphics, tf_conf_right, lhc_pat_cw,1.0)
                                self.tfr_bunches.append(new_bunch)
                            elif bnch.x == 38:
                                #print("TF left")
                                self.sps_done = True #duplicate
                                new_bunch = Bunch(self.graphics, tf_conf_left, lhc_pat_cw,1.0)
                                self.tfl_bunches.append(new_bunch)   
                else:
                    del_bunches.append(index)
                    self.sps_bcnt += 1
                    #print("inc",self.sps_cycle)

            #print ("before bunches", len(self.bunches))                

            for index in sorted(del_bunches, reverse=True):
                del self.sps_bunches[index]

            if self.debug:
                print(self.sps_pos)        

    def updateTF(self, config, pattern, line):
        global global_i
        if self.sps_done : 
            del_bunches = list()
            if line == TFL:
                bunches = self.tfl_bunches
            else:
                bunches = self.tfr_bunches
            for index, bnch in enumerate(bunches):
                if bnch.cycles == 0:
                    #print('ALIVE')
                    bnch.mode = LONG
                    bnch.draw()
                    bnch.travel()                        
                else:
                    if line == TFL:
                        #print("tfl done")
                        self.tfl_done = True
                        new_bunch = Bunch(self.graphics, lhc_conf[CW], lhc_pat_cw,1.0,CW)
                        self.lhc_bunches[CW].append(new_bunch)
                    else:
                        self.tfr_done = True
                        new_bunch = Bunch(self.graphics, lhc_conf[CCW], lhc_pat_ccw,1.0,CCW)
                        self.lhc_bunches[CCW].append(new_bunch)
                    del_bunches.append(index)

            for index in sorted(del_bunches, reverse=True):
                del bunches[index]

    def updateLHC(self, config, pattern, direction):
        global global_i
        if (self.tfl_done == True and direction == CW) or (self.tfr_done == True and direction == CCW) : 
            del_bunches = list()
            for index, bnch in enumerate(self.lhc_bunches[direction]):
                if bnch.cycles == 0:
                    #print('ALIVE')
                    bnch.mode = LONG
                    if self.lhc_pos > 1 * 2 * LHC_SIZE and \
                        ((direction == CW and self.checkCollision(bnch.x, bnch.y, CCW)) or \
                        (direction == CCW and self.checkCollision(bnch.x, bnch.y, CW)) ) :
                        if self.debug:
                            print("collide", bnch.x, bnch.y)
                        #bnch.cycles += 1
                        # no deletion of bunches as only very few partciles collide per turn
                        #del_bunches.append(index)
                        #del_bunches.append(index-1)
                    else:
                        bnch.draw()    
                    bnch.travel()
                else:
                    new_bunch = Bunch(self.graphics, lhc_conf[direction], pattern,1.0,direction)
                    self.lhc_bunches[direction].append(new_bunch)
                    del_bunches.append(index)
                    

            for index in sorted(del_bunches, reverse=True):
                del self.lhc_bunches[direction][index]
            
            #print(self.lhc_pos)  
            if self.lhc_pos > 10 * 2 * (LHC_SIZE) :
                #sys.exit(2)
                #return 0
                self.lhc_done = True
            else:
                self.lhc_pos += 1
        return 1
            

    def generate(self):
        global global_i
        global g_atlas_col
        global g_alice_col
        global g_cms_col
        global g_lhcb_col
        global g_last_collision

        if self.restart:
            global_i = 0
            g_atlas_col = 0
            g_alice_col = 0
            g_cms_col = 0
            g_lhcb_col = 0
            g_last_collision = 0
            self.reset()
            while self.serialPort == None:
                try:
                    print('-> trying to open serial port')
                    self.serialPort = serial.Serial('/dev/cu.usbmodem1411',115200,timeout=None)
                except:
                    #print('serial port not valid')
                    self.serialPort = None
                    time.sleep(1)
            print("-> Ready, touch the bottle...")
            self.serialPort.flushInput()
            self.serialPort.read(1)
            self.serialPort.close()
            self.serialPort = None
            #print("Press any key to continue...")
            #os.system('read -s -n 1')
            self.restart = False
            print('{:%Y-%b-%d %H:%M:%S} -> starting LED strip animation'.format(datetime.datetime.now()))
        self.graphics.fill(BLACK)
        # self.bot_done = True
        # self.duo_done = True
        self.updateBottle()
        self.updateDuoplasmatron()
        self.updateLINAC(lin_conf, lin_pat)
        self.updateSPS(sps_conf, sps_pat)
        self.updateTF(lhc_conf, lhc_pat_cw, TFL)
        self.updateTF(lhc_conf, lhc_pat_cw, TFR)
        self.updateLHC(lhc_conf, lhc_pat_cw, CW)
        self.updateLHC(lhc_conf, lhc_pat_ccw, CCW)
        self.updateCollisions()
        if self.lhc_done:
            # reset
            print('-> LED strip animation ended')
            self.graphics.fill(BLACK)
            self.restart = True
        global_i += 1
        return self.graphics.getSurface()
