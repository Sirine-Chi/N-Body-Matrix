from dataclasses import dataclass as component
from random import uniform
import esper
import mylinal as l
import mymath
import markup_manager as mm
from mydatatypes import print_dict, color4f
import vis
# from loguru import logger

# TODO implement tubelist
# TODO isolate data

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
    color: color4f

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

        return mymath.G * m1 * m2 * (r2 - r1) / (l.Array.scal(r1 - r2))**3

    @staticmethod
    def hooke_force_ent(ent1: int, ent2: int) -> l.Array:
        r1 = esper.try_component(ent1, Position).positions[-1]
        r2 = esper.try_component(ent2, Position).positions[-1]
        st_lenght = 1.0
        return 0.0 * ( (r1 - r2) / l.Array.scal(r1 - r2) - st_lenght)

# --- --- --- --- --- PROCESSORS

class ForceProcessor(esper.Processor):

    def __init__(self, all_funcs: dict[str, callable], timestep: float = 1.0):
        self.timestep = timestep
        self.all_funcs = all_funcs

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

        # --- --- FORCE APPLICATION

        for ent, (frc, acc, m) in esper.get_components(Force, Acceleration, Mass):
            acc.accelerations.append(frc.force/m.mass)

        for ent, (acc, vel, pos) in esper.get_components(Acceleration, Velocity, Position):
            vel.velocities.append(vel.velocities[-1] + self.timestep*acc.accelerations[-1])
            pos.positions.append(pos.positions[-1] + self.timestep*vel.velocities[-1])

class AnalyticCoordinateUpdateProcessor(esper.Processor):
    pass

class VisualProcessor(esper.Processor):
    def __init__(self):
        self.vinst = vis.viswind()

    def process(self):
        vis_positions = []
        # vis_colors = []
        for ent, (vis, pos) in esper.get_components(Visualised, Position):
            vis_positions.append( [pos.positions[-1].give_tuple(), vis.color] )
            # vis_colors.append( vis.color )
            # print(pos.positions[-1].len)
        # logger.trace(f"all positions: {vis_positions[1]}")
        # print(f"all positions: {vis_positions[1]}")

        self.vinst.window_tick(vis_positions)
            # call to visualiser, send all_positions to Vis module

# --- --- --- --- --- CONSTANTS

funcs: dict[str, callable] = {
        "1" : ForceHandler.gravity_force_ent,
        "2": ForceHandler.hooke_force_ent
        }
n = 4
t = 0
t_end = 10
step = 5e-5

# --- --- --- --- --- ENT CREATION

def init_ent(name: str, color: color4f, mass: float, pos: l.Array, vel: l.Array):
    id: int = esper.create_entity()

    esper.add_component(id, Name(name))
    esper.add_component(id, Mass(mass))
    esper.add_component(id, Position([pos]))
    esper.add_component(id, Velocity([vel]))

    esper.add_component(id, Force(pos * 0.0))
    esper.add_component(id, Acceleration([pos * 0.0]))
    esper.add_component(id, Visualised(color.get_tuple))

    return id

def get_bodies(path) -> list[dict]:
    result = mm.get_toml(path)["Bodies"]

    objects = []
    for key, obj in result.items():
        obj["Name"] = key
        objects.append(obj)

    return objects

path = 'nbody/system.toml'
objects = get_bodies(path)

# for o in objects:
#     print_dict(o)

# objects = [
#     {
#         "Name": "Sun",
#         "Mass": 332840,
#         "R (polar)": [0.0, 0.0, 0.0],
#         "V (polar)": [0.0, 0.0, 0.0],
#         "Color": [1.0, 1.0, 0.0],
#         "force_1 (to, from)": [1, 1],
#         "force_2 (to, from)": [0, 0],
#         "force_3 (to, from)": [0, 0],
#         "force_4 (to, from)": [0, 0]
#     },
#     {
#         "Name" : "Earth",
#         "Mass" : 1,
#         "R (polar)" : [1.496e+11, 0.0, 0.0],
#         "V (polar)" : [0.0, 2.978e+4, 0.0],
#         "Color" : [0.0, 0.0, 1.0],
#         "force_1 (to, from)" : [1, 1],
#         "force_2 (to, from)" : [0, 0],
#         "force_3 (to, from)" : [0, 0],
#         "force_4 (to, from)" : [0, 0]
#     }
# ]

# objects = []
# for i in range(1, n+1):

#     # FIXME dimensional independent INIT'ion
#     pl = [uniform(-5, 5), uniform(-5, 5), uniform(-5, 5)]
#     vl = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]
#     pp = l.Array.cartesian_array(pl)
#     pv = 0.1 * l.Array.cartesian_array(vl)

#     o = {
#         "Name": f"Particle n. {i}",
#         "Color": [uniform(0, 1), uniform(0, 1), uniform(0, 1)],
#         "Mass": uniform(1, 100),
#         "R (polar)" : pl,
#         "V (polar)" : vl,
#         "force_1 (to, from)" : "1, 1"
#         }
#     objects.append(o)

# --- --- --- --- --- ENT INITIALISATION

for o in objects:
    p = init_ent(o["Name"], color4f(o["Color"][0], o["Color"][1], o["Color"][2]), o["Mass"], l.Array.cartesian_array(o["R (polar)"]), l.Array.cartesian_array(o["V (polar)"]))

    print(f"INIT:")
    print(*esper.try_components(p, Name, Mass, Position, Velocity, Force, Visualised), sep="   ")

# --- --- --- --- --- FIRST FORCE COLLECTION

for force_id, force_f in funcs.items():
    # print(f"F ID: {force_id}")
    for ent2, (f2) in esper.get_component(Force):
        for ent1, (f1) in esper.get_component(Force):
            if ent1 != ent2:
                if isinstance(ent1, int) and isinstance(force_id, str): # если тело2 действует на
                    if isinstance(ent2, int) and isinstance(force_id, str): # если действуют на тело 1
                        f1.force = f1.force + force_f(ent1, ent2) # force_f returns GOOD Value

for ent, (frc, acc, m) in esper.get_components(Force, Acceleration, Mass):
    acc.accelerations.append(frc.force/m.mass)

# --- --- --- --- --- PROCESSORS INITIALISATION

forceprocessor = ForceProcessor(all_funcs=funcs, timestep=step)
# analyticcoordinateupdateprocessor = AnalyticCoordinateUpdateProcessor()
visualprocessor = VisualProcessor()

esper.add_processor(forceprocessor, priority=10)
# esper.add_processor(analyticcoordinateupdateprocessor)
esper.add_processor(visualprocessor, priority=1)

# --- --- --- --- --- PROCESSING

while t < t_end:
    esper.process()
    t += step

# print(esper.list_worlds())
