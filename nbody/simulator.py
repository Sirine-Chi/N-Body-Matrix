from dataclasses import dataclass as component
from random import randrange
import esper
import mylinal as l
import mymath
import vis
# import threading
# import inspect
from loguru import logger

logger.add(lambda msg: print(msg, end=""), level="TRACE")
is_logs: bool = True
if is_logs == True:
    logger.add("dev/logs/trace_{time}.log", level="TRACE")

# --- --- --- --- --- COMPONENTS

@component
class Name:
    mame: str

@component
class Mass:
    # pass
    mass: float

@component
class Position:
    # pass
    positions: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __str__(self):
        return self.positions.__str__()


@component
class Velocity:
    # pass
    velocities: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])]

@component
class Acceleration:
    # pass
    accelerations: list[l.Array] # = [l.Array.cartesian_array([0.0, 0.0, 0.0])])

@component
class Force:
    """ Just the current force vector """
    force: l.Array

@component
class ForceMap:
    pass
    # force_map: dict[str, tuple[bool]] = {"1": (1, 1), "2": (0, 0)}
    # TODO implement logic

@component
class UpdatesAnalytically:
    isupdatesanalytically: bool

@component
class Visualised:
    color: str

@component
class Monitoring:
    pass


class ForceHandler:

    @staticmethod
    def gravity_force_ent(ent1: int, ent2: int) -> l.Array:
        m1 = esper.try_component(ent1, Mass).mass
        m2 = esper.try_component(ent2, Mass).mass
        r1 = esper.try_component(ent1, Position).positions[-1]
        r2 = esper.try_component(ent2, Position).positions[-1]

        return mymath.G * m1 * m2 * (r1 - r2) / (l.Array.scal(r1 - r2))**3

    @staticmethod
    def hooke_force_ent(ent1: int, ent2: int) -> l.Array:
        r1 = esper.try_component(ent1, Position).positions[-1]
        r2 = esper.try_component(ent2, Position).positions[-1]
        st_lenght = 1.0
        return 0.0 * ( (r1 - r2) / l.Array.scal(r1 - r2) - st_lenght)

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

        for ent, (frc) in esper.get_component(Force): # nullling force before each tick-cycle
            frc.force = 0.0*frc.force

        for force_id, force_f in self.all_funcs.items():
            for ent2, (f2) in esper.get_component(Force):
                for ent1, (f1) in esper.get_component(Force):
                    if ent1 != ent2:
                        if isinstance(ent1, int) and isinstance(force_id, str): # если тело2 действует на
                            if isinstance(ent2, int) and isinstance(force_id, str): # если действуют на тело 1
                                f1.force = f1.force + force_f(ent1, ent2)

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
    def __init__(self):
        self.vinst = vis.viswind()

    def process(self):
        vis_positions = []
        for ent, (vis, pos) in esper.get_components(Visualised, Position):
            vis_positions.append(pos.positions[-1].give_tuple())
            # print(pos.positions[-1].len)
        # logger.trace(f"all positions: {vis_positions[1]}")
        # print(f"all positions: {vis_positions[1]}")

        self.vinst.window_tick(vis_positions)
            # call to visualiser, send all_positions to Vis module

# --- --- --- --- --- ENT INITIALISATION

for i in range(1, 100):
    particle = esper.create_entity()

    # FIXME dimensional independent INIT'ion
    pp = l.Array.cartesian_array([randrange(-10, 10), randrange(-10, 10), randrange(-10, 10)])
    pv = l.Array.cartesian_array([randrange(1, 10), randrange(1, 10), randrange(1, 10)])
    # pa = l.Array.cartesian_array([randrange(1, 10), randrange(1, 10), randrange(1, 10)])

    esper.add_component(particle, Name(f"Particle n. {particle}"))
    esper.add_component(particle, Mass(randrange(1, 10)))
    esper.add_component(particle, Position([pp]))
    esper.add_component(particle, Velocity([pv]))
    esper.add_component(particle, Force(pp * 0.0))
    # print("tttype", type(esper.try_component(particle, Force).force)) # why force is Mx, and v[-1] is Array?
    esper.add_component(particle, Acceleration([pp * 0.0]))
    esper.add_component(particle, Visualised(color="some"))

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
t_end = 100000000
step = 0.01

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

# class Loop(threading.Thread):
#     def __init__(self, id):
#         super().__init__()
#         self.id = id

#     def run(self, t, t_end, step):
#         while t < t_end:
#             esper.process()
#             # print(f"t={t}, {esper.try_component(1, Position)}")
#             t += step
#         print(f"Thread {self.id} finished!")

# loop_inst = Loop(1)
# loop_inst.start()

while t < t_end:
    esper.process()
    # print(f"t={t}, {esper.try_component(1, Position)}")
    t += step

# print(esper.list_worlds())
