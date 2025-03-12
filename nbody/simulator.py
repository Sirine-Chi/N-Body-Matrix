from dataclasses import dataclass as component
import esper
import mylinal as l
import mymath

# --- --- --- --- --- COMPONENTS

@component
class Mass:
    mass: float
    def __init__(self, mass: float) -> None:
        self.mass = mass

@component
class Position:
    positions: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, position: l.Array.cartesian_array) -> None:
        self.positions.append(position)

@component
class Velocity:
    velocities: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, velocity: l.Array.cartesian_array) -> None:
        self.velocities.append(velocity)

@component
class Acceleration:
    accelerations: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, acceleration: l.Array.cartesian_array) -> None:
        self.accelerations.append(acceleration)

class Force:
    force: l.Array

@component
class ForceSelfOnOthers:
    isactingonothers: bool

@component
class ForceOthersOnSelf:
    isothersacting: bool

@component
class UpdatesAnalytically:
    isupdatesanalytically: bool

@component
class Visualised:
    isvisualised: bool
    color: str

@component
class Monitoring:
    pass

class Particle:
    pass


class ForceHandling:

    def gravityforce_1(self, p1: Particle, p2: Particle):
        """Gravity force

        Args:
            p1 (Particle): Force to
            p2 (Particle): Force form

        Returns:
            _type_: _description_
        """

        return mymath.G * p1.m * p2.m * (p1.r - p2.r).mymath.unitise()

# --- --- --- --- --- PROCESSORS

class ForceCollectingProcessor(esper.Processor):
    """

    Args:
        esper (_type_): _description_
    """
    def process(self, timestep: float):
        for ent, (pos, mass, fso) in esper.get_components(Position, Mass, ForceSelfOnOthers):
            pass

class ForceApplicationProcessor(esper.Processor):
    def process(self, timestep: float):
        for ent, (acc, vel, pos) in esper.get_components(Acceleration, Velocity, Position):
            vel.append(vel[-1] + acc*timestep)
            pos.append(pos[-1] + vel*timestep)

class AnalyticCoordinateUpdateProcessor(esper.Processor):
    pass
 
class VisualProcessor(esper.Processor):
    def process(self) -> None:
        for ent, (pos, vis) in esper.get_components(Position, Visualised):
            pass
            # call to visualiser

# --- --- --- --- --- ENT INITIALISATION

for i in range(1, 100):
    particle = esper.create_entity()


    esper.add_component(particle, Position)
    esper.add_component(particle, Velocity)

# --- --- --- --- --- PROCESSORS INITIALISATION

forcecollectingprocessor = ForceCollectingProcessor()
forceapplictionprocessor = ForceApplicationProcessor()
analyticcoordinateupdateprocessor = AnalyticCoordinateUpdateProcessor()
visualprocessor = VisualProcessor()

esper.add_processor(forcecollectingprocessor)
esper.add_processor(forceapplictionprocessor)
esper.add_processor(analyticcoordinateupdateprocessor)
esper.add_processor(visualprocessor)

# --- --- --- --- --- PROCESSING

# esper.process()
