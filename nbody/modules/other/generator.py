# from typing import Optional as opt
from numpy import random
from loguru import logger
from nbody.modules.linal.linal_lib import Array
from nbody.modules.data.data_manager import YamlManager
# from nbody.modules.data.data_manager import YamlManager # for commented code
# from n_body_lib import *

DEFAULT_GENERATING_PATTERN: dict = {
    "number of objects": 2,
    "center": Array.new_mx_from_list([0.0, 0.0, 0.0]),
    "medium radius": 1.0,
    "crit radius delta": 0.25,
    "medium mass": 1.0,
    "crit mass delta": 0.0,
    "mass center velocity": Array.new_mx_from_list([0.0, 0.0, 0.0]),
    "medium velocity scalar": 0.0,
    "velocity crit delta": 0.0
}

# FIXME haven't find implementation, TODO read and understad, what it's doing

# class GeneratingPattern:
#     def __init__(self) -> None:
#         self.pattern: dict = DEFAULT_GENERATING_PATTERN

#     def set_pattern(self, pattern: dict) -> None:
#         """
#         Set pattern from dictionary
#         """
#         self.validate_pattern()
#         self.pattern: dict = pattern

#     def set_pattern_manually(self, num: int, cen: np.ndarray, med_rad: float, crit_rad_d: float, med_m: float,
#                              crit_m_d: float, m_cen_vel: np.ndarray, med_vel_scal: float, vel_crit_d: float) -> None:
#         """
#         Manually sets parametres to generating pattern dictionary
#         """
#         self.pattern = {
#             "number of objects": num,
#             "center": cen,
#             "medium radius": med_rad,
#             "crit radius delta": crit_rad_d,
#             "medium mass": med_m,
#             "crit mass delta": crit_m_d,
#             "mass center velocity": m_cen_vel,
#             "medium velocity scalar": med_vel_scal,
#             "velocity crit delta": vel_crit_d
#         }

#     def load_pattern_from_yaml(self, path_to_yaml):
#         """
#         Loads pattern from yaml file and sets it
#         """
#         self.pattern = YamlManager.get_yaml(path_to_yaml)
#         self.validate_pattern()

#     def __str__(self) -> str:
#         return str(self.pattern)

#     def validate_pattern(self):
#         lines = []
#         for key in DEFAULT_GENERATING_PATTERN.items():
#             if type(DEFAULT_GENERATING_PATTERN[key]) != type(self.pattern[key]):
#                 line = f"Mistake in option {key},\n your type is {type(self.pattern[key])}, but must be {type(DEFAULT_GENERATING_PATTERN[key])}"
#                 logger.error(line)
#                 lines.append(line)
#         return lines


class TableGenerator:
    def __init__(self) -> None:
        self.default_pattern = DEFAULT_GENERATING_PATTERN

    def spherical(self, pattern: dict = DEFAULT_GENERATING_PATTERN) -> list:
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

# TODO pattern(dict) class, 

default_path: str = "nbody/tmp/patterns"
class GeneratingPattern(dict):
    
    def __init__(self):
        self.pattern = {"a": "a"}

    def read_pattern_from_yaml(self, path_to_pattern: str = default_path+'/pattern.yaml'):
        self.pattern = YamlManager.get_yaml(path_to_pattern)
        print(self.pattern)
        
    def validate_pattern(self):
        lines = []
        for key in DEFAULT_GENERATING_PATTERN.items():
            if type(DEFAULT_GENERATING_PATTERN[key]) is not type(self.pattern[key]):
                line = f"Mistake in option {key},\n your type is {type(self.pattern[key])}, but must be {type(DEFAULT_GENERATING_PATTERN[key])}"
                logger.error(line)
                lines.append(line)
        return lines

g = GeneratingPattern()
g.read_pattern_from_yaml()
