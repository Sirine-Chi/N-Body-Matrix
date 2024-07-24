from __future__ import annotations
import yaml
from loguru import logger
from typing import Iterable

def recursive_writer(iterable_object: list, func):
    """
    Function to write iterables, even if they can't be written as one object
    """
    limit: int = 1
    calls: int = 0
    while calls <= limit:
        try:
            func(iterable_object)
        except TypeError:
            for element in iterable_object:
                recursive_writer(element, func)
        calls += 1
    # raise Exception('RecursionFailed').with_traceback(recursive_writer(iterable_object, func))


def parallel(something: Iterable) -> Iterable:
    """
    Function to unfold iterables to one parallel iterable
    """
    parl = []
    if isinstance(something, list) or isinstance(something, tuple):
        for element in something:
            parl += parallel(element)
    elif isinstance(something, dict):
        for index in something:
            parl.append([index, something[index]])
    else:
        parl.append(something)
    return parl


class YamlManager:
    """
    Functions to work with yaml files and it's content
    """

    @staticmethod
    def get_yaml(path_to_yaml: str) -> dict:
        """
        Reads yaml file on given path, as dictonary
        If not found, returns empty dictionary.
        """
        try:
            with open(path_to_yaml, 'r', encoding="utf-8") as stream:
                content = yaml.load(stream, Loader=yaml.FullLoader)
        except (FileNotFoundError, FileExistsError) as error:
            message = f"File not found on path {path_to_yaml}, \n {error}"
            logger.trace(message)
            return {}
        return content

    @staticmethod
    def print_yaml(yaml_content: dict) -> None:
        maxlen = max(list(map(len, yaml_content.keys())))
        for index in yaml_content.items():
            print(" " * (maxlen - len(index)), index, ":", yaml_content[index])

    @staticmethod
    def save_yaml_to_txt(yaml_content: dict, path_to_txt: str, file_name="yaml_content.txt") -> None:
        try:
            with open(path_to_txt + file_name, 'w', encoding="utf-8") as file:
                maxlen = max(list(map(len, yaml_content.keys())))
                for key in yaml_content:
                    file.write(" " * (maxlen - len(key)) + f"{key} : {yaml_content[key]}")
        except (FileExistsError, FileNotFoundError) as error:
            message = f"Can't write file, maybe there's no such directory as {path_to_txt + file_name},\n {error}"
            logger.trace(message)

    @staticmethod
    def save_to_yaml(yaml_content: dict, path_to_yaml: str, file_name="yaml_content.txt") -> None:
        with open(path_to_yaml + "/" + file_name, 'w', encoding="utf-8") as stream:
            yaml.dump(yaml_content, stream, default_flow_style=False, sort_keys=False)
