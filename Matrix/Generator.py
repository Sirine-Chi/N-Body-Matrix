import NBodyLib as nbl
import numpy as np

#config = open('System.txt', 'r')

objects = []
#center - vector
def spherical(N, center,  medium_radius, crit_radius_delta, medium_mass, crit_mass_delta, cen_velocity, vel_scal, vel_crit_delta):
    for i in range (1, N):
        st_der = crit_mass_delta/3
        objects.append([np.random.normal(medium_mass, st_der), center + nbl.ranvec(medium_radius), cen_velocity + nbl.ranvec(vel_scal)])
        #можно добавить дельту к medium_radius
    #print(*objects, sep = "\n")

def mass_vectors(objects):
    masses = []
    inv_masses = []
    for o in objects:
        masses.append(o[0])
        inv_masses.append(1/o[0])
    return [masses, inv_masses]
def position_matrix(objects):
    positions = []
    for o in objects:
        positions.append(o[1])
    return positions
def velocity_matrix(objects):
    velocities = []
    for o in objects:
        velocities.append(o[2])
    return velocities

def mass_matrix(ms):
    mx = []
    for i in ms:
        ln = []
        for j in ms:
            ln.append(i * j)
        mx.append(ln)
    #print(mx, 'mass matris')
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
    #print(mx, 'inv mass matrix')
    return nbl.v(mx)

def giveout(N, center,  medium_radius, crit_radius_delta, medium_mass, crit_mass_delta, cen_velocity, vel_scal, vel_crit_delta):
    spherical(N, center,  medium_radius, crit_radius_delta, medium_mass, crit_mass_delta, cen_velocity, vel_scal, vel_crit_delta)
    return [mass_matrix(mass_vectors(objects)[0]), mass_inv_matrix(mass_vectors(objects)[1]), nbl.v(position_matrix(objects)), nbl.v(velocity_matrix(objects))]