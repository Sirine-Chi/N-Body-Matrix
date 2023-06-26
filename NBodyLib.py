import numpy as np
import pyopencl as cl
#import gnumpy as gpu
import pandas as pd
import math
import Visualise as Vis
import random2 as rnd
import datetime
import time

def scal(v): #Модуль (скаляр, длиннна) вектора
    return np.linalg.norm(v, 2, None, False)
def v(v1): #вектор
    return np.array(v1)
def unvec(v): #еденичный вектор
    uv = v / scal(v)
    return uv
def dist(v1, v2): #расстояние между двумя точками (концами векторов v1 и v2)
    return scal(v1-v2)
def v12(v1, v2):
    return (v2-v1)
def ranvec(r): #Случайный радиус-вектор длинны r
    rv = v(  [rnd.uniform(-r, r), 2*(rnd.getrandbits(1)-0.5) *(r**2 - rnd.uniform(-r, r)**2)**0.5]  )
    return rv
#TODO: use distribution!
def ranrv(r): #Случайный радиус-вектор длинны r
    a = rnd.uniform(0, 2*math.pi)
    rr = rnd.uniform(0, r)
    rv = v( [rr*math.cos(a), rr*math.sin(a)]  )
    return rv
def vsum(v_list):
    return sum(v_list) #сумма N-мерных векторов
def rotvec(v, al):
    return [ v[0]*math.cos(math.radians(al)), v[1]*math.sin(math.radians(al))]
def format_table(system):
    lines = []
    for line in system.to_numpy():
        lines.append( [line[1].replace(' ', ''), line[2], v([line[3], line[4]]), v([line[5], line[6]]), line[7].replace(' ', ''), line[8]] )
    # print(*lines, sep='\n')
    return lines

# CONSTANTS
G = 0.0001184069#09138
# ДОБАВИТЬ КОНСТАНТЫ ДЛЯ ПЕРЕВОДА? ПОДКЛЮЧИТЬ СИ ТАБЛИЦУ И ПЕРЕВОДИТЬ

def net(step):
    dots = []
    for x in range(-10, 10):
        for y in range(-10, 10):
            dots.append([x, y])
            y += step
        x += step
    return dots
def u_ob(coor, obj, n): #coor - vector, obj1 - Star, потенциал, создаваемый телом obj1 в точке coor / на шаге n
    u_ob = G*obj.m / dist(coor, obj.r[n])
    return u_ob
def U(coor, galaxy, n): #потенциал, создаваемый всеми в точке coor /на шаге n
    c_us = []
    for obj in galaxy:
        c_us.append(u(coor, obj, n))
    U = sum(c_us)
    return U
def u_in_net(system, n, step):
    U_s = []
    U_3d_s = []
    net_dots = net(step)
    for coor in net_dots:
        U_s.append(U(coor, system, n))
        U_3d_s.append([coor[0], coor[1], U(coor, system, n)])
    return U_s
def f12(obj1, obj2, n):  # силa, действующая на 1 от 2
    return v(unvec(obj2.r[n - 1] - obj1.r[n - 1]) * obj1.m * obj2.m * G / (dist(obj2.r[n - 1], obj1.r[n - 1]) ** 2))
def f(obj, system, n):
    obj.fn = []
    for other in system:
        if obj != other:
            obj.fn.append(f12(obj, other, n))
    return vsum(obj.fn)
    obj.fn.clear()

def simul(method, objects, N, dir, end, dt, delta_cur, inum, pulse_table, field):
    simulation_time = time.time()
    enn = int(end/dt)
    dt = dir*dt
    class Object:
        def __init__(self, m, r0, v0, i, system, colour, *args, **kwargs): #ПРОБЛЕМА мы берём коррдинаты ещё неинициализированных объектов
            self.colour = colour
            self.m = m
            self.r0 = r0
            self.v0 = v0
            self.i = i
            self.r = []
            self.v = []
            self.f = []
            self.t = []

            self.r.append(v(r0))
            self.v.append(v(v0))
            self.t.append(0)
            self.f.append( f(self, system, 1) )

            #FOR ADAMS
            self.r.append(v(self.r[0]+dt*self.v[0]))
            self.v.append(v(self.v[0]+dt*self.f[0]/self.m))
            self.t.append(1)
            self.f.append( f(self, system, 2) )

            if pulse_table == True:
                self.Ps = []
                self.Ps.append(v(self.v[0] * self.m))
                self.Ps.append(v(  self.v[1]*self.m  ))

            if field == True:
                inum = 'f'
                delta_cur = 0
                Vis.vis_field(system, 0, inum, delta_cur) #0 is case of n

        def print_object(self):
            print("id="+str(self.i), self.m, "f"+str(self.f), "v"+str(self.v), "r"+str(self.r), "t"+str(self.t))
        def print_object_coor(self):
            print("id="+str(self.i), self.r)
        def makeXY(obj):
            # devider = 1
            # devider = int(devider)
            x_s0=[]
            y_s0=[]
            for i in obj.r:
                x_s0.append(i[0])
                y_s0.append(i[1])
                # x_s0 = x_s0[::devider]
                # y_s0 = y_s0[::devider]
            return [x_s0, y_s0]

        def iteration(self, system, n, dt):

            def eiler_method(fs, vs, rs, m):
                vs.append(v(vs[n-1] + dt * fs[n - 1] / m))  # Eiler
                rs.append(v(rs[n-1] + dt * vs[n]))
            def midpoint_method(f, v, r, m):
                v.append(v(v[n-1] + dt * f(r[n-1] + dt/2 * f(r[n-1]))/m))  # Midpoint
                r.append(v(r[n-1] + dt/2 * (v[n-1] + v[n-2])))
            def adams_method(f, v, r, m):
                v.append(v( v[n-1] + dt/2*(3*f[n]/m - f[n-1]/m)))  # Adams
                r.append(v( r[n-1] + dt/2*(3*v[n] - v[n-1])))

            self.t.append(self.t[n-1]+dt)
            self.f.append(f(self, system, n))

            eiler_method(self.f, self.v, self.r, self.m)

            if pulse_table == True:
                self.Ps.append(v(  self.v[n]*self.m  ))

        def reper(self, n):
            self.r[n] = self.r[n] - system[0].r[n]

    class object(Object):
        pass

    system = []
    for ob in objects:
        system.append(object( ob[1], ob[2], ob[3], ob[4], system, ob[6].replace("'", '') ))

    #--define function for pulse---
    if pulse_table == True:
        def Pn(system, n):
            ps = []
            for ob in system:
                ps.append(ob.Ps[n-1])
            return scal(vsum(ps))

    #---Iterator---
    for n in range (2, enn):
        #dtn = dt #FOR DYNAMIC TIME STEP!!!
        # Star.iter(system, n, dt)
        for ss in system:
            ss.iteration(system, n, dt)
            ss.reper(n)
            #ss.printstar() #вывести всё про точку

    # ---PULSE TABLE---
    if pulse_table == True:
        PS = [] #Добавляем в список значения полного импульса с итераций
        for n in range (0, enn):
            PS.append(Pn(galaxy, n))

        tP = pd.DataFrame(
            {
                "t":galaxy[0].t,
                "P":PS
            } )
        tP.to_csv('tP.csv')

        print(PS[1] - PS[-1])

    print('sim num= '+ str(inum)+' ', 'delta= '+ str(delta_cur)+' ')

    print('Finished!', 'simulation time')
    print("--- %s seconds ---" % (time.time() - simulation_time))

    #Vis.vis_N_2D(system, inum, delta_cur)

    #Vis.vis_N_3D(galaxy).show
    #Vis.vis_N_anim(galaxy, enn).save('Galaxy.gif', writer='imagemagic', fps=60)

def progons(method, objects, N, dir, end, dt, delta_step, k, delta_start, delta_end, pulse_table):
    progons_global_time = time.time()

    delta_cur = delta_start
    while delta_cur <= delta_end:
        for inum in range (0, k):
            simul(method, objects, N, dir, end, dt, delta_cur, inum, pulse_table, 0)
        delta_cur = float(delta_cur) + delta_step

    print('progons_global_time')
    print("--- %s seconds ---" % (time.time() - progons_global_time))

def openCL_mult(matrix1, matrix2):
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
    b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix1.nbytes)

    prg = cl.Program(ctx, """
        __kernel void multiplymatrices(const unsigned int size, __global float * matrix1, __global float * matrix2, __global float * res) {

        int i = get_global_id(1); 
        int j = get_global_id(0);

        res[i + size * j] = 0;

        for (int k = 0; k < size; k++)
        {
            res[i + size * j] += matrix1[k + size * i] * matrix2[j + size * k];
        }

        }
        """).build()
    # res[i + size * j] += matrix1[i + size * k] * matrix2[k + size * j];

    t0 = datetime.datetime.now()

    prg.multiplymatrices(queue, matrix1.shape, None, np.int32(len(matrix1)), a_buf, b_buf, dest_buf)

    final_matrix = np.empty_like(matrix1)
    cl.enqueue_copy(queue, final_matrix, dest_buf)

    #print(final_matrix)

    delta_t = datetime.datetime.now() - t0
    print('OpenCL Multiplication: ' + str(delta_t))

    return final_matrix

def np_mult(matrix1, matrix2): # =m1 x m2, порядок как в письме
    return matrix1.dot(matrix2)
    # return np.matmul(matrix1, matrix2)