import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv


def plot_data(x_data, y_data):
    # Initialize plot
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    from itertools import count
    # scatter = ax.scatter([], [])
    ax.grid(True, color = 'w', alpha = 0.125)
    # plt.axes(xlim=(0, 1), ylim=(-5, 5)) 

    # Data storage
    # x_data = []
    # y_data = []

    # def catch_t_data(t_cur: float, data:float):
    #     x_data.append(t_cur)
    #     y_data.append(data)

    index = count()
    # Animation function
    def animate(i):
        # Simulate new data (replace with your data source)
        # x_data.append(next(index))
        # y_data.append(np.random.uniform(0, 1))

        # Update scatter plot data
        # scatter.set_offsets(np.c_[x_data, y_data])
        # plt.cla()
        plt.plot(x_data, y_data, color='cyan', alpha=0.5)

        # Adjust plot limits if necessary
        ax.relim()
        ax.autoscale_view()

        # return scatter,

    # Create animation
    ani = animation.FuncAnimation(plt.gcf(), animate, interval=10, blit=False)

    plt.tight_layout()
    plt.show()

with open('nbody/tmp/01:07:34.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)

    xs = []
    ys = []
    for row in data:
        xs.append(float(row[0]))
        ys.append(float(row[1]))

plot_data(xs, ys)
