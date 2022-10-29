import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anima
import numpy as np
from random import uniform

def vis_1_23D(x_s, y_s, t_s):
    plt.style.use('dark_background')
    #plt.axes(xlim=(-10, 2), ylim=(-5, 5))
    plt.grid(True, color = 'w', alpha = 0.125)
    plt.plot(0, 0, marker="s", c="y")
    plt.plot(x_s, y_s, marker=" ", c="c")
    #plt.style.use('dark_background')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_s, y_s, t_s)
    ax.plot(0, 0, 0, marker=" ", c="y")
    ax.plot(0, 0, t_s[len(t_s)-1], marker=" ", c="y")

    ax.grid(False)
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.set_xlabel('X', c = 'w')
    ax.set_ylabel('Y', c = 'w')
    ax.set_zlabel('t', c = 'w')

    plt.show()
    #plt.savefig('F_2.png')
    return plt

def vis_N_2D(galaxy, inum, delta_v):
    plt.style.use('dark_background')
    #plt.axes(xlim=(-10, 2), ylim=(-5, 5))
    plt.grid(True, color = 'w', alpha = 0.125)
    plt.plot(0, 0, marker="s", c="y")

    de = 1
    # plt.plot(galaxy[3].makeXY()[0], galaxy[3].makeXY()[1], alpha = 0.4, marker=" ", c='b')
    for dot in galaxy:
        plt.plot(galaxy[dot.i].makeXY()[0], galaxy[dot.i].makeXY()[1], alpha = 0.4, marker=" ", c= dot.col)
    plt.savefig(str(inum)+'_'+str(delta_v) +'.png')
    #plt.show()
    return plt

def vis_N_3D(galaxy):
    de = 1
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #plt.plot(galaxy[3].makeXY()[0], galaxy[3].makeXY()[1], galaxy[3].t, alpha = 0.4, marker=" ", c='b')
    for dot in galaxy:
        ax.plot(galaxy[dot.i].makeXY()[0], galaxy[dot.i].makeXY()[1], galaxy[dot.i].t, alpha = 0.4, marker=" ", c='g')

    ax.grid(False)
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.set_xlabel('X', c = 'w')
    ax.set_ylabel('Y', c = 'w')
    ax.set_zlabel('t', c = 'w')

    plt.show()
    return plt

def vis_N_anim(galaxy, enn):
    plt.style.use('dark_background')

    fig = plt.figure()
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
    line, = ax.plot([], [], lw=2)

    def init():
        line.set_data([], [])
        return line

    n =[]
    for i in range (0, enn, 1):
        n.append(i)
    fig, ax = plt.subplots()

    # GalX = []
    # GalY = []
    # for s in galaxy:
    #     GalX.append((s.r[0])[0])
    #     GalY.append((s.r[0])[1])
    GalX = (galaxy[2])[1][0]
    GalY = (galaxy[2])[1][1]

    def animate(n):
        ax.clear()
        return ax.scatter(GalX[n], GalY[n])

    galanim = anima.FuncAnimation(fig, animate, frames=galaxy[0].t, interval = 100, repeat = False)
    return galanim
