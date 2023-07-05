import NBodyLib as nbl
import numpy as np
import sys

original_stdout = sys.stdout


# center - vector
def spherical(N, center, medium_radius, crit_radius_delta, medium_mass, crit_mass_delta, cen_velocity, vel_scal,
              vel_crit_delta):
    objects = []
    for i in range(0, N):
        st_der = crit_mass_delta / 3
        objects.append([str(i), np.random.normal(medium_mass, st_der), list(center + nbl.ranvec(medium_radius)),
                        list(cen_velocity + nbl.ranvec(vel_scal)), i, 'system', 'w'])
        # можно добавить дельту к medium_radius
    # print(*objects, sep = "\n")
    return objects


def spherical_sc(N, center, medium_radius, crit_radius_delta, medium_mass, crit_mass_delta, cen_velocity, vel_scal,
                 vel_crit_delta):
    objects = []
    type = "dynamic"
    for i in range(0, N):
        st_der = crit_mass_delta / 3
        objects.append(
            [str(type), str(i), np.random.normal(medium_mass, st_der), list(center + nbl.ranvec(medium_radius))[0],
             list(center + nbl.ranvec(medium_radius))[1], list(cen_velocity + nbl.ranvec(vel_scal))[0],
             list(cen_velocity + nbl.ranvec(vel_scal))[1], 'w', 0])
    print(*objects, sep="\n")
    return objects


def mass_vectors(objects):
    masses = []
    inv_masses = []
    for o in objects:
        masses.append(o[1])
        inv_masses.append(1 / o[1])
    return [masses, inv_masses]


def position_matrix(objects):
    positions = []
    for o in objects:
        positions.append(nbl.v(o[2]))
    return positions


def velocity_matrix(objects):
    velocities = []

    def vel(o):
        return nbl.v(o[3])

    for o in objects:
        velocities.append(nbl.v(o[3]))
    # return map(vel, objects)
    return velocities


def mass_matrix(ms):
    mx = []
    for i in ms:
        ln = []
        for j in ms:
            ln.append(i * j)
        mx.append(ln)
    # print(mx, 'mass matris')
    return nbl.v(mx)


def mass_inv_matrix(ms):
    mx = []
    for i in ms:
        ln = []
        for j in ms:
            if i == j:
                ln.append(j)
            if i != j:
                ln.append(0)
        mx.append(ln)
    # print(mx, 'inv mass matrix')
    return nbl.v(mx)


def write_objects(objects):  # Writes objects to System.txt
    with open('System.txt', 'w') as system:
        ps = []
        for p in objects:
            st = str(p)
            ps.append('obj_(' + st[1:-1] + ')')
        sys.stdout = system
        print(*ps, sep="\n")
    system.close()
    sys.stdout = original_stdout


def write_table(objects):
    names = ["Type", "Name", "Mass", "R x", "R y", "V x", "Vy", "Color", "Angle (Deg)"]  # str(type),
    tab = nbl.pd.DataFrame(data=objects)
    tab.to_csv('Table.csv', header=names, index=False)


def formatting(s):
    # print(*s, sep="\n")
    return [mass_matrix(mass_vectors(s)[0]), mass_inv_matrix(mass_vectors(s)[1]), nbl.v(position_matrix(s)),
            nbl.v(velocity_matrix(s))]
# По порядку: матрица произведений масс, матрица обратных масс, вектор координат системы, вектор скоростей системы
# если исполнить файл, то эта функция сгенирирует объекты заданных параметров

# Writing generated data to System.TXT
# write_objects(spherical(50, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))

# Writing generated data to System.CSV table
# write_table(spherical_sc(50, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))
