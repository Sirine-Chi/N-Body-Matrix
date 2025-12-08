# that was a prototype for gemini

from dataclasses import dataclass as component
import esper
from random import uniform
import mylinal as l

# --- --- --- --- --- COMPONENTS

@component
class Name:
    mame: str

@component
class Mass:
    mass: float

@component
class Position:
    positions: list[l.Array]

@component
class Velocity:
    velocities: list[l.Array]

@component
class Acceleration:
    accelerations: list[l.Array]

@component
class Visualised:
    color: str

# --- --- ---  --- --- PROCESSORS

class MovementProcessor(esper.Processor):

    def __init__(self, timestep: float):
        self. timestep = timestep
    
    def process(self):
        for ent, (acc, vel, pos) in esper.get_components(Acceleration, Velocity, Position):
                vel.velocities.append(vel.velocities[-1] + acc.accelerations[-1]*self.timestep)
                pos.positions.append(pos.positions[-1] + vel.velocities[-1]*self.timestep)

class VisualProcessor(esper.Processor):
    def process(self):
        vis_positions = []
        for ent, (vis, pos) in esper.get_components(Visualised, Position):
            vis_positions.append(pos.positions[-1].give_tuple())
        print(vis_positions)

# --- --- --- --- --- CONSTANTS

n = 100
t = 0
t_end = 100000000
step = 0.01

# --- --- --- --- --- ENTITIES INITIALISATION

for i in range(1, n+1):
    particle = esper.create_entity()

    pp = l.Array.cartesian_array([uniform(-5, 5), uniform(-5, 5), uniform(-5, 5)])
    pv = l.Array.cartesian_array([uniform(0, 2), uniform(0, 2), uniform(0, 2)])

    esper.add_component(particle, Name(f"Particle n. {particle}"))
    esper.add_component(particle, Mass(uniform(1, 100)))
    esper.add_component(particle, Position([pp]))
    esper.add_component(particle, Velocity([pv]))
    esper.add_component(particle, Acceleration([pp * 0.0]))
    esper.add_component(particle, Visualised(color="some"))

# --- --- --- --- --- PROCESSORS INITIALISATION

movementprocessor = MovementProcessor(timestep=step)
visualprocessor = VisualProcessor()

esper.add_processor(movementprocessor, priority=10)
esper.add_processor(visualprocessor, priority=1)

# --- --- --- --- --- PROCESSING

while t < t_end:
    esper.process()
    t += step
