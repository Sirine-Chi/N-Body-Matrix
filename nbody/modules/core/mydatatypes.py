"""
Some custom data types
"""

from __future__ import annotations
from typing import Iterable
from collections.abc import MutableSequence
from dataclasses import dataclass

@dataclass
class TubeList(MutableSequence):
    """List with fixed lenght, where you can read any element,\n
    but adding just on top like in stack,\n
    If the tubelist is full, adding new values will pop the bottom element\n
    When tubelist is created, the lenght is checked, gives error when you trying to init it with more element\n
    """
    tube: list

    def __str__(self) -> str:
        return str(self.tube)

    def __init__(self, thelist: Iterable, depth: int):
        self.depth: int = depth
        self.tube = thelist

        if len(thelist) > depth:
            raise ValueError

    def __len__(self):
        return len(self.tube)

    def __getitem__(self, index):
        return self.tube[index]

    def __delitem__(self, index):
        del self.tube[index]

    def check_depth(self):
        if len(self) == self.depth+1:
            self.pop(0)

    def __setitem__(self, index, value):
        """There's no way to insert element anywhere in tubelist =)
        """
        raise IndexError

    def insert(self, index, value):
        if index == len(self):
            self.tube.insert(index, value)
            self.check_depth()
        else:
            raise IndexError

class PseudoEnum:
    """
    Special type for creating declared Enums
    """
    registery: list[PseudoEnum] = []
    values: list = []

    def __init__(self, values: list):
        self.values += values

        self.registery.append(self)


class Node:
    """Node for stack
    """
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    """Classic stack
    """
    def __init__(self):
        self.head = Node("head")
        self.size = 0

    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-2]

    def len(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def peek(self):

        if self.isEmpty():
            raise IndexError("Peeking from an empty stack")
        return self.head.next.value

    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise IndexError("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value