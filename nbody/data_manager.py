from __future__ import annotations
import yaml
from pandas import read_csv, DataFrame
from numpy import array as v
import colorama
from colorama import Fore, Back, Style
import n_body_lib

colorama.just_fix_windows_console()
colorama.init()


def recursive_writer(iterable_object: list, func):
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


class ConfigManager:

    @staticmethod
    def get_config(path_to_yaml: str) -> dict:
        """
        Reads config file on given path
        """
        try:
            stream = open(path_to_yaml, 'r')
            config = yaml.load(stream, Loader=yaml.FullLoader)
        except FileNotFoundError:
            # logger.trpip install pyinstaller
            return {}
            raise FileNotFoundError
        return config

    @staticmethod
    def print_config_to_console(config: dict):
        for index in config:
            print(' ' * (16 - len(index)), Fore.CYAN, index, Style.RESET_ALL, ':', config[index])

    @staticmethod
    def save_config_to_txt(config: dict, path_to_txt: str):
        file = open(path_to_txt + '/results.txt', 'w')
        for index in config:
            file.write(' ' * (15 - len(index)), index, ':', config[index], '\n')
        file.close()

class TableManager:
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
    def format_table(table: DataFrame) -> list:
        lines = []
        for line in table.to_numpy():
            lines.append(
                [
                    str(line[1]).replace(' ', ''),
                    line[2],
                    v([line[3], line[4]]),
                    v([line[5], line[6]]),
                    line[7].replace(' ', ''),
                    line[8]
                ]
            )
        return lines

    @staticmethod
    def format_table_dicts(table: DataFrame) -> list:
        dicts = []
        for line in table.to_numpy():
            dicts.append(
                {
                    'name': str(line[1]),
                    'mass': line[2],
                    'start_position': v([line[3], line[4]]),
                    'start_velocity': v([line[5], line[6]]),
                    'color': str(line[7]),
                    'start_angle': line[8]
                }
            )
        return dicts


class ReportManager:
    def __init__(self):
        """
        Class constructor
        """
        self.report_list = []
        self.report_dict = {}

    def add_to_report(self, *text):
        """
        Adds any object to log 
        \n
        *text: auto | any number of any objects, that we add to log
        """
        def log_append(something):
            self.report_list.append(something)
            if isinstance(*text, dict):
                self.report_dict[text] = text[text]

        for item in text:
            log_append(item)
        # recursive_writer(iterable_object=text, func=log_append)

    def get_report(self) -> list:
        return self.report_list
    

    # Make abstract fabric
    def print_report_to_console(self):
        for item in parallel(self.report_list):
            print(item)

    def save_report_to_txt(self, path_to_report: str):
        file = open(path_to_report + '/report.txt', 'w', encoding='utf-8')
        for item in parallel(self.report_list):
            if isinstance(item[0], list) or isinstance(item, tuple):
                for element in item:
                    file.write(str(element) + ', ')
            else:
                file.write(str(item)[1:-1] + '\n')
        file.close()

    def save_report_to_yaml(self, path_to_report: str):
        stream = open(path_to_report+'/report.yaml', 'w')
        # yaml.dump_all()
