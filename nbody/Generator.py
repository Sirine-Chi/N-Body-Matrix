import sys

import n_body_lib as nbl
import numpy as np


# center - vector
def spherical(
    N,
    center,
    medium_radius,
    crit_radius_delta,
    medium_mass,
    crit_mass_delta,
    cen_velocity,
    vel_scal,
    vel_crit_delta,
):
    objects = []
    for i in range(0, N):
        st_der = crit_mass_delta / 3
        objects.append(
            [
                str(i),
                np.random.normal(medium_mass, st_der),
                list(center + nbl.ranvec(medium_radius)),
                list(cen_velocity + nbl.ranvec(vel_scal)),
                i,
                "system",
                "w",
            ]
        )
        # можно добавить дельту к medium_radius
    # print(*objects, sep = "\n")
    return objects


def spherical_sc(
    N,
    center,
    medium_radius,
    crit_radius_delta,
    medium_mass,
    crit_mass_delta,
    cen_velocity,
    vel_scal,
    vel_crit_delta,
):
    objects = []
    type = "dynamic"
    for i in range(0, N):
        st_der = crit_mass_delta / 3
        objects.append(
            [
                str(type),
                str(i),
                np.random.normal(medium_mass, st_der),
                list(center + nbl.ranvec(medium_radius))[0],
                list(center + nbl.ranvec(medium_radius))[1],
                list(cen_velocity + nbl.ranvec(vel_scal))[0],
                list(cen_velocity + nbl.ranvec(vel_scal))[1],
                "w",
                0,
            ]
        )
    print(*objects, sep="\n")
    return objects


def write_table(objects):
    names = [
        "Type",
        "Name",
        "Mass",
        "R x",
        "R y",
        "V x",
        "Vy",
        "Color",
        "Angle (Deg)",
    ]  # str(type),
    tab = nbl.pd.DataFrame(data=objects)
    tab.to_csv("Table.csv", header=names, index=False)


# Writing generated data to System.TXT
# write_objects(spherical(50, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))

# Writing generated data to System.CSV table
# write_table(spherical_sc(50, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))
