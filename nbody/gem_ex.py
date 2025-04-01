import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
import time
import random
import threading
from collections import deque

class SimpleRealtime3DScatter:
    def __init__(self, interval=200):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.scatter = None
        self.points_queue = deque()
        self.current_points = np.array([]).reshape(0, 3)
        self.interval = interval

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Realtime 3D Scatter Plot')
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])

        self.ani = animation.FuncAnimation(
            self.fig, self._animate, frames=None,
            interval=self.interval, blit=True, repeat=False
        )
        plt.show()

    def update_points(self, new_points):
        """Updates the points queue with a new set of 3D points."""
        if new_points:
            points_array = np.array(new_points)
            if points_array.ndim == 2 and points_array.shape[1] == 3:
                self.points_queue.append(points_array)
                if hasattr(self, 'ani') and self.ani.event_source:
                    self.ani._drawn = False  # Force a redraw
                    self.ani.event_source.start()

    def _animate(self, i):
        """Animation function called by matplotlib."""
        if self.points_queue:
            self.current_points = self.points_queue.popleft()

        if self.current_points.size > 0:
            x, y, z = self.current_points[:, 0], self.current_points[:, 1], self.current_points[:, 2]
            if self.scatter:
                self.scatter._offsets3d = (x, y, z)
            else:
                self.scatter = self.ax.scatter(x, y, z)
        elif self.scatter:
            self.scatter.remove()
            self.scatter = None
        return self.scatter,

if __name__ == '__main__':
    visualizer = SimpleRealtime3DScatter(interval=500)

    def generate_random_points(num_points=10):
        return [(random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5))
                for _ in range(num_points)]

    def update_loop():
        time.sleep(1)
        visualizer.update_points(generate_random_points(15))
        time.sleep(0.5)
        visualizer.update_points([(0, 0, 0), (1, 1, 1), (-1, -1, -1)])
        time.sleep(1.5)
        visualizer.update_points([]) # Clear the points
        time.sleep(1)
        visualizer.update_points(generate_random_points(30))

    update_thread = threading.Thread(target=update_loop)
    update_thread.daemon = True
    update_thread.start()