import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import networkx as nx
import random as rd

def initialize():
    global g
    global n
    global p_e
    g = nx.erdos_renyi_graph(n, p_e)
    g.pos = nx.spring_layout(g)
    for i in g.nodes:
        g.nodes[i]['state'] = 1 if random() < .5 else 0

def observe():
    global g
    cla()
    nx.draw(g, vmin = 0, vmax = 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)

def async_update():
    global g
    a = rd.choice(list(g.nodes))
    if g.nodes[a]['state'] == 0: # if susceptible
        b = rd.choice(list(g.neighbors(a)))
        if g.nodes[b]['state'] == 1: # if neighbor b is infected
            g.nodes[a]['state'] = 1 if random() < p_i else 0
    else: # if infected
        g.nodes[a]['state'] = 0 if random() < p_r else 1


def sync_update():
    global g
    for node in list(g.nodes):
        if g.nodes[node]['state'] == 0: # if susceptible
            g.nodes[node]['next_state'] = 0
            for neighbor in list(g.neighbors(node)):
                if g.nodes[neighbor]['state'] == 1: # if neighbor  is infected
                    if random() < p_i:
                        g.nodes[node]['next_state'] = 1
                        #break
        else: g.nodes[node]['next_state'] = 0 if random() < p_r else 1
    #update all
    for node in list(g.nodes):
        g.nodes[node]['state'] = g.nodes[node]['next_state']

#Here the infection survives but doesn't take over
#n, p_e, p_i, p_r = (100, 0.1, 0.5, 0.5)

#Here the infection dies
#n, p_e, p_i, p_r = (100, 0.1, 0.04, 0.5)

#Here the infection survives but doesn't take over, mostly healthy individuas
#n, p_e, p_i, p_r = (200, 0.1, 0.04, 0.5)


n, p_e, p_i, p_r = (200, 0.05, 0.04, 0.5)


import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, sync_update])
