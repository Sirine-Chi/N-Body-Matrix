import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anima


# fig, ax = plt.subplots(111, projection='3d')
# xdata, ydata, zdata = [], [], []
# ln, = plt.plot([], [], [])
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# line, = ax.plot([], [], [], lw=2) # example for line plot

# def init():
#     ax.set_xlim(-10, 10)
#     ax.set_ylim(-10, 10)
#     return ln,

# def update(points):
#     for p in points:
#         pos = p[0]
#         clr = p[1]
#         # xdata.append(pos[0])
#         # ydata.append(pos[1])
#         # zdata.append(pos[2])
#         line.set_data(pos[0], pos[1])
#         line.set(pos[2])
#         # ax.plot(pos[0], pos[1], pos[2], animated=True, marker=" ", c=clr)

# ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 100, 1000),
#                     init_func=init, blit=True, interval=10)

# plt.show()

# def vis3d():
#     plt.style.use('dark_background')

#     fig = plt.figure()
#     ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
#     line, = ax.plot([], [], lw=2)

#     def init():
#         line.set_data([], [])
#         return line

#     n =[]
#     for i in range (0, enn, 1):
#         n.append(i)
#     fig, ax = plt.subplots()

#     GalX = (galaxy[2])[1][0]
#     GalY = (galaxy[2])[1][1]

#     def animate(n):
#         ax.clear()
#         return ax.scatter(GalX[n], GalY[n])

#     galanim = anima.FuncAnimation(fig, animate, frames=galaxy[0].t, interval = 100, repeat = False)
#     return galanim

class Vis3d:
    def __init__(self):
        self.plt.style.use('dark_background')
        self.ax = plt.figure().add_subplot(projection='3d')
        self.points_all_t = []

        def update(points_t):
            self.points_all_t.append(points_t)

