# from dataclasses import dataclass as component
import esper
import mylinal as l
import mymath
from loguru import logger

logger.add(lambda msg: print(msg, end=""), level="TRACE") # FIXME move to main / entry point
is_logs: bool = True
if is_logs == True:
    logger.add("dev/logs/trace_{time}.log", level="TRACE")

# --- --- --- --- --- COMPONENTS

# @component
class Mass(float):
    pass
    # mass: float
    # def __init__(self, mass: float) -> None:
    #     self.mass = mass

# @component
class Position:
    positions: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, position: l.Array.cartesian_array) -> None:
        self.positions.append(position)

# @component
class Velocity:
    velocities: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, velocity: l.Array.cartesian_array) -> None:
        self.velocities.append(velocity)

# @component
class Acceleration:
    accelerations: list[l.Array] = [l.Array.cartesian_array([0.0, 0.0, 0.0])]
    def __init__(self, acceleration: l.Array.cartesian_array) -> None:
        self.accelerations.append(acceleration)

# # @component
# class Force:
#     force: l.Array
#     def __init__(self, force: l.Array) -> None:
#         self.force = force

# @component
class ForceSelfOnOthers:
    isactingonothers: bool

# @component
class ForceOthersOnSelf:
    isothersacting: bool
    force: l.Array
    def set_force(self, force: l.Array) -> None:
        self.force = force

# @component
class UpdatesAnalytically:
    isupdatesanalytically: bool

# @component
class Visualised:
    isvisualised: bool
    color: str

# @component
class Monitoring:
    pass

class Particle:
    pass


class ForceHandler:

    def gravityforce_1(self, r1:l.Array, r2:l.Array, m1:Mass, m2:Mass) -> l.Array:
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

    def gravityforce_2(self, p1, p2) -> l.Array:
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
        r1, m1 = esper.get_components(p1, Position, Mass)
        r2, m2 = esper.get_components(p2, Position, Mass)

        return mymath.G * m1 * m2 * (r1 - r2) / ((r1 - r2).l.scal())**3

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
    def __init__(self, timestep: float = 1.0):
        self. timestep = timestep

    def process(self):
        for ent2, (pos2, mass2) in esper.get_components(Position, Mass, ForceSelfOnOthers): # here we get entities, with ForceSelfOnOthers
            for ent1, (pos1, mass1) in esper.get_components(Position, Mass, ForceOthersOnSelf):
                if ent1 != ent2:
                    print("type: " + type(ent1)) # FIXME delete after testing
                    force = ForceHandler().gravityforce_1(pos1[-1], pos2[-1], mass1, mass2)
                    


                    

                    

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

# forcecollectingprocessor = ForceCollectingProcessor()
# forceapplictionprocessor = ForceApplicationProcessor()
forceprocessor = ForceProcessor()
# analyticcoordinateupdateprocessor = AnalyticCoordinateUpdateProcessor()
# visualprocessor = VisualProcessor()

# esper.add_processor(forcecollectingprocessor)
# esper.add_processor(forceapplictionprocessor)
esper.add_processor(forceprocessor)
# esper.add_processor(analyticcoordinateupdateprocessor)
# esper.add_processor(visualprocessor)

# --- --- --- --- --- PROCESSING

esper.process()
# print(esper.list_worlds())
