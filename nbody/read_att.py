import markup_manager as mm
from mydatatypes import print_dict

def get_bodies(path) -> list(dict):
    result = mm.get_toml(path)["Bodies"]

    objects = []
    for key, obj in result.items():
        obj["Name"] = key
        objects.append(obj)

    return objects

path = 'nbody/system.toml'

for o in get_bodies(path):
    print_dict(o)
