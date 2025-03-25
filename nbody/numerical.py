"""
Numerical methods module

Has class, which contains order checking logic and string representations
Has some methods, new methods can be declared there
"""

import inspect

class Method:
    def __init__(self, order: int, func: callable):
        self.order = order
        self.func = func

    def __str__(self):
        return f"\033[31mName:\033[0m {str(self.__class__.__name__).lower()},\n\033[31mFunc:\033[0m \n{inspect.getsource(self.func)}"

    def __call__(self, xs, ys, f: callable, h: float):
        self.xs = xs
        self.ys = ys
        if self.check_depth():
            return self.func(xs, ys, f, h)

    def check_depth(self):
        if len(self.xs) >= self.order and len(self.ys) >= self.order:
            return True
        else:
            raise IndexError(f"Method require depth {self.order},but len xs={len(self.xs)}, len ys={len(self.ys)} < {self.order}")

def new_method(order: int):
    """
    Numerical Method decorator factory

    Args:
        order (int): method order
    Returns:
        Callable: method function
    """
    
    def dec(func: callable):
        return Method(order, func)
    return dec

# --- --- --- METHOD OBJECT CREATION
# to add new method, just add @new_method(order:int) decorator =)

@new_method(order=1)
def euler(xs:list, ys:list, f: callable, h: float):
    """Euler method

    Args:
        xs (list): _description_
        ys (list): _description_
        f (callable): function
        h (float): step

    Returns:
        _type_: _description_
    """
    return xs[-1] + h*f(xs[-1], ys[-1])/2

@new_method(order=1)
def euler_improved(xs:list, ys:list, f: callable, h: float):
    """
    (Euler)[https://en.wikipedia.org/wiki/Euler_method]

    Args:
        x_n (MATH): previous Xs list
        y_n (MATH): previous Ys list
        f (callable): function f(x_n, y_n)
        h (float): step dx

    Returns:
        MATH: returns x_n type
    """
    k1 = h*f(xs[-1], ys[-1])
    k2 = h*f(xs[-1]+h, ys[-1]+k1)
    return ys[-1] + (k1+k2)/2

@new_method(order=2)
def two_step(xs: list, ys: list, f: callable, h: float):
    """
    (Two step nm)[]

    Args:
        x_n (MATH): previous Xs list
        y_n (MATH): previous Ys list
        f (callable): function f(x_n, y_n)
        h (float): step dx

    Returns:
        MATH: returns x_n type
    """
    return ys[-2] + 2*h*f(xs[-1], ys[-1])

@new_method(order=1)
def adams(xs: list, ys: list, f: callable, h:float):
    return xs[-1] + h * 3 / 2 * ys[-1] - h /2 * ys[-2]

# --- --- --- TESTING

# def exf(x, y):
#     return x + y

# print(f"euler_obj: {euler}, euler_ars: {euler(xs=[0], ys=[2], f=exf, h=0.1 )}")

# print( f"\033[1mMethod instance __str__: \033[0m \n{euler}\n\033[1mMethod: \033[0m {euler(xs=[0], ys=[2], f=exf, h=0.1)}, \033[1m \nFunc: \033[0m {euler_f(xs=[0], ys=[2], f=exf, h=0.1)}" )
