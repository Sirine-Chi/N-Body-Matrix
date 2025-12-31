from __future__ import annotations
import math
import torch
from mymath import Plane, Angle, polar_to_decart
from mydatatypes import timer
import numpy as np

# Global device configuration for GPU acceleration
DEVICE = torch.device("mps" if torch.mps.is_available() else "cpu")
print(f"Using device: {DEVICE}")

class Mx:
    """
    Matrix class using PyTorch for GPU acceleration
    """

    def __init__(self, ms: torch.Tensor):
        """Matrix constructor - ensures data is on the correct device"""
        if not isinstance(ms, torch.Tensor):
            ms = torch.tensor(ms, device=DEVICE, dtype=torch.float32)
        else:
            ms = ms.to(DEVICE)
        self.m: torch.Tensor = ms

    @staticmethod
    def new_mx_from_list(m: list):
        return Mx(torch.tensor(m, device=DEVICE, dtype=torch.float32))

    def give_tuple(self):
        # Move to CPU before converting to list/tuple
        return tuple(self.m.cpu().tolist())

    # print
    def __str__(self) -> str:
        return f"Matrix: {self.m.cpu().tolist()}"

    def __repr__(self) -> str:
        return f"Array: {self.m.cpu().tolist()}"

    def len(self) -> int:
        # numel() is the PyTorch equivalent of size
        return f"{self.m.numel()}"

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

    # dot product (Matrix Multiplication)
    def __mul__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(torch.matmul(self.m, other.m))
        else:
            try:
                # Handles scalar multiplication or tensor multiplication
                return Mx(self.m * other)
            except TypeError:
                print("Oops! Not a matrix type")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if other != 0:
            return self.__mul__(1/other)
        else:
            raise ArithmeticError

    # hadamard product
    def __mod__(self, other) -> Mx:
        if isinstance(other, Mx):
            return Mx(torch.mul(self.m, other.m))
        else:
            try:
                return Mx(torch.mul(self.m, other))
            except TypeError:
                print("Oops! Not a matrix type")

    # transpose
    def transpose(self) -> Mx:
        return Mx(self.m.t())
    
    @staticmethod
    def rotation_matrix(angle: Angle, p: Plane, d: int = 3) -> Mx:
        m = torch.zeros((d, d), device=DEVICE)
        m[p.a1.n, p.a1.n] = math.cos(angle)
        m[p.a1.n, p.a2.n] = -1*math.sin(angle)
        m[p.a2.n, p.a1.n] = math.sin(angle)
        m[p.a2.n, p.a2.n] = math.cos(angle)
        return Mx(m)
    
    @staticmethod
    def zeros_mx(length: int, height: int) -> Mx:
        return Mx(torch.zeros((length, height), device=DEVICE))
    
    @staticmethod
    def identity_mx(length: int) -> Mx:
        return Mx(torch.eye(length, device=DEVICE))

    @staticmethod
    def rand_mx(length: int, height: int, rrange: float = 1) -> Mx:
        # PyTorch normal distribution
        m = torch.normal(0, rrange, size=(length, height), device=DEVICE)
        return Mx(m)


class Array(Mx):

    def __init__(self, ms: list[float] | torch.Tensor):
        if isinstance(ms, torch.Tensor):
            self.m = ms.to(DEVICE)
        else:
            self.m = torch.tensor(ms, device=DEVICE, dtype=torch.float32)

    def __str__(self) -> str:
        return f"Array: {self.m.cpu().tolist()}"
    
    def __repr__(self) -> str:
        return f"Array: {self.m.cpu().tolist()}"

    def len(self) -> int:
        return f"{self.m.numel()}"

    @staticmethod
    def cartesian_array(args: list[float]) -> Array:
        return Array(torch.tensor(args, device=DEVICE))

    @staticmethod
    def polar_array(args: list[float]) -> Array:
        return Array(torch.tensor(polar_to_decart(args), device=DEVICE))
    
    @staticmethod
    def scal(v: Array | Mx | torch.Tensor) -> float:
        # If it's our custom class, extract the underlying tensor
        if hasattr(v, 'm'):
            tensor = v.m
        else:
            tensor = v
            
        # Ensure it is a tensor for the PyTorch function
        return torch.linalg.vector_norm(tensor, ord=2).item()

    def unitise(self) -> Array:
        return Array(self.m / Array.scal(self))

    def rotation(self, angle: float, p: Plane, d: int = 3):
        # We perform matrix multiplication to apply rotation
        rot_mx = Mx.rotation_matrix(angle, p, d).m
        self.m = torch.matmul(rot_mx, self.m)

    @staticmethod
    def zeros_arr(dimensions: int) -> Array:
        a = torch.zeros((dimensions, 1), device=DEVICE)
        return Array(a)

    @staticmethod
    def randarr_fixed_length(lenght: float, dimensions: int = 3 ) -> Array:
        args: list[float] = [lenght]
        for i in range(1, dimensions):
            # Using torch's uniform generator
            args.append(torch.empty(1).uniform_(0.0, 2 * math.pi).item())
        return Array.polar_array(args)

    @staticmethod
    def randarr_less_than_lenght(lenght: float, dimensions: int = 3) -> Array:
        r = torch.empty(1).uniform_(0.0, lenght).item()
        args: list[float] = [r]
        for i in range(1, dimensions):
            args.append(torch.empty(1).uniform_(0.0, 2 * math.pi).item())
        return Array.polar_array(args)