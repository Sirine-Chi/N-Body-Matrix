from visualiser import Orbits2D
from n_body_lib import *
from particle import DynamicParticle


class Simulator:
    def __init__(self, particlesp: list, end_timep: float, stepp: float):
        self.begin_runtime: float = monotonic()
        self.particles: list = particlesp
        self.end_time: float = end_timep
        self.step: float = stepp

        logger.trace('-- Simulator initialized!')

    def start_forces(self):
        pass

    def simulation(self):
        pass

    def get_positions(self) -> list[list]:
        pass

    def get_runtime(self) -> float:
        return monotonic() - self.begin_runtime


class SimulatorCPU(Simulator):
    def __init__(self, particles_fp: list, end_timep: float, stepp: float):
        super().__init__(particles_fp, end_timep, stepp)
        self.particles = self.initialize_particles(particles_fp)
        self.start_forces()

        self.tau: float = 0

    @staticmethod
    def initialize_particles(table_f: list) -> list:  # WITHOUT deltas!!!!
        particles = []
        for e in table_f:
            particles.append(DynamicParticle(
                e['name'],
                e['mass'],
                e['start_position'],
                e['start_velocity'],
                e['color'],
                e['start_angle']
            ))
        return particles

    def start_forces(self):
        # map(Particle.first_iteration(pcl, self.particles), self.particles)
        for pcl in self.particles:
            DynamicParticle.start_force(pcl, self.particles)

    def simulation(self):
        while self.tau < self.end_time:
            for element in self.particles:
                element.iteration(self.particles, self.step)
            self.sys_offset()
            self.tau += self.step
            yield

    def sys_offset(self):
        for pcl in self.particles:
            pcl.offset(self.particles[0], n=-1)

    def get_positions(self) -> list[list]:
        poses = []
        for element in self.particles:
            poses.append(element.positions)
        return poses

    def get_last_positions(self) -> list[np.ndarray]:
        last_poses = []
        for elemnt in self.particles:
            last_poses.append(elemnt.get_last_position())
        return last_poses

    def vis(self, path_to_png: str):
        Orbits2D.render(self.particles, 's', 0, path_to_png)


class SimulatorGPU(Simulator):
    # mx - matrix, mxs - matrices
    def __init__(self, particles_fp: list, end_timep: float, stepp: float):
        super().__init__(particles_fp, end_timep, stepp)

        self.mass_vector = SimulatorGPU.smth_vector(particles_fp, 'mass')
        self.positions_vectors = []
        self.velocity_vectors = []
        self.acceleration_vectors = []
        self.positions_vectors.append(SimulatorGPU.smth_vector(particles_fp, 'start_position'))
        self.velocity_vectors.append(SimulatorGPU.smth_vector(particles_fp, 'start_velocity'))
        self.tau: float = 0.0

    @staticmethod
    def smth_vector(particles: list, key: str) -> np.ndarray:
        smts = []
        for pcl in particles:
            smts.append(pcl[key])
        return v(smts)

    # @staticmethod
    # def format_matrices(particles_f) -> dict:
    #     return {
    #         'mass vector': Simulator_GPU.smth_vector(particles_f, 'mass'),
    #         'coordinates vector': Simulator_GPU.smth_vector(particles_f, 'start_position'),
    #         'velocity vector': Simulator_GPU.smth_vector(particles_f, 'start_velocity')
    #     }

    def start_forces(self):
        pass

    def simulation(self):
        while tau < self.end_time:
            pass

    def get_positions(self) -> list:
        pass
