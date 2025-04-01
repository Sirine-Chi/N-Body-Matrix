from __future__ import annotations
from typing import Final, Iterable
import math
import numpy as np

from mydatatypes import TubeList

# CONSTANTS
G: Final = 0.0001184069  # 09138
# G: Final = 4 * (math.pi**2)
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
    """
    Converts a list of polar coordinates to Cartesian coordinates.
    Args:
        polar (list[float]): A list of polar coordinates, [0] is radius
                             and the subsequent elements are the angles in degrees.
    Returns:
        list[float]: A list of Cartesian coordinates corresponding to the given polar coordinates.
    Example:
        polar_to_decart([5, 45, 30]) -> [3.5355339059327378, 2.5, 4.330127018922193]
    """

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
    """
    Convert Cartesian coordinates to polar coordinates, angles in radians, using atan2

    Args:
        decart (list[float]): A list of Cartesian coordinates.
    Returns:
        list[float]: A list of polar coordinates where the first element is the radius (r) 
                     and the subsequent elements are the angles (theta) in radians.
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
