import inspect
def euler_improved(xs, ys, f:callable, h: float):
    requirement_depth = 1

    k1 = h*f(xs[-1], ys[-1])
    k2 = h*f(xs[-1]+h, ys[-1]+k1)
    return ys[-1] + (k1+k2)/2

# def two_step(x_n, y_n, y_n_, f:callable, h: float):
#     """
#     Euler's Improved nm

#     Args:
#         x_n (MATH): previous X
#         y_n (MATH): previous Y
#         y_n_ (MATH): previous previous Y
#         f (callable): function f(x_n, y_n)
#         h (float): step dx

#     Returns:
#         MATH: returns x_n type
#     """
#     requirement_depth = 2
#     return y_n_ + 2*h*f(x_n, y_n)

# each method has requirement_depth, to check, if there's enough values

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
    def dec(func: callable):
        return Method(order, func)
    return dec

# --- --- --- METHOD OBJECT CREATION

@new_method(order=1)
def euler(xs, ys, f: callable, h: float):
    return xs[-1] + h*f(xs[-1], ys[-1])/2

# --- --- --- USAGE

def exf(x, y):
    return x + y

print(f"euler_obj: {euler}, euler_ars: {euler(xs=[0], ys=[2], f=exf, h=0.1 )}")

# print( f"\033[1mMethod instance __str__: \033[0m \n{euler}\n\033[1mMethod: \033[0m {euler(xs=[0], ys=[2], f=exf, h=0.1)}, \033[1m \nFunc: \033[0m {euler_f(xs=[0], ys=[2], f=exf, h=0.1)}" )
