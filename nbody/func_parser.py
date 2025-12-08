import sympy
import mylinal as l

expression = "f1 = G * mass_1 * mass_2 * (r_1 - r_2) / scal(r1 - r2)**3"

def find_var(vars: dict, key: str) -> dict:
    """Returns a key-value pair, if there's exactly one kein dict.

    Args:
        vars (dict): to search in
        key (str): key to find

    Raises:
        KeyError: If there's a dublicate value

    Returns:
        dict: key-value pair
    """
    if key in vars.keys():
        try:
            vars.pop(key)
        except KeyError:
            return {key: vars[key]}
        raise KeyError("There's a dublicate value")

def parse_func(expression: str) -> callable:
    expression = expression.replace(" ", "")
    pass

def parse_all(all_expressions: list[str]) -> dict:
    funcs = {}
    for expr in all_expressions:
        funcs.update( {expr: parse_func(expr)} )
    return funcs

constants = {
    "G": 1
}

std_bindings = {
    "r": "position",
    "v": "velocity",
    "a": "acceleration",
    "f": "force"
}

class Particle:
    mass = 1
    position = l.Array([0.1, 0.2])
    velocity = l.Array([0.1, 0.2])
    acceleration = l.Array([0.1, 0.2])
    force: l.Array

p = Particle

# ---- TEST ----
print(parse_func(expression))
