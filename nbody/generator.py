from dataclasses import dataclass
from typing import Final
import copy
from numpy import random
from loguru import logger
import markup_manager
from mylinal import Array
from datetime import datetime


# FIXME rethink the way of generating patterns

DEFAULT_PATH: str = "dev/tmp"
tmp_path = "dev/tmp/pattern_benchmark.toml"

# @dataclass
class Pattern:
    """
    To check if some generator conform the convention
    """
    number_of_objects: int = 1000
    center_pos: Array = [0.0, 0.0, 0.0]
    medium_radius: float = 1.0
    crit_radius_delta: float = 0.25
    medium_mass: float = 1.0
    crit_mass_delta: float = 0.0
    center_mass_vel: Array = [0.0, 0.0, 0.0]
    medium_value_vel: float = 0.0
    velocity_crit_delta: float = 0.0

# FIXME test and check all toml imports
    @staticmethod
    def get_pattern_from_toml( path_to_pattern: str = DEFAULT_PATH+'/pattern.toml'):
        # p = markup_manager.get_toml(path_to_pattern)["Pattern"]
        return markup_manager.get_toml(path_to_pattern)["Pattern"]
        # if Pattern.pattern_is_valid(p):
        #     return p

    def __init__(self, pattern = get_pattern_from_toml(tmp_path)):
        self.pattern = pattern
        logger.trace(f"the pattern is loaded from {tmp_path}")

    def __str__(self) -> str:
        return self.pattern

    # @staticmethod
    # def pattern_is_valid(pattern: dict):
    #     DEFAULT_GENERATING_PATTERN: Final = {
    #         "number of objects": 2,
    #         "center": Array.cartesian_array([0.0, 0.0, 0.0]),
    #         "medium radius": 1.0,
    #         "crit radius delta": 0.25,
    #         "medium mass": 1.0,
    #         "crit mass delta": 0.0,
    #         "mass center velocity": Array.cartesian_array([0.0, 0.0, 0.0]),
    #         "medium velocity scalar": 0.0,
    #         "velocity crit delta": 0.0
    #     }
    #     for key in DEFAULT_GENERATING_PATTERN.items():
    #         if type(DEFAULT_GENERATING_PATTERN[key]) is not type(pattern[key]):
    #             logger.error(f"Mistake in option {key},\n your type is {type(pattern[key])}, but must be {type(DEFAULT_GENERATING_PATTERN[key])}")
    #             return False
    #     return True

class TableGenerator:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def spherical( pattern: dict = Pattern.get_pattern_from_toml(DEFAULT_PATH+'/pattern_benchmark.toml')) -> list:
        """
        :param pattern: dict | dictionary with settings for generator
        :returns list | data to write to csv table
        """
        objects_data = []
        object_type = "dynamic"
        for i in range(0, pattern["number_of_objects"]):
            st_der = pattern["crit_mass_delta"] / 3
            position = Array.new_mx_from_list(pattern["center_pos"]) + Array.randarr_fixed_length(pattern["medium_radius"])
            velocity = Array.new_mx_from_list(pattern["center_mass_vel"]) + Array.randarr_fixed_length(pattern["medium_velocity_scalar"])
            objects_data.append(
                [
                    str(i),
                    str(object_type),
                    random.normal(pattern["medium_mass"], st_der),
                    position,
                    velocity,
                    Array.randarr_less_than_lenght(1, 3).m
                ])
        # print(*objects_data, sep="\n")
        return objects_data

    @staticmethod
    def write_data(self, data, path_to_write = "nbody/systems"):
        markup_manager.save_toml(path = path_to_write, data = data, file_name= f"{datetime.now()}" )
        # I want to save the pattern itself also

# print( TableGenerator().spherical() )

# print( Pattern.get_pattern_from_toml(tmp_path) )
