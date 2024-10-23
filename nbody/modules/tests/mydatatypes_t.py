from nbody.modules.core.mydatatypes import *

a = TubeList([4, 5, 6], depth=3)

test_dict = {
    "Tubelist = a": a,
    "len(a)": len(a),
    "a, after appending 7": a.append(7)
}

print(test_dict)

try:
    b = TubeList([3, 4, 5, 6, 7], depth=4)
except ValueError:
    print(f"list of 5 elements can't be initialised because of depth set to 4")


