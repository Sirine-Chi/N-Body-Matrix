from __future__ import annotations
from typing import Final, Iterable
import math
import numpy as np

from mydatatypes import TubeList

# CONSTANTS
G: Final = 0.0001184069  # 09138
K: Final = 4.0

def mul(args: Iterable):
    """Multiplies any given number of variables
    """
    m = 1
    for i in args:
        m *= i
        # print(f"m: {m}")
    return m

def lmap(f, values: Iterable):
    """list(map(...))
    """
    return list(map(f, values))

def maximize_function(values: Iterable, function: Iterable):
    """
    returns maximum value of a function affected on container of values
    """
    return max(lmap(function, values))

def minimize_function(values: Iterable, function: Iterable):
    """
    returns minimum value of a function affected on container of values
    """
    return min(lmap(function, values))

class Axis:
    """
    Represents axes, contains integer > 0
    Numerates up from 0
    """
    def __init__(self, n: int):
        if n >= 0:
            self.n : int = n
        else:
            raise ValueError("axis value must be >= 0")

class Plane:
    """To represent planes of rotation, as combination of 2 axes
    """

    def __init__(self, ax_1: Axis, ax_2: Axis):
        self.a1 = ax_1
        self.a2 = ax_2

class Angle(float):
    """
    In radians by default, >0 - forced
    """
    
    @staticmethod
    def new_deg_angle(d: float):
        d = Angle.normalise_angle(d, 360.0)
        return(Angle(d*2*math.pi/360.0))
    # phi / 2pi = alpha / 360

    @staticmethod
    def new_rad_angle(r: float):
        r = Angle.normalise_angle(r, 2*math.pi)
        return Angle(r)
    
    @staticmethod
    def normalise_angle(a: Angle, p: Angle) -> Angle:
        # angle in (0, Period)
        i = 0
        while a < 0:
            a += (p*i)
            i+=1
        return a
    
    @staticmethod
    def radians(degrees: float):
        return degrees*2*math.pi/360.0
    
    @staticmethod
    def degrees(radians: float):
        return radians*360/(2*math.pi)

def polar_to_decart(polar: list[float]) -> list[float]:
    lenght: int = len(polar) # phi_i = pol[i]
    d: list = [None] * lenght
    r = polar[0]

    def sin(a): # from degrees
        if abs(math.sin(math.radians(a))) < 1e-15:
            return 0
        return math.sin(math.radians(a))
    
    def cos(a):
        def check(a: float) -> float:
            values = (-1, 1, 0)
            for i in values:
                if abs(i - a) < 1e-15:
                    return i
            return a
        
        return check( math.cos(math.radians(a)) )

    match lenght:
        case 1:
            d[0] = r
        case _:
            d[0] = r * cos(polar[1])
            for i in range(2, lenght): # i correspondes to angle in pol
                d[i-1] = r * cos(polar[i]) * mul(lmap(sin, polar[1:i]))
                # r*cos(a_n-1)* sin(a_1)*...*sin(a_n-2)
            d[lenght-1] = r * mul(lmap( sin, polar[1:lenght] ))

    return d

def decart_to_polar(decart: list[float]) -> list[float]:
    """Cartesian to polar coordinates connversion, angles in radians, using atan2
    """
    lenght: int = len(decart)
    pol: list = [None] * lenght
    r = float(np.linalg.norm(np.array(decart), ord=2))
    pol[0] = r
    def square(a):
        return a**2
    
    for i in range(1, lenght):
        pol[i] = math.atan2((sum(lmap(square, decart[i+1:lenght])))**0.5, decart[i])
        
    return decart

# FIXME make tubelists of vels, poss as inputs

class numeric_methods:

    # FIXME strange NM class, uncertain about it

    def __init__(self, order=1) -> None:
        self.order = order

    #input: previous Y, previous X, Step, Order
    # input: vel, pos, step, order

    @staticmethod
    def euler(x_nm, y_n, h):
        return x_nm + h * y_n
    
    @staticmethod
    def eiler(pos: TubeList,
              vel: TubeList,
              step: float): # order: int = 1
        return pos[-1] + step*vel[-1]
        # if order != 1:
        #     raise IndexError(f"Method with order 1 was called with order {order}")
    
    @staticmethod
    def adams(pos: TubeList,
              vel: TubeList,
              step: float): # order: int = 2
        return pos[-1] + step * 3 / 2 * vel[-1] - step / 2 * vel[-2]
        # if order != 2:
        #     raise IndexError(f"Method with order 1 was called with order {order}")


    # @staticmethod
    # def runge_kutta(pos: TubeList, vel: TubeList, step: float, func, order: int):
    #     def 
    #     sum_bk = []
    #     for i in range(order):
    #         sum_ak = []
    #         for i in range(i-1):
    #             sum_ak.append(a_i_1*k_1)
    #         k_i = func(t_n + c_i*step, y_n + (sum(sum_ak)))
    #         sum_bk.append(b(i) * k_i)
    #     y_n = y_nm + step*sum(sum_bk)

        
    #     pass
