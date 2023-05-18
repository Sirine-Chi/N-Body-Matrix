import numpy as np
import array
import pandas as pd
import math
import Visualise as Vis
#import Generator as gen
from random2 import uniform
from random2 import triangular
from random2 import getrandbits
from random2 import randint
import datetime
import time

def scal(v): #Модуль (скаляр, длиннна) вектора
    return (v[0]**2 + v[1]**2)**0.5
def a(v1):
    return array.array('f', v1)
def v(v1): #вектор
    return np.array(v1)
def unvec(v): #еденичный вектор
    return v/scal(v)
def dist(v1, v2): #расстояние между двумя точками (концами векторов v1 и v2)
    return scal(v1-v2)
def v12(v1, v2):
    return (v2-v1)
def ranvec(r): #Случайный радиус-вектор длинны r
    rv = v(  [uniform(-r, r), 2*(getrandbits(1)-0.5) *(r**2 - uniform(-r, r)**2)**0.5]  )
    return rv
def ranrv(r): #Случайный радиус-вектор длинны r
    a = uniform(0, 2*math.pi)
    rr = uniform(0, r)
    rv = v( [rr*math.cos(a), rr*math.sin(a)]  )
    return rv
def vsum(v_list):
    vl=[]
    for l in range(0, len(v_list[0]) ):
        vli=[]
        for i in v_list:
            vli.append(i[l])
        vl.append(sum(vli))
        l+=1
    # vlx=[]
    # for i in v_list:
    #     vlx.append(i[0])
    # vly=[]
    # for i in v_list:
    #     vly.append(i[1])
    return v(vl) #сумма n-мерных векторов
def dsum(v_list):
    vlx=[]
    for i in v_list:
        vlx.append(i[0])
    vly=[]
    for i in v_list:
        vly.append(i[1])
    return v([sum(vlx), sum(vly)]) #сумма двумерных векторов

#CONSTANTS
G = 0.0001184069#09138
#ДОБАВИТЬ КОНСТАНТЫ ДЛЯ ПЕРЕВОДА? ПОДКЛЮЧИТЬ СИ ТАБЛИЦУ И ПЕРЕВОДИТЬ

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
def U(coor, system, n): #потенциал, создаваемый всеми в точке coor /на шаге n
    c_us = []
    for obj in system:
        c_us.append(u_ob(coor, obj, n))
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

def simul(method, objects, N, dir, end, dt, delta_cur, inum, pulse_table, field):
    simulation_time = time.time()
    enn = int(end/dt)
    dt = dir*dt
    class Object:
        def f12(obj1, obj2, n):  # силa, действующая на 1 от 2
            f12 = v(
                unvec(obj2.r[n - 1] - obj1.r[n - 1]) * obj1.m * obj2.m * G / (dist(obj2.r[n - 1], obj1.r[n - 1]) ** 2))
            return f12
        def f(obj, system, n):
            obj.fn = []
            for other in system:
                if obj != other:
                    obj.fn.append(f12(obj, other, n))
            return dsum(obj.fn)
        def __init__(self, m, r0, v0, i, system, colour, *args, **kwargs):
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
            self.f.append( Object.f(self, system, 1) )
            if pulse_table == True:
                self.Ps = []
                self.Ps.append(v(  self.v[0]*self.m  ))

            #FOR ADAMS
            self.r.append(v(self.r[0]+dt*self.v[0]))
            self.v.append(v(self.v[0]+dt*self.f[0]/self.m))
            self.t.append(1)
            self.f.append( Object.f(self, system, 2) )

            if pulse_table == True:
                self.Ps.append(v(  self.v[1]*self.m  ))

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
        def reper(self, n):
            self.r[n] = self.r[n] - system[0].r[n]

        def iteration(self, system, n, dt):
            def f12(obj1, obj2, n): #силa, действующая на 1 от 2
                return v( unvec(obj2.r[n-1]-obj1.r[n-1]) * obj1.m*obj2.m*G / (dist(obj2.r[n-1], obj1.r[n-1])**2) )
            def f(obj, system, n):
                obj.fn=[]
                for other in system:
                    if obj != other:
                        obj.fn.append(f12(obj, other, n))
                return dsum(obj.fn)
                obj.fn.clear()

            self.t.append(self.t[n-1]+dt)
            self.f.append(f(self, system, n))
            if method == 'Eiler':
                #self.v.append(v( self.v[n-1] +dt/2*))
                self.v.append(v( self.v[n-1]+dt*self.f[n-1]/self.m )) # Eiler
            elif method == 'Eiler_Reverse':
                self.v.append(v( self.v[n-1]+dt*self.f[n-1]/self.m )) # Eiler anvis
            # elif method == 'W':
            #     self.v.append(v( self.v[n-1] +dt*(self.f[n]/self.m+ ) ))
            elif method == 'Midpoint':
                self.v.append(v( self.v[n-1]+ dt*f( self.r[n-1]+ dt/2*f(self.r[n-1]) )/self.m )) # Midpoint
            elif method == 'Adams':
                self.v.append(v( self.v[n-1] + dt/2*( 3*self.f[n]/self.m - self.f[n-1]/self.m) )) # Adams

            if pulse_table == True:
                self.Ps.append(v(  self.v[n]*self.m  ))

            if method == 'Eiler':
                self.r.append(v( self.r[n-1]+dt*self.v[n])) #Eiler
            #self.r[n] = self.r[n] - galaxy[0].r[n]
            elif method == 'Midpoint':
                self.r.append(v( self.r[n-1]+ dt/2*(self.v[n-1]+self.v[n-2]) )) #midpoint
            elif method == 'Adams':
                self.r.append(v( self.r[n-1] + dt/2*(3*self.v[n-1] - self.v[n-2]) )) # Adams

            # if n > 3:
            #     del self.r[0]

    class object(Object):
        pass

    system = []
    for ob in objects:
        system.append(object(ob[1], ob[2]+ranrv(delta_cur), ob[3], ob[4], system, ob[6].replace("'", '')))

    #---Iterator---
    for n in range (2, enn):
        for ss in system:
            ss.iteration(system, n, dt)
            ss.reper(n)

    # ---PULSE TABLE---
    if pulse_table == True:
        def Pn(system, n):
            ps = []
            for ob in system:
                ps.append(ob.Ps[n-1])
            return scal(dsum(ps))
        PS = [] #Добавляем в список значения полного импульса с итераций
        for n in range (0, enn):
            PS.append(Pn(system, n))

        tP = pd.DataFrame(
            {
                "t":system[0].t,
                "P":PS
            } )
        tP.to_csv('tP.csv')

        print(PS[1] - PS[-1])

    print('sim num= '+ str(inum)+' ', 'delta= '+ str(delta_cur)+' ')

    print('Finished!', 'simulation time')
    print("--- %s seconds ---" % (time.time() - simulation_time))

    Vis.vis_N_2D(system, inum, delta_cur)
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
