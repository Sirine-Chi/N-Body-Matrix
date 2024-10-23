from __future__ import annotations
import math
import numpy as np
from mymath import Plane, Angle, polar_to_decart
# from random import randrange
    
# parentness: Mx -> arr? -> 3d -> 2d

class Mx:
    """Matrix class
    """
	
    def __init__(self, ms : np.array):
        """Matrix constructor
        """
		
        self.m : np.array = ms
    
    @staticmethod
    def new_mx_from_list( m: list):
        return Mx(np.array(m))

    # print
    def __str__(self) -> str:
        return f"Matrix: {self.m}"

	# +
    def __add__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(self.m + other.m)
        else:
            return Mx(self.m + other)

    # +=
    def __iadd__(self, other) -> None:
        if isinstance(other, Mx):
            self.m += other.m
        else:
            self.m += other

    # -
    def __sub__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(self.m - other.m)
        else:
            return Mx(self.m - other)

    # dot product
    def __mul__(self, other) -> Mx:
        return Mx(np.dot(self.m, other.m))

    # hadamar %
    def __mod__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(np.multiply(self.m, other.m))
        else:
            try:
                return Mx(np.multiply(self.m, other))
            except TypeError:
                print("Oops! Not a matrix type")

    # transpose
    def transpose(self) -> Mx:
        return(Mx(np.matrix_transpose(self.m)))
    
    @staticmethod
    def rotation_matrix(angle: Angle, p: Plane, d: int = 3) -> Mx:
        m = np.zeros((d, d))
        m[p.a1.n, p.a1.n] = math.cos(angle)
        m[p.a1.n, p.a2.n] = -1*math.sin(angle)
        m[p.a2.n, p.a1.n] = math.sin(angle)
        m[p.a2.n, p.a2.n] = math.cos(angle)

        return Mx(m)
    
    @staticmethod
    def zeros_mx(length: int, height: int) -> Mx:
        return np.zeros((length, height))
    
    @staticmethod
    def identity_mx(length: int) -> Mx:
        return Mx(np.identity(length))

    @staticmethod
    def rand_mx(length: int, height: int, rrange: float = 1) -> Mx:
        m = np.zeros((length, height))

        for i in m:
            for j in i:
                j = np.random.normal(0, rrange, size=1)
        
        return m


class Array(Mx):

    def __init__(self, ms: list[float]):
        self.m = np.array(ms)

    def __str__(self) -> str:
        return f"Array: {self.m}"

    @staticmethod
    def cartesian_array(args: list[float]) -> Array:
        """Constructor for arrays in cartesian coordinates
        """
        return Array(np.array(args))

    @staticmethod
    def polar_array(args: list[float]) -> Array:
        """Constructor for arrays in polar coordinates
        """
        return Array(np.array(polar_to_decart(args) ))

    def scal(self) -> float:
        return np.linalg.norm(self.m, ord=2)

    def unitise(self) -> Array:
        return self.m / Array.scal(self.m)

    def rotation(self, angle: float, p: Plane, d: int = 3):
        """Method rotating Array

        Args:
            angle (float): rotation angle
            p (Plane): rotation plane
            d (int, optional): Number of diemensions. Defaults to 3.
        """
        self.m *= Mx.rotation_matrix(angle, p, d).m

    # Special things

    @staticmethod
    def zeros_arr(dimensions: int) -> Array:
        a = np.zeros((dimensions, 1))
        return Array(a)

    @staticmethod
    def randarr_fixed_length(lenght: float, dimensions: int = 3 ) -> Array:
        """Random array with fixed lenght
        """
        args: list[float] = [lenght]
        for i in range(1, dimensions):
            args.append(np.random.uniform(0.0, 2 * math.pi))
        
        return Array.polar_array(args)

    @staticmethod
    def randarr_less_than_lenght(lenght: float, dimensions: int = 3) -> Array:
        """Random array with lenght <= than given
        """
        r = np.random.uniform(0.0, lenght)
        args: list[float] = [r]
        for i in range(1, dimensions):
            args.append(np.random.uniform(0.0, 2 * math.pi))
        
        return Array.polar_array(args)