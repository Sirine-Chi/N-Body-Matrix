import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anima
from time import time


class Visualisator():
    def __init__(self):
        self.begin_time = time()
        print('- Visualiser initialised!')

    def render(self):
        pass

    def get_runtime(self) -> float:
        return time() - self.begin_time


class Animated2D(Visualisator):
    def __init__(self, particles: list, path_to_results):
        super().__init__()

    def visualise(self):
        pass


class Animated3D(Visualisator):
    pass


class Orbits2D(Visualisator):
    def __init__(self, particles: list, path_to_results):
        super().__init__()
        self.particles = particles
        self.path_to_results = path_to_results
    @staticmethod
    def render(system: list, inum='', delta_cur=0, path_to_results=''):
        plt.clf()
        # plt.figure(str(inum)+'_delta='+str(delta_cur)+'.png')
        plt.style.use('dark_background')
        plt.axes(xlim=(-7, 7), ylim=(-7, 7))
        plt.figure(figsize=(10, 10))
        plt.grid(True, color='w', alpha=0.125)
        plt.plot(0, 0, marker="o", c="y")

        for obj in system:
            plt.plot(obj.get_xy()[0], obj.get_xy()[1], alpha=0.4, marker=" ", c=obj.colour)
        plt.savefig(path_to_results + '/' + str(inum) + '_delta=' + str(delta_cur) + '.png', dpi=200)
        return plt


class Orbits3D(Visualisator):
    pass


class Realtime2D(Visualisator):
    pass


class Realtime3D(Visualisator):
    pass
