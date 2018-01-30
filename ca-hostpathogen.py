# Simple CA simulator in Python
#
# *** Hosts & Pathogens ***
#
# Copyright 2008-2012 Hiroki Sayama
# sayama@binghamton.edu

import matplotlib
matplotlib.use('TkAgg')

import pylab as PL
import random as RD
import scipy as SP

RD.seed()

width = 50
height = 50
initProb = 0.05
infectionRate = 0.90
regrowthRate = 0.10

def init():
    global time, config, nextConfig, ratio_healthy, total_pop

    time = 0

    config = SP.zeros([height, width])
    for x in xrange(width):
        for y in xrange(height):
            if RD.random() < initProb:
                state = 2
            else:
                state = 1
            config[y, x] = state

    nextConfig = SP.zeros([height, width])
    ratio_healthy = []
    total_pop = []

def draw():
    PL.cla()
    PL.subplot(1,3,1)
    PL.pcolor(config, vmin = 0, vmax = 2, cmap = PL.cm.jet)
    PL.axis('image')
    PL.title('t = ' + str(time))

    ratio_healthy.append(sum([c == 1 for row in config for c in row])/sum([c == 2  for row in config for c in row]))
    PL.subplot(1,3,2)
    PL.plot(ratio_healthy)
    PL.title("Healthy / Infected")

    total_pop.append(width*height - sum([c == 0 for row in config for c in row]))
    PL.subplot(1,3,3)
    PL.plot(total_pop)
    PL.title('Total poulation')


def step():
    global time, config, nextConfig

    time += 1

    for x in xrange(width):
        for y in xrange(height):
            state = config[y, x]
            if state == 0:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 1:
                            if RD.random() < regrowthRate:
                                state = 1
            elif state == 1:
                for dx in xrange(-1, 2):
                    for dy in xrange(-1, 2):
                        if config[(y+dy)%height, (x+dx)%width] == 2:
                            if RD.random() < infectionRate:
                                state = 2
            else:
                state = 0

            nextConfig[y, x] = state

    config, nextConfig = nextConfig, config



import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])
