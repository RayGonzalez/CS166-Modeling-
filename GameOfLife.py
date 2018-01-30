
import matplotlib
matplotlib.use('TkAgg')
from pylab import *

n = 100 # size of space: n x n
p = 0.1# probability of initially panicky individuals

def initialize():
    global config, nextconfig, density
    config = zeros([n, n])
    for x in xrange(n):
        for y in xrange(n):
            config[x, y] = 1 if random() < p else 0
    nextconfig = zeros([n, n])
    density = []

def observe():
    global config, nextconfig
    cla()
    subplot(1,2,1)
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary)
    density.append(sum(config)/len(config)**2)
    subplot(1,2,2)
    title("Density")
    plot(density)

def update():
    global config, nextconfig
    for x in xrange(n):
        for y in xrange(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n]
            if config[x, y] == 0:
                if count == 3: nextconfig[x, y] = 1
                else: nextconfig[x, y] = 0
            else:
                if count in [3, 4]: nextconfig[x, y] = 1
                else: nextconfig[x, y] = 0
    config, nextconfig = nextconfig, config



import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
