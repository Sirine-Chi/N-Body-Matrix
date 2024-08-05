from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Command:
    name: str
    description: str
    childs: list[Command]
    arguments: list[str]

    def __init__(self, name):
        self.name = name
    
    def do(self):
        print(f"{self.name} Done!")


        """
        > hints
        -> hints is on/offf

        > hints off
        -> hints turned off

        > help
        -> output

        > load
        > table = path_to_table
        -> output

        > load table = path_to_table
        """

