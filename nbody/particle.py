from __future__ import annotations
# import n_body_lib as nbl
from n_body_lib import *

def force_obj_obj(obj1: Particle, obj2: Particle):
    """
    Force between first and second given objects on last position. Uses lambda f_ij
    obj1: Particle | Object, on which force is acting
    obj2: Particle | Object, from which force is acting
    return: np.ndarray | Force acting on obj1 from obj2
    """
    # return f_ij(obj1.positions[-1], obj2.positions[-1], obj1.mass, obj2.mass)
    return f_ij(obj1.positions[-1], obj2.positions[-1], obj1.mass, obj2.mass)


def force_obj_sys(obj: Particle, system: list[Particle]):
    """
    Sum of forces affected on given object in system on time step n. Uses lambda f_ij

    obj: Particle | Object, on which force is acting
    system: list[Particle] | Systems of objects, which forces are acting
    return: np.ndarray | Summary force
    """
    forces = []
    for other in system:
        if obj != other:
            forces.append(force_obj_obj(obj, other))
    return sum(forces)


# def potential_at_point(point: np.ndarray, force_obj_sys: callable, system: list[Particle]):
#     point = Particle("unit", 1.0, point, [0.0, 0.0], 'w', 0.0)
#     return np.gradient(force_obj_sys(point, system))


# def kinetic_energy(obj: Particle):
#     return obj.mass*(scal(obj.velocities[-1]))**2 / 2

# def potential_Energy(obj: Particle, system: list[Particle]):
#     pass
#     return sum(potential_at_point(Particle.get_last_position, force_obj_sys(Particle, system=system), system=system))

class Particle:
    """
    Has two subclasses, each real object from table can be initialised as one of them, or as both.
    """

    def __init__(self, name: str, mass: float, r0: list, v0: list, colour: str, start_angle: float, *args, **kwargs):
        """
        Particle class constructor
        """
        
        self.name: str = name
        self.colour: str = colour
        self.start_angle: float = start_angle
        self.mass: float = mass

        self.positions = []
        self.velocities = []
        self.forces = []
        self.times = []

        self.positions.append(rotvec(v(r0), self.start_angle))
        self.velocities.append(rotvec(v(v0), self.start_angle))
        self.times.append(0.0)

        logger.trace(self.__str__())

    def first_iteration(self, system: list[Particle]):
        pass

    # def print_object(self):
    #     logger.trace(f'New Obj: {self.name} \n mass: {self.mass} \n forces: {str(self.forces)}\n velocities: {str(self.velocities)} \n positions: {str(self.positions)} \n times: {str(self.times)}\n')

    def __str__(self) -> str:
        return f"Name: {self.name}, Mass: {self.mass}, Positions: {self.positions}, Colour: {self.colour}, Angle: {self.start_angle}"

    # def print_object_coor(self):
    #     logger.trace(f'Obj coordinates: {self.positions}\n')

    def offset(self, offset_object: Particle, n: int):
        """
        Rewrites position (on index n) to last position - position of given particle (on index n)
        \n
        offset_object: Particle | object, which moves positoins
        n: int | index of position in all positions
        """
        self.positions[n] = self.positions[n] - offset_object.positions[n]

    def get_xy(self) -> list[list]:
        """
        list, where each elememt is list with length = 2, contains coordinates of a particle in each point it's been
        \n
        returns: list | list of 2d points
        """
        x_s0 = []
        y_s0 = []
        for i in self.positions:
            x_s0.append(i[0])
            y_s0.append(i[1])
        return [x_s0, y_s0]

    def get_last_position(self) -> np.ndarray:
        """
        Returns last position of the particle
        \n
        self: Particle | some particle
        returns: np.ndarray | last position
        """
        return self.positions[-1]

    def get_positions(self) -> list[np.ndarray]:
        return self.positions

    def get_name(self) -> str:
        return self.name

    def get_function(self, function):
        pass
        return 


class DynamicParticle(Particle):
    # @classmethod

    def start_force(self, system: list[Particle]):
        """
        Calculates and appends forces on 0 step
        system: list[Particle] | our initialised particles
        """
        self.forces.append(force_obj_sys(self, system))

    # @classmethod
    def iteration(self, system: list[Particle], dt: float, velocity_depth=1):
        """
        calls f(), calculates new velocities and position using some numerical method
        system: list | Objects which trajectory deternined by others with force
        """
        def eiler_method(fs, vs, rs, m):
            vs.append(eiler(vs[-1], (fs[-1] / m), dt))
            rs.append(eiler(rs[-1], vs[-1], dt))

        def midpoint_method(fs, vs, rs, m):
            vs.append(v(vs[-1] + dt * f(rs[-1] + dt / 2 * f(rs[-1])) / m))  # Midpoint
            rs.append(v(rs[-1] + dt / 2 * (vs[-1] + vs[-2])))

        def adams_method(fs, vs, rs, m):
            vs.append(adams(vs[-1], (fs[-1] / m), (fs[-2] / m), dt))
            rs.append(adams(rs[-1], (vs[-1] / m), (vs[-2] / m), dt))
            # vs.append(v(vs[n - 1] + dt / 2 * (3 * fs[n] / m - fs[n - 1] / m)))
            # rs.append(v(rs[n - 1] + dt / 2 * (3 * vs[n] - vs[n - 1])))

        self.times.append(self.times[-1] + dt)
        self.forces.append(force_obj_sys(self, system))

        eiler_method(self.forces, self.velocities, self.positions, self.mass)

        # Cleaning velocities
        if len(self.velocities) == (velocity_depth+1):
            self.velocities.pop(0)
        # logger.debug(len(self.velocities))


class AnalyticParticle(Particle):
    """
    Object, on which others don't affect, which is going on it's own independent trajectory
    But others feel it's force
    """

    # @classmethod
    def iteration(self, tau: float, dt: float):
        self.times.append(self.times[-1] + dt)
        self.velocities.append(analytic_f(self.positions[0], self.velocities[0], (tau))[1])
        self.positions.append(analytic_f(self.positions[0], self.velocities[0], (tau))[0])
