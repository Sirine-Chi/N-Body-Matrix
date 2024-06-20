from __future__ import annotations
import yaml
from pandas import read_csv, DataFrame
# import csv
from n_body_lib import *

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


def parallel(something: list) -> list:
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
            print(" " * (maxlen - len(index)), Fore.CYAN, index, Style.RESET_ALL, ":", yaml_content[index])

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


class ConfigManager:
    """
    Class to work with config
    """
    def __init__(self, path_to_config: str) -> None:
        self.config: dict = YamlManager.get_yaml(path_to_yaml=path_to_config)

    def get_config(self, path_to_config: str) -> dict:
        return self.config
    
    def print_config_to_console(self):
        YamlManager.print_yaml(self.config)
    
    def save_config_to_txt(self, path_to_txt: str, file_name="config.txt"):
        YamlManager.save_yaml_to_txt(self, path_to_txt, file_name)


class TableManager:
    """
    Class to work with configuration tables
    """

    @staticmethod
    def get_table_sliced(path_to_table: str, limit_down=0, limit_up=-1 ) -> DataFrame:
        """
        Reads table from files, gives away table, sliced from one object to other
        \n
        path_to_table: str | path to the table
        limit_down: int | first object
        limit_up: int | last object
        returns: pd.DataFrame | sliced table
        """

        table = read_csv(path_to_table)
        return table[limit_down:limit_up]

    @staticmethod
    def format_table_dicts(table: DataFrame) -> list[dict]:
        """returns list of dicts containing object initialisation parameters

        Args:
            table (DataFrame): _description_

        Returns:
            list(dict): _description_
        """
        dicts = []
        for line in table.to_numpy():
            dicts.append(
                {
                    'name': str(line[0]),
                    'type': str(line[1]),
                    'mass': line[2],
                    'start_position': v([line[3], line[4], line[5]]),
                    'start_velocity': v([line[6], line[7], line[8]]),
                    'color': str(line[9]),
                    'start_angle': line[10]
                }
            )
        return dicts


class Report:
    """
    Class to work with report, that stores values as dictionary
    """
    def __init__(self):
        """
        Class constructor
        """
        self.report_dict = {}

    def add_to_report(self, item: dict) -> None:
        """
        Adds any object to log 
        \n
        :param: item: dict | any number of any objects, that we add to log
        """
        for key in item.keys():
            self.report_dict[key] = item[key]
        # recursive_writer(iterable_object=text, func=log_append)

    def get_report(self) -> list:
        return self.report_dict
    
    def print_report_to_console(self) -> None:
        for item in parallel(self.report_dict):
            print(item)

    def save_report_to_txt(self, path_to_report: str) -> None:
        with open(path_to_report + '/report.txt', 'w', encoding='utf-8') as file:
            for item in parallel(self.report_dict):
                if isinstance(item[0], list) or isinstance(item, tuple):
                    for element in item:
                        file.write(str(element) + ', ')
                else:
                    file.write(str(item)[1:-1] + '\n')

    def save_report_to_yaml(self, path_to_report: str) -> None:
        YamlManager.save_to_yaml(self.report_dict, path_to_report, file_name="report.yaml")
