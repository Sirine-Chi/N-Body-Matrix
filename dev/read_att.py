import markup_manager as mm
from mydatatypes import print_dict, color4f

def get_bodies(path) -> list[dict]:
    result = mm.get_toml(path)["Bodies"]

    objects = []
    for key, obj in result.items():
        obj["Name"] = key
        objects.append(obj)

    return objects

path = 'nbody/system.toml'

# for o in get_bodies(path):
#     print_dict(o)

clr = color4f(0.0, 0.1, 0.5)
print(clr.c)
