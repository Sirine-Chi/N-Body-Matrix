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
from typing import Any, Final
import sys
import os
import math
from time import monotonic
import numpy as np
from numpy import array as v
import pandas as pd
import random2 as rnd
import pyopencl as cl
from numba import jit, prange
from tqdm import tqdm
import colorama
from colorama import Fore, Back, Style
from loguru import logger

colorama.just_fix_windows_console()
colorama.init()

logger.remove(0)
logger.add(sys.stdout, level="TRACE")


# CONSTANTS
G: Final = 0.0001184069  # 09138
K: Final = 4.0


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


def maximize_function(values, function):
    """
    returns maximum value of a function affected on container of values
    """
    return max(list(map(function, values)))

def minimize_function(values, function):
    """
    returns minimum value of a function affected on container of values
    """
    return max(list(map(function, values)))

# MATRIX FUNCTIONS

def openCL_mult(matrix1, matrix2):
    os.environ["PYOPENCL_CTX"] = "0"
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
    b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix1.nbytes)

    prg = cl.Program(ctx, """
        __kernel void multiplymatrices(const unsigned int size, __global float * matrix1, __global float * matrix2, __global float * res) {

        int i = get_global_id(1); 
        int j = get_global_id(0);

        res[i + size * j] = 0;

        for (int k = 0; k < size; k++)
        {
            res[i + size * j] += matrix1[k + size * i] * matrix2[j + size * k];
        }

        }
        """).build()
    # res[i + size * j] += matrix1[i + size * k] * matrix2[k + size * j];

    t0 = monotonic()

    prg.multiplymatrices(queue, matrix1.shape, None, np.int32(len(matrix1)), a_buf, b_buf, dest_buf)

    final_matrix = np.empty_like(matrix1)
    cl.enqueue_copy(queue, final_matrix, dest_buf)

    # print(final_matrix)

    delta_t = monotonic() - t0
    # print('OpenCL Multiplication: %.4f seconds' % delta_t)

    return final_matrix

def np_mult(matrix1, matrix2):  # =m1 x m2, порядок как в письме
    return matrix1.dot(matrix2)
    # return np.matmul(matrix1, matrix2)

def gravec(ri: np.ndarray, rj:np.ndarray) -> np.ndarray:
    """
    Unit vector of force, acting from body J to body I, devided by the squared distance
    \n
    :param: ri: np.ndarray | Position vector of first body (on which force acts)
    :param: rj: np.ndarray | Position vector of second body (which acts)
    """
    d = scal(ri - rj)
    if d == 0.0:
        return v([0, 0])
    else:
        return v((rj - ri) / d ** 3)

def gravecs_matrix(position_vectors):  # расчёт матрицы единичных векторов сил, действующих от тела j на тело i
    matrix = []  # собираем матрицу R_ij
    for i in position_vectors:
        line = []
        for j in position_vectors:
            line.append(gravec(i, j))
        matrix.append(line)
    # print(Style.DIM, Fore.RED, '\nMx start:\n', matrix, '\nMx end.\n', Style.RESET_ALL)
    return v(matrix)

def mass_vectors(objects):
    masses = []
    inv_masses = []
    for o in objects:
        masses.append(o[1])
        inv_masses.append(1 / o[1])
    return [v(masses), v(inv_masses)]

def position_matrix(objects):
    positions = []
    for o in objects:
        positions.append(v(o[2]))
    return positions

def velocity_matrix(objects):
    velocities = []
    for o in objects:
        velocities.append(v(o[3]))
    # return map(vel, objects)
    return velocities

def new_format_matrices(s):
    return {
        "Mass vector": mass_vectors(s)[0],
        "Coordinates vector": v(position_matrix(s)),
        "Velocities vector": v(velocity_matrix(s))
    }


# @jit(nogil=True, fastmath=True) #nopython=True, 
# def simulation(method="eiler", objects: list, dir, end, h):
#     matrices = format_matrices(objects)
#     new_matrices = new_format_matrices(objects)

#     r_sys_mx = []
#     v_sys_mx = []
#     a_sys_mx = []
#     v_sys_mx.append(new_matrices["Velocities vector"])
#     r_sys_mx.append(new_matrices["Coordinates vector"])

#     a_sys_mx.append(G * np_mult(gravecs_matrix(r_sys_mx[0]), np.vstack(new_matrices["Mass vector"])) )

#     num = int(dir * end / h)  # Number of steps
#     print(Fore.GREEN)

#     for i in tqdm(range(1, num)):
#         a_sys_mx.append(G * np_mult(gravecs_matrix(r_sys_mx[i-1])[0], np.vstack(v(new_matrices["Mass vector"]))) )

#         # метод эйлера
#         v_sys_mx.append(v_sys_mx[i - 1] + h * a_sys_mx[i])
#         r_sys_mx.append(r_sys_mx[i - 1] + h * v_sys_mx[i])
    
#     print(Style.RESET_ALL)
#     print(Fore.BLUE, r_sys_mx[-1], Style.RESET_ALL)

#     print(Back.GREEN, 'Finished!', 'Runtime:', "%.4f seconds" % (finish_time), Style.RESET_ALL, '\n')



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


class NumericalIntegrationMethod:
    def __init__(self, name: str, depth: int) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


# numerical methods
eiler = lambda x_nm, y_n, h: x_nm + h * y_n
adams = lambda x_nm, y_n, y_nd, h: x_nm + h * 3 / 2 * y_n - h / 2 * y_nd


# force functions
f_ij = lambda ri, rj, mi, mj: v(((rj - ri) * mi * mj * G) / (
    scal(ri - rj)) ** 3)  # функция силы Ньютоновской гравитации, действующей между двумя телами, даны массы и положения
analytic_f = lambda r0, v0, t: [(r0 + v0 * t - 5 * t ** 2), (v0 - 5 * t)]  # EXAMPLE!
f_gyk_ij = lambda ri, rj, mi, mj: v((rj-ri)*K)
