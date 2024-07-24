# from typing import Optional as opt
from dataclasses import dataclass
from typing import Final
import copy
from numpy import random
from loguru import logger
from nbody.modules.data.data_manager import YamlManager
from nbody.modules.core.mylinal import Array

DEFAULT_GENERATING_PATTERN: Final = {
    "number of objects": 2,
    "center": Array.cartesian_array([0.0, 0.0, 0.0]),
    "medium radius": 1.0,
    "crit radius delta": 0.25,
    "medium mass": 1.0,
    "crit mass delta": 0.0,
    "mass center velocity": Array.cartesian_array([0.0, 0.0, 0.0]),
    "medium velocity scalar": 0.0,
    "velocity crit delta": 0.0
}

class TableGenerator:
    def __init__(self) -> None:
        self.default_pattern = DEFAULT_GENERATING_PATTERN

    def spherical(self, pattern: dict = copy.deepcopy(DEFAULT_GENERATING_PATTERN)) -> list:
        """
        :param pattern: dict | dictionary with settings for generator
        :returns list | data to write to csv table
        """
        objects_data = []
        object_type = "dynamic"
        for i in range(0, pattern["number of objects"]):
            st_der = pattern["crit mass delta"] / 3
            position = pattern["center"] + Array.randarr_fixed_length(pattern["medium radius"])
            velocity = pattern["mass center velocity"] + Array.randarr_fixed_length(pattern["medium velocity scalar"])
            objects_data.append(
                [
                    str(i),
                    str(object_type),
                    random.normal(pattern["medium mass"], st_der),
                    position,
                    velocity,
                    'w'
                ])
        # print(*objects_data, sep="\n")
        return objects_data

DEFAULT_PATH: str = "nbody/tmp/patterns"

@dataclass
class GeneratingPattern:
    number_of_objects: int = 2
    center_pos: Array = Array.cartesian_array([0.0, 0.0, 0.0])
    medium_radius: float = 1.0
    crit_radius_delta: float = 0.25
    medium_mass: float = 1.0
    crit_mass_delta: float = 0.0
    center_mass_vel: Array = Array.cartesian_array([0.0, 0.0, 0.0])
    medium_value_vel: float = 0.0
    velocity_crit_delta: float = 0.0
    
    def __init__(self, pattern: dict = copy.deepcopy(DEFAULT_GENERATING_PATTERN)):
        self.pattern = pattern

    def __str__(self) -> str:
        return self.pattern

    def read_pattern_from_yaml(self, path_to_pattern: str = DEFAULT_PATH+'/pattern.yaml'):
        p = YamlManager.get_yaml(path_to_pattern)
        if GeneratingPattern.pattern_is_valid(p):
            self.pattern = p
            print(self.pattern)
    
    @staticmethod
    def pattern_is_valid(pattern: dict):
        for key in DEFAULT_GENERATING_PATTERN.items():
            if type(DEFAULT_GENERATING_PATTERN[key]) is not type(pattern[key]):
                logger.error(f"Mistake in option {key},\n your type is {type(pattern[key])}, but must be {type(DEFAULT_GENERATING_PATTERN[key])}")
                return False
        return True

g = GeneratingPattern()
g.read_pattern_from_yaml()
