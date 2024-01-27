import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anima
from particle import Particle
from time import monotonic
from n_body_lib import logger, v

class Visualisator:
    def __init__(self):
        self.begin_time = monotonic()
        logger.trace('-- Visualiser initialised!')

    def render(self):
        pass

    def get_runtime(self) -> float:
        return monotonic() - self.begin_time


class Animated2D(Visualisator):
    """
    Code draft:

    Make something like frame with X, Y

    Make shot with points on start positions
    On each next shot make previos positions ligther
    Link all the shots together and give as video
    """

    def __init__(self, particles: list, path_to_results: str):
        super().__init__()

    def visualise(self):
        pass


class Animated3D(Visualisator):
    pass


class Orbits2D(Visualisator):
    def __init__(self, particles: list[Particle], path_to_results: str):
        super().__init__()
        self.particles = particles
        self.path_to_results = path_to_results
    
    @staticmethod
    def render(system: list[Particle], inum='', delta_cur=0, path_to_results=''):
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


class DistributionVisualisator:
    import matplotlib.pyplot as plt
    from n_body_lib import *

    @staticmethod
    def dist_check(values: list):
        # print(f"1 {values}")

        plt.clf()
        plt.hist(values, bins=len(values)//10)
        plt.show()

    @staticmethod
    def make_xy(points: list) -> list:
        x_s0 = []
        y_s0 = []
        for i in points:
            x_s0.append(i[0])
            y_s0.append(i[1])
        return v([x_s0, y_s0])

    @staticmethod
    def dist_check_2d(list_of_vectors: list[np.ndarray]):
        print(f"Vectors: {list_of_vectors}")
        v_shaped = DistributionVisualisator.make_xy(list_of_vectors)

        plt.clf()
        plt.hist2d(
            v_shaped[0],
            v_shaped[1],
            bins=len(list_of_vectors)//10
            )
        plt.show()
