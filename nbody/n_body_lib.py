"""
N Body Library
=====

Provides:
    1. Vector math functions
    2. Numerical methods as lambda functions
    3. Physical and astronomical constants
    4. Imports for numpy, pandas, pyopencl, pyopengl, numba, tqdm, colorama, loguru
"""

from __future__ import annotations
import sys
import numpy as np
from numpy import array as v
import pandas as pd
import math
import random2 as rnd
from time import monotonic
import datetime
import pyopencl as cl
from numba import jit, prange
from tqdm import tqdm
from typing import Final
import colorama
from colorama import Fore, Back, Style
from loguru import logger

colorama.just_fix_windows_console()
colorama.init()

logger.remove(0)
logger.add(sys.stdout, level="TRACE")

def scal(vec: np.ndarray) -> float:
    """
    Vector length in Euclidian space (l2 norm, or scalar)
    \n
    :param: np.ndarray | vector
    :return: float | scalar
    """
    return np.linalg.norm(vec, ord=2)


def unvec(vec: np.ndarray) -> np.ndarray:
    """
    Vector with same direction as on input, but with length = 1 (unit-vector)
    \n
    vec: np.ndarray | vector
    return: np.ndarray | unit-vector
    """
    return vec / scal(v)


def ranvec(r: float) -> np.ndarray:
    """
    Random vector with lengh r
    \n
    r: float | vector length
    return: np.ndarray | random vector
    """
    rv = v([rnd.uniform(-r, r), 2 * (rnd.getrandbits(1) - 0.5) * (r ** 2 - rnd.uniform(-r, r) ** 2) ** 0.5])
    return rv


def ranrv(r: float) -> np.ndarray:
    """
    Random vector with random radius < r
    \n
    r: float | length
    return: np.ndarray | random vector
    """
    a = rnd.uniform(0, 2 * math.pi)
    rr = rnd.uniform(0, r)
    rv = v([rr * math.cos(a), rr * math.sin(a)])  # radians
    return rv


def rotvec(vec: np.ndarray, al: float) -> np.ndarray:
    """
    Rotates 2D vector on AL degrees, multiplies rotation matrix on vector   v' = M*v
    \n
    vec: np.ndarray | vector to rotate
    al: float | rotation angle in degrees
    returns: np.ndarray | rotated vector
    """
    rotation_mx = v([[math.cos(math.radians(al)), math.sin(math.radians(al))],
                     [-1 * math.sin(math.radians(al)), math.cos(math.radians(al))]])
    return np.matmul(vec, rotation_mx)

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
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
            raise Exception("Peeking from an empty stack")
        return self.head.next.value

    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1

    def pop(self):
        if self.isEmpty():
            raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value

# numerical methods
eiler = lambda x_nm, y_n, h: x_nm + h * y_n
adams = lambda x_nm, y_n, y_nd, h: x_nm + h * 3 / 2 * y_n - h / 2 * y_nd

# force functions
f_ij = lambda ri, rj, mi, mj: v(((rj - ri) * mi * mj * G) / (
    scal(ri - rj)) ** 3)  # функция силы Ньютоновской гравитации, действующей между двумя телами, даны массы и положения
analytic_f = lambda r0, v0, t: [(r0 + v0 * t - 5 * t ** 2), (v0 - 5 * t)]  # EXAMPLE!

# CONSTANTS
G: Final = 0.0001184069  # 09138
