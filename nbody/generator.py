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

# FIXME test and check all toml imports
    @staticmethod
    def get_pattern_from_toml( path_to_pattern: str = DEFAULT_PATH+'/pattern.toml'):
        return markup_manager.get_toml(path_to_pattern)["Pattern"]

    def __init__(self, pattern = get_pattern_from_toml(tmp_path)):
        self.pattern = pattern
        logger.trace(f"the pattern is loaded from {tmp_path}")

    def __str__(self) -> str:
        return self.pattern


class TableGenerator:
    def __init__(self) -> None:
        self.pattern: dict
        self.objects_data: dict
        self.type: str
    
    def spherical(self, pattern: dict = Pattern.get_pattern_from_toml(DEFAULT_PATH+'/pattern_benchmark.toml')) -> dict:
        """
        :param pattern: dict | dictionary with settings for generator
        :returns list | data to write to csv table
        """
        self.objects_data: dict = {}
        self.pattern = pattern
        self.type = 'spherical'
        # object_type = "dynamic"

        for i in range(0, pattern["number_of_objects"]):
            st_der = pattern["crit_mass_delta"] / 3
            position = Array.new_mx_from_list(pattern["center_pos"]) + Array.randarr_less_than_lenght(pattern["medium_radius"])
            velocity = Array.new_mx_from_list(pattern["center_mass_vel"]) + Array.randarr_less_than_lenght(pattern["medium_velocity_scalar"])

            object: dict = {
                "Mass": random.normal(pattern["medium_mass"], st_der),
                "R (polar)": position.give_list(),
                "V (polar)": velocity.give_list(),
                "Color": Array.randarr_less_than_lenght(1, 3).give_list(),
                "force_1 (to, from)": [1, 1],
                "force_2 (to, from)": [0, 0],
            }
            self.objects_data[ f"{i}" ] = object
        return self.objects_data

    def write_data(self, path_to_write = "nbody/systems"):
        data_n: dict = {
            "Type": self.type,
            "Pattern": self.pattern,
            "Bodies": self.objects_data,
            }
        markup_manager.save_toml(
            path = path_to_write,
            data = data_n,
            file_name= f"{datetime.now()}.toml"
            )
        # I want to save the pattern itself also

# Pattern.write_data(
#     data = Pattern.spherical(),
#     path_to_write = 
# )

gen1 = TableGenerator()
gen1.spherical()
gen1.write_data( path_to_write="nbody/systems")

# TableGenerator.write_data( data=TableGenerator().spherical(), path_to_write="nbody/systems" )


# ['999', 'dynamic', 10.0, Array: [49.78313438812249, 4.629753155590941, 0.4526767195602096], Array: [1.9970351862870175, 0.10854215476735692, 0.008310557745197553], array([0.86074519, 0.05724164, 0.00095352])]

# "Sun" = {"Mass" = 332840, "R (polar)" = [0.0, 0.0, 0.0], "V (polar)" = [0.0, 0.0, 0.0], "Color" = [1.0, 1.0, 0.0], "force_1 (to, from)" = [1, 1], "force_2 (to, from)" = [0, 0], "force_3 (to, from)" = [0, 0], "force_4 (to, from)" = [0, 0]}

# print( Pattern.get_pattern_from_toml(tmp_path) )
