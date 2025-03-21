from __future__ import annotations
import math
import numpy as np
from mymath import Plane, Angle, polar_to_decart
# from random import randrange
from mydatatypes import timer

# parentness: Mx -> arr? -> 3d -> 2d

class Mx:
    """
    Matrix class
    """

    def __init__(self, ms : np.array):
        """Matrix constructor
        """
		
        self.m : np.array = ms

    # class NonMxTypeError(TypeError):
    #     def __init__(self, msg="Not a linal.Mx type"):
    #         self.msg = msg
    #         super().__init__(self.msg)

    @staticmethod
    def new_mx_from_list( m: list):
        return Mx(np.array(m))

    def give_tuple(self):
        return tuple(self.m.tolist())

    # print
    def __str__(self) -> str:
        return f"Matrix: {self.m.tolist()}"

    def __repr__(self) -> str:
        return f"Array: {self.m.tolist()}"

    def len(self) -> int:
        return f"{self.m.size()}"


	# +
    def __add__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(self.m + other.m)
        else:
            return Mx(self.m + other)

    # +=
    def __iadd__(self, other) -> None:
        if isinstance(other, Mx):
            self.m = self.m + other.m
        else:
            self.m = self.m + other

    # -
    def __sub__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(self.m - other.m)
        else:
            return Mx(self.m - other)

    # dot product
    def __mul__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(np.dot(self.m, other.m))
        else:
            try:
                return Mx(np.dot(self.m, other))
            except TypeError:
                print("Oops! Not a matrix type")
                # FIXME do something with cringy prints
        #     #     raise Mx.NonMxTypeError

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if other != 0:
            return self.__mul__(1/other)
        else:
            raise ArithmeticError

    # hadamar %
    def __mod__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(np.multiply(self.m, other.m))
        else:
            try:
                return Mx(np.multiply(self.m, other))
            except TypeError:
                print("Oops! Not a matrix type")
            #     raise Mx.NonMxTypeError

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
        return f"Array: {self.m.tolist()}"
    
    def __repr__(self) -> str:
        return f"Array: {self.m.tolist()}"

    def len(self) -> int:
        return f"{self.m.size()}"

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
    
    @staticmethod
    def scal(v: Array) -> float:
        return np.linalg.norm(v.m, ord=2)

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

# class LinalTest:

#     ap = np.array( ((0.7, 1.2), (3.0, 4.0)) )
#     bp = np.array( ((1.0, 2.0), (0.1, 0.3)) )

#     a = Mx(ap)
#     b = Mx(bp)

#     @timer
#     def test_add(self):
#         print(self.a + self.b)
    

# lt = LinalTest()
# lt.test_add()

# ap = np.array( ((0.7, 1.2), (3.0, 4.0)) )
# bp = np.array( ((1.0, 2.0), (0.1, 0.3)) )

# cl =  np.array( (0.7, 1.2) )

# a = Mx(ap)
# b = Mx(bp)
# c = Array(cl)
# # print(np.dot(0, c.m))
# print(a*0)
# # print(Array.__mul__)