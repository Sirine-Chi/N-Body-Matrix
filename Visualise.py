import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def vis_N_2D(galaxy):
    plt.style.use('dark_background')
    #plt.axes(xlim=(-10, 2), ylim=(-5, 5))
    plt.grid(True, color = 'w', alpha = 0.125)
    plt.plot(0, 0, marker="s", c="y")
    for dot in galaxy:
        plt.plot(galaxy[dot.i].makeXY()[0], galaxy[dot.i].makeXY()[1], alpha = 0.4, marker=" ", c='g')
    plt.show()
    return plt

def vis_N_3D(galaxy):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for dot in galaxy:
        ax.plot(galaxy[dot.i].makeXY()[0], galaxy[dot.i].makeXY()[1], galaxy[dot.i].t, alpha = 0.4, marker=" ", c='g')
    #ax.plot(0, 0, 0, marker=" ", c="y")

    ax.grid(False)
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.set_xlabel('X', c = 'w')
    ax.set_ylabel('Y', c = 'w')
    ax.set_zlabel('t', c = 'w')

    fig.show()
    return fig
