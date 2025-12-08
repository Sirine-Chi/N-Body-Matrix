"""
Module to manage markup files: TOML, YAML.
# FIXME add json support
"""

from tomlkit import load, dump
from loguru import logger
import yaml

# --- TOML ---

def get_toml(path: str) -> dict:
    """
    Reads toml file on given path, as dictonary
    If not found, returns empty dictionary.
    """
    try:
        with open(path, 'r', encoding="utf-8") as stream:
            content = load(stream)
            logger.trace(f"FIle loaded at path {path}")
    except (FileNotFoundError, FileExistsError) as error:
        message = f"File not found on path {path}, \n {error}"
        logger.trace(message)
        return {}
    return content

def save_toml(path: str, data: dict, file_name="toml_content.toml") -> None:
    """
    Saves data to toml file on given path
    """
    with open(path + "/" + file_name, 'w', encoding="utf-8") as stream:
        dump(data, stream, sort_keys=False)
        # stream.write(data)

# --- YAML ---

def get_yaml(path: str) -> dict:
    """
    Reads yaml file on given path, as dictonary
    If not found, returns empty dictionary.
    """
    try:
        # with open(path, 'r', encoding="utf-8") as stream:
        #     content = yaml.load(stream, Loader=yaml.FullLoader)
        with open(path, 'r', encoding="utf-8") as stream:
            content = yaml.safe_load(stream)
            logger.trace(f"FIle loaded at path {path}")
    except (FileNotFoundError, FileExistsError) as error:
        message = f"File not found on path {path}, \n {error}"
        logger.trace(message)
        return {}
    return content

def save_yaml(path: str, data: dict, file_name="yaml_content.yaml") -> None:
    """
    Saves data to yaml file on given path
    """
    with open(path + "/" + file_name, 'w', encoding="utf-8") as stream:
        yaml.dump(data, stream, default_flow_style=False, sort_keys=False)

# def test() -> None:
#     path1: str = "nbody/info.toml"
#     path2: str = "nbody/info.yaml"
#     t = get_toml(path1)
#     y = get_yaml(path2)

#     print(f"T is Y: {t == y} \n")

#     print("TOML")
#     for key, value in t.items():
#         print(f"{key}:: {value} \n")

#     print("YAML")
#     for key, value in y.items():
#         print(f"{key}:: {value} \n")
