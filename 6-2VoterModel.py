import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd
import numpy as np

def initialize():
    global g
    g = nx.karate_club_graph()
    g.pos = nx.spring_layout(g)
    for i in g.nodes:
        g.nodes[i]['state'] = 1 if random() < .5 else 0


def observe():
    global g
    cla()
    nx.draw(g, vmin = 0, vmax = 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)

def update():
    global g
    listener = rd.choice(list(g.nodes))
    speaker = rd.choice(list(g.neighbors(listener)))
    g.nodes[listener]['state'] = g.nodes[speaker]['state']
    #check for homogeneity
    return sum([g.nodes[i]['state'] == 0 for i in g.nodes]) in [0, len(g.nodes)]

def update_reversed():
    global g
    speaker = rd.choice(list(g.nodes))
    listener = rd.choice(list(g.neighbors(speaker)))
    g.nodes[listener]['state'] = g.nodes[speaker]['state']
    #check for homogeneity
    return sum([g.nodes[i]['state'] == 0 for i in g.nodes]) in [0, len(g.nodes)]

def update_edge_based():
    global g
    edge = rd.choice(list(g.edges))
    listener_index = rd.choice([0,1])
    listener = edge[listener_index]
    speaker = edge[1 - listener_index]
    g.nodes[listener]['state'] = g.nodes[speaker]['state']
    #check for homogeneity
    return sum([g.nodes[i]['state'] == 0 for i in g.nodes]) in [0, len(g.nodes)]

#printing average number of steps to homogeneity:
counts = []
for _ in range(100):
    initialize()
    count = 0
    while not update():
        count += 1
    counts.append(count)
print np.mean(counts)

counts = []
for _ in range(100):
    initialize()
    count = 0
    while not update_reversed():
        count += 1
    counts.append(count)
print np.mean(counts)

counts = []
for _ in range(100):
    initialize()
    count = 0
    while not update_edge_based():
        count += 1
    counts.append(count)
print np.mean(counts)


"""
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])
"""
