from __future__ import annotations
import yaml
from pandas import read_csv
from numpy import array as v
import colorama
from colorama import Fore, Back, Style

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


class Reader:

    @staticmethod
    def get_config(path_to_yaml: str) -> dict:
        stream = open(path_to_yaml, 'r')
        config = yaml.load(stream, Loader=yaml.FullLoader)
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

    @staticmethod
    def get_table_sliced(path_to_table: str, limit_down=0, limit_up=-1):
        table = read_csv(path_to_table)
        return table[limit_down:limit_up]

    @staticmethod
    def format_table(table):
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
    def format_table_dicts(table):
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


class Logger:
    def __init__(self):
        self.log_text = []

    def add_to_log(self, text):
        def log_append(something):
            self.log_text.append(something)

        recursive_writer(iterable_object=text, func=log_append)
        self.log_text.append('\n')

    def get_log(self) -> list:
        return self.log_text

    def print_log_to_console(self):
        for line in self.log_text:
            if type(line) == dict:
                for index in line:
                    print(' ' * (16 - len(index)), Fore.CYAN, index, Style.RESET_ALL, ':', line[index])
            elif type(line) == list:
                for element in line:
                    print(element)
            else:
                print(line)

    def save_log_to_txt(self, path_to_log: str):
        file = open(path_to_log + '/results.txt', 'w')
        recursive_writer(iterable_object=self.log_text, func=file.write())
