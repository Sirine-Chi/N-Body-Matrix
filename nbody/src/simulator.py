"""
Simulator class
"""
from dataclasses import dataclass as component
import esper
import modules.core.mylinal as l


class Simulator:
    def __init__(self, particlesp: list, end_timep: float, stepp: float):
        self.begin_runtime: float = monotonic()
        self.particles: list = particlesp
        self.end_time: float = end_timep
        self.step: float = stepp

    def particle_init(self):
        pass

    def simulation(self):
        pass

    def get_positions(self) -> list[list]:
        pass

    def get_runtime(self) -> float:
        return monotonic() - self.begin_runtime
