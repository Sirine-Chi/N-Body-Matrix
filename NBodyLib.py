import numpy as np
import pandas as pd
import math
import Visualise as Vis
import Generator as gen
from random2 import uniform
from random2 import triangular
from random2 import getrandbits
from random2 import randint
import datetime
import time

def scal(v): #Модуль (скаляр, длиннна) вектора
    return (v[0]**2 + v[1]**2)**0.5
def v(v1): #вектор
    v = np.array(v1)
    return v
def unvec(v): #еденичный вектор
    uv = v / scal(v)
    return uv
def dist(v1, v2): #расстояние между двумя точками (концами векторов v1 и v2)
    return scal(v1-v2)
def v12(v1, v2):
    return (v2-v1)
def v12(v2, v1):
    return (v1-v2)
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

# N = 4
#Parametries
# dur = 1
# end = 4.5*(10**2) #4.5*10**9
# dt = dur * 1*10**-4 #10**-4
#
# pulse_table = False
# inum = 's'

def simul(objects, N, dur, end, dt, delta_cur, inum, pulse_table):
    simulation_time = time.time()
    enn = int(end/dt)
    class Star:
        def __init__(self, m, r0, v0, i, galaxy, col, *args, **kwargs): #ПРОБЛЕМА мы берём коррдинаты ещё неинициализированных объектов
            self.col = col
            self.m = m
            self.r0 = r0
            self.v0 = v0
            self.i = i
            self.r = []
            self.v = []
            self.a = []
            self.f = []
            self.t = []
            if pulse_table == True:
                self.Ps = []
            self.r.append(v(r0))
            self.v.append(v(v0))
            self.t.append(0)
            self.f0s=[]
            for other in galaxy:
                if self.i != other.i:
                    #self.f0s.append(v(   -unvec(other.r[0]- self.r[0])*( dist(other.r[0], self.r[0])**(-6) - dist(other.r[0], self.r[0])**(-12))  ))
                    self.f0s.append(v( unvec(other.r[0]-self.r[0]) * (self.m*other.m*G / dist(other.r[0], self.r[0])**2) ))
            self.f.append(dsum(self.f0s))
            self.a.append(self.f[0]/self.m)
            if pulse_table == True:
                self.Ps.append(v(  self.v[0]*self.m  ))

            #FOR ADAMS
            self.r.append(v(self.r[0]+dt*self.v[0]))
            self.v.append(v(self.v[0]+dt*self.a[0]))
            self.t.append(1)
            self.f1s=[]
            for oth in galaxy:
                if self.i != oth.i:
                    self.f1s.append(v( unvec(oth.r[1]-self.r[1]) * (self.m*oth.m*G / dist(oth.r[1], self.r[1])**2) ))
            self.f.append(dsum(self.f1s))
            self.a.append(self.f[1]/self.m)
            if pulse_table == True:
                self.Ps.append(v(  self.v[1]*self.m  ))

        def printstar(self):
            print("id="+str(self.i), self.m, "f"+str(self.f), "v"+str(self.v), "r"+str(self.r), "t"+str(self.t))
        def print_s_cor(self):
            print("id="+str(self.i), self.r)
        def makeXY(self):
            # devider = 1
            # devider = int(devider)
            x_s0=[]
            y_s0=[]
            for i in galaxy[self.i].r:
                x_s0.append(i[0])
                y_s0.append(i[1])
                # x_s0 = x_s0[::devider]
                # y_s0 = y_s0[::devider]
            return [x_s0, y_s0]

        def iter(self, galaxy, n, dt, i):
            self.t.append(self.t[n-1]+(dt*dur))
            def f(r):
                self.fn=[]
                for ot in galaxy:
                    if self.i != ot.i:
                        self.fn.append(v( unvec(ot.r[n-1]-self.r[n-1]) * (self.m*ot.m*G / dist(ot.r[n-1], self.r[n-1])**2) ))
                        #self.fn.append(v(   -unvec(ot.r[n-1]- self.r[n-1])*(dist(ot.r[n-1], self.r[n-1])**-6 - dist(ot.r[n-1], self.r[n-1])**-12)  ))
                return dsum(self.fn)
            self.f.append(f(self.r[n-1]))
            self.a.append(self.f[n]/self.m)
            self.v.append(v( self.v[n-1]+dt*self.a[n] )) # Eiler
            #self.v.append(v( self.v[n-1]+dt*self.a[n-1] )) # Eiler anvis
            #self.v.append(v( self.v[n-1]+ dt*f( self.r[n-1]+ dt/2*f(self.r[n-1]) )/self.m )) # Midpoint
            #self.v.append(v( self.v[n-1] + dt/2*(3*self.a[n-1] - self.a[n-2]) )) # Adams
            if pulse_table == True:
                self.Ps.append(v(  self.v[n]*self.m  ))
            self.r.append(v( self.r[n-1]+dt*self.v[n])) #Eiler
            #self.r[n] = self.r[n] - galaxy[0].r[n]
            #self.r.append(v( self.r[n-1]+ dt/2*(self.v[n-1]+self.v[n-2]) )) #midpoint
            #self.r.append(v( self.r[n-1] + dt/2*(3*self.v[n-1] - self.v[n-2]) )) # Adams

            # if n > 3:
            #     del self.r[0]

        def reper(self, n):
            self.r[n] = self.r[n] - galaxy[0].r[n]

    class star(Star):
        pass

    galaxy = []
    #galaxy = gen.SS03(galaxy)
    for ob in objects:
        galaxy.append(star( ob[1], ob[2], ob[3], ob[4], galaxy, ob[6].replace("'", '') ))

    #galaxy.append(Star(M/2, [1, 0], [1, 3**0.5], 0, galaxy))
    #galaxy.append(Star(M/2, [-1, 0], [1, -(3**0.5)], 1, galaxy))
    # galaxy.append(Star(M/2, [0, 3**0.5], [-2, 0], 2, galaxy))
    #
    # galaxy.append(Star(M, [1, 1], [-3, 3], 0, galaxy))
    # galaxy.append(Star(M, [1, -1], [3, 3], 1, galaxy))
    # galaxy.append(Star(M, [-1, -1], [3, -3], 2, galaxy))
    # galaxy.append(Star(M, [-1, 1], [-3, -3], 3, galaxy))

    #---Print start configuration---
    # for i in range (0, N):
    #     #galaxy.append(Star(M/2, ranrv(5), ranrv(0.5), i, galaxy))
    #     galaxy[i].printstar()

    #--define function for pulse---
    if pulse_table == True:
        def Pn(galaxy, n):
            ps = []
            for st in galaxy:
                ps.append(st.Ps[n-1])
            return scal(dsum(ps))

    #---Iterator---
    for n in range (2, enn):
        dtn = dt
        for ss in galaxy:
            ss.iter(galaxy, n, dtn, ss.i)
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

    Vis.vis_N_2D(galaxy, inum, delta_cur)
    #Vis.vis_N_3D(galaxy).show
    #Vis.vis_N_anim(galaxy, enn).save('Galaxy.gif', writer='imagemagic', fps=60)

#------PROGONS------
delta_start = 0.2
delta_end = 0.3
k = 3 #количество симуляций
delta_step = 0.01

def progons(N, dur, end, dt, delta_step, k, delta_start, delta_end, pulse_table):
    progons_global_time = time.time()

    delta_cur = delta_start
    while delta_cur <= delta_end:
        for inum in range (0, k):
            simul(N, dur, end, dt, delta_cur, inum, pulse_table)
        delta_cur = float(delta_cur) + delta_step

    print('progons_global_time')
    print("--- %s seconds ---" % (time.time() - progons_global_time))
