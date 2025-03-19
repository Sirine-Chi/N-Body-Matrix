from dataclasses import dataclass as component
from random import randrange
import esper
import mylinal as l
import mymath
# import inspect
# from loguru import logger

# logger.add(lambda msg: print(msg, end=""), level="TRACE")
# is_logs: bool = True
# if is_logs == True:
#     logger.add("dev/logs/trace_{time}.log", level="TRACE")

# --- --- --- --- --- COMPONENTS

@component
class Name:
    mame: str

@component
class Mass:
    # pass
    mass: float
    # def __init__(self, mass: float) -> None:
    #     self.mass = mass

@component
class Position:
    # pass
    positions: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    # def __init__(self, position: l.Array = l.Array.cartesian_array([0.0, 0.0, 0.0]) ) -> None:
    #     super().append(position)
    def __str__(self):
        return self.positions.__str__()


@component
class Velocity:
    # pass
    velocities: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    # def __init__(self, velocity: l.Array) -> None:
    #     super().append(velocity)

@component
class Acceleration:
    # pass
    accelerations: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])]

    # def __str__(self):
    #     return self.accelerations.__str__()
    # def __init__(self, acceleration: l.Array) -> None:
    #     super().append(acceleration)

@component
class Force:
    """ Just the current force vector """
    force: l.Array

    # def __str__(self):
    #     return self.force.__str__()

@component
class ForceMap:
    pass # TODO implement logic

@component
class UpdatesAnalytically:
    isupdatesanalytically: bool

@component
class Visualised:
    # pass
    # isvisualised: bool
    color: str

@component
class Monitoring:
    pass


class ForceHandler:

    @staticmethod
    def gravityforce_1(r1:l.Array, r2:l.Array, m1:Mass, m2:Mass) -> l.Array:
        """
        Calculate the gravitational force between two particles.

        Args:
            r1 (l.Array): Position vector of the first particle.
            r2 (l.Array): Position vector of the second particle.
            m1 (Mass): Mass of the first particle.
            m2 (Mass): Mass of the second particle.

        Returns:
            l.Array: Gravitational force vector acting on the first particle due to the second particle.
        """

        return mymath.G * m1 * m2 * (r1 - r2) / ((r1 - r2).l.scal())**3

    @staticmethod
    def gravity_force_ent(ent1: int, ent2: int) -> l.Array:
        m1 = esper.try_component(ent1, Mass).mass
        m2 = esper.try_component(ent2, Mass).mass
        r1 = esper.try_component(ent1, Position).positions[-1]
        r2 = esper.try_component(ent2, Position).positions[-1]

        return mymath.G * m1 * m2 * (r1 - r2) / (l.Array.scal(r1 - r2))**3

    @staticmethod
    def hooke_force(r1: l.Array, r2:l.Array):
        st_lenght = 1.0
        return mymath.K * ( (r1 - r2) / l.Array.scal(r1 - r2) - st_lenght)

    @staticmethod
    def hooke_force_ent(ent1: int, ent2: int) -> l.Array:
        r1 = esper.try_component(ent1, Position).positions[-1]
        r2 = esper.try_component(ent2, Position).positions[-1]
        st_lenght = 1.0
        return 0.0 * ( (r1 - r2) / l.Array.scal(r1 - r2) - st_lenght)

    # def gravityforce_2(self, p1, p2) -> l.Array:
    #     """
    #     Calculate the gravitational force between two particles.

    #     Args:
    #         r1 (l.Array): Position vector of the first particle.
    #         r2 (l.Array): Position vector of the second particle.
    #         m1 (Mass): Mass of the first particle.
    #         m2 (Mass): Mass of the second particle.

    #     Returns:
    #         l.Array: Gravitational force vector acting on the first particle due to the second particle.
    #     """
    #     r1, m1 = esper.get_components(p1, Position, Mass)
    #     r2, m2 = esper.get_components(p2, Position, Mass)

    #     return mymath.G * m1 * m2 * (r1 - r2) / ((r1 - r2).l.scal())**3

    # def coulombforce(self, p1, p2) -> l.Array:
    #     r1, q1 = esper.get_components(p1, Position, Charge)
    #     r2, q2 = esper.get_components(p2, Position, Charge)

    #     return mymath.K * q1 * q2 * (r1 - r2) / ((r1 - r2).l.scal())**3


# --- --- --- --- --- PROCESSORS

class ForceProcessor(esper.Processor):
    """

    Args:
        esper (_type_): _description_
    """
    all_funcs: dict[str, callable]  = {
            "1" : ForceHandler.gravity_force_ent,
            "2": ForceHandler.hooke_force_ent
            }

    def __init__(self, timestep: float = 1.0):
        self. timestep = timestep

    def process(self):
        # for ent2, (pos2, mass2) in esper.get_components(Position, Mass): # here we get entities, with ForceSelfOnOthers
        #     for ent1, (pos1, mass1) in esper.get_components(Position, Mass):
        #         if ent1 != ent2:
        #             force = ForceHandler().gravityforce_1(pos1[-1], pos2[-1], mass1, mass2)

        for ent, (frc) in esper.get_component(Force): # nullling force before each tick-cycle
            frc.force = 0.0*frc.force

        for force_id, force_f in self.all_funcs.items():
            for ent2, (f2) in esper.get_component(Force):
                for ent1, (f1) in esper.get_component(Force):
                    if ent1 != ent2:
                        if isinstance(ent1, int) and isinstance(force_id, str): # если тело2 действует на
                            if isinstance(ent2, int) and isinstance(force_id, str): # если действуют на тело 1
                                f1.force = f1.force + force_f(ent1, ent2)
                                # print(f"FFFFFFFFFFFFFFFF {f1.force}")
                                # esper.component_for_entity(ent1, Force) # = force(ent1, ent2)

        for ent, (frc, acc, m) in esper.get_components(Force, Acceleration, Mass):
            acc.accelerations.append(frc.force/m.mass)
        
        for ent, (acc, vel, pos) in esper.get_components(Acceleration, Velocity, Position):
            vel.velocities.append(vel.velocities[-1] + acc.accelerations[-1]*self.timestep)
            pos.positions.append(pos.positions[-1] + vel.velocities[-1]*self.timestep)


# class ForceCollectingProcessor(esper.Processor):
#     """

#     Args:
#         esper (_type_): _description_
#     """
#     def process(self, timestep: float):
#         for ent, (pos, mass) in esper.get_components(Position, Mass, ForceSelfOnOthers): # here we get entities, with ForceSelfOnOthers
#             for ent2, (pos2, mass2) in esper.get_components(Position, Mass, ForceOthersOnSelf):
                # pass
    

# class ForceApplicationProcessor(esper.Processor):
#     def process(self, timestep: float):
#         for ent, (acc, vel, pos) in esper.get_components(Acceleration, Velocity, Position):
#             vel.append(vel[-1] + acc*timestep)
#             pos.append(pos[-1] + vel*timestep)

class AnalyticCoordinateUpdateProcessor(esper.Processor):
    pass
 
class VisualProcessor(esper.Processor):
    def process(self):
        vis_positions = []
        for ent, (pos, vis) in esper.get_components(Position, Visualised):
            vis_positions.append([ent, pos.positions[-1]])
            print(pos.positions[-1])
        
        print(f"all positions: {vis_positions}")
            # call to visualiser

# --- --- --- --- --- ENT INITIALISATION

for i in range(1, 10):
    particle = esper.create_entity()

    # FIXME dimensional independent INIT'ion
    pp = l.Array.cartesian_array([randrange(1, 10), randrange(1, 10), randrange(1, 10)])
    pv = l.Array.cartesian_array([randrange(1, 10), randrange(1, 10), randrange(1, 10)])
    # pa = l.Array.cartesian_array([randrange(1, 10), randrange(1, 10), randrange(1, 10)])

    esper.add_component(particle, Name(f"Particle n. {particle}"))
    esper.add_component(particle, Mass(randrange(1, 10)))
    esper.add_component(particle, Position([pp]))
    esper.add_component(particle, Velocity([pv]))
    esper.add_component(particle, Force(pp * 0.0))
    # print("tttype", type(esper.try_component(particle, Force).force)) # why force is Mx, and v[-1] is Array?
    esper.add_component(particle, Acceleration([pp * 0.0]))
    esper.add_component(particle, Visualised)

                            # esper.component_for_entity(ent1, Force) # = force(ent1, ent2)
                            # print("force:" + force(ent1, ent2))
                            # print(f"Force: {esper.try_component(particle, Force)}")
    # esper.add_component(particle, Acceleration(esper.try_component(particle, Force) / esper.try_component(particle, Mass)))

    print(f"INIT:")
    print(*esper.try_components(particle, Name, Mass, Position, Force), sep="   ")

# --- --- --- --- --- FIRST FORCE COLLECTION

for force_id, force_f in ForceProcessor.all_funcs.items():
    # print(f"F ID: {force_id}")
    for ent2, (f2) in esper.get_component(Force):
        for ent1, (f1) in esper.get_component(Force):
            if ent1 != ent2:
                # store force_map in force or in ent? - In ent!
                if isinstance(ent1, int) and isinstance(force_id, str): # если тело2 действует на
                    if isinstance(ent2, int) and isinstance(force_id, str): # если действуют на тело 1
                        f1.force = f1.force + force_f(ent1, ent2) # force_f returns GOOD Value
                        # print(f"f1 {ent1}:: {f1.force}")

for ent, (frc, acc, m) in esper.get_components(Force, Acceleration, Mass):
    acc.accelerations.append(frc.force/m.mass)

# --- --- --- --- --- PROCESSORS INITIALISATION

t = 0
t_end = 1
step = 0.1

# forcecollectingprocessor = ForceCollectingProcessor()
# forceapplictionprocessor = ForceApplicationProcessor()
forceprocessor = ForceProcessor(timestep=step)
# analyticcoordinateupdateprocessor = AnalyticCoordinateUpdateProcessor()
visualprocessor = VisualProcessor()

# esper.add_processor(forcecollectingprocessor)
# esper.add_processor(forceapplictionprocessor)
esper.add_processor(forceprocessor, priority=10)
# esper.add_processor(analyticcoordinateupdateprocessor)
esper.add_processor(visualprocessor, priority=1)

# --- --- --- --- --- PROCESSING

while t < t_end:
    esper.process()
    # print(f"t={t}, {esper.try_component(1, Position)}")
    t += step
# print(esper.list_worlds())
