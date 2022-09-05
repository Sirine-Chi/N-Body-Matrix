import numpy as np
import pandas as pd
import math
import Visualise as Vis
from random2 import uniform
from random2 import triangular
from random2 import getrandbits

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
    rv = v([uniform(-r, r), 2*(float(getrandbits(1))-0.5)*(r**2 - uniform(-r, r)**2)**0.5])
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
    return v(vl)
def dsum(v_list):
    vlx=[]
    for i in v_list:
        vlx.append(i[0])
    vly=[]
    for i in v_list:
        vly.append(i[1])
    return v([sum(vlx), sum(vly)])

G = 0.000118406909138
M = 332840
N = 20

dur = 1
end = 4 * 10**4
dt = dur * 0.02

class Star:
    def __init__(self, m, r0, v0, i, *args, **kwargs):
        self.m = m
        self.r0 = r0
        self.v0 = v0
        self.i = i
        self.r = []
        self.v = []
        self.a = []
        self.f = []
        self.t = []
        self.r.append(v(r0))
        self.v.append(v(v0))
        self.t.append(0)
        self.f0s=[]
        for other in galaxy:
            if self.i != other.i:
                self.f0s.append(v( unvec(other.r[0]-self.r[0]-[0.00001, 0]) * (self.m*other.m*G / dist(other.r[0], self.r[0]-[0.00001, 0])**2) ))
        self.f.append(dsum(self.f0s))
        self.a.append(self.f[0]/self.m)

    def iteration(self, galaxy, n, dt, i):
        self.t.append(n*dt)
        self.fn=[]
        for ot in galaxy:
            if self.i != ot.i:
                self.fn.append(v( unvec(ot.r[n-1]-self.r[n-1]-[0.00001, 0]) * (self.m*ot.m*G / dist(ot.r[n-1], self.r[n-1]-[0.00001, 0])**2) ))
        self.f.append(dsum(self.fn))
        self.a.append(self.f[n]/self.m)
        #print(self.i, self.a[n])
        self.v.append(v( self.v[n-1]+dt*self.a[n]  ))
        self.r.append(v( self.r[n-1]+dt*self.v[n]  ))

    def printstar(self):
        print("id="+str(self.i), self.m, self.f, self.v, self.r, self.t)
    def print_s_cor(self):
        print("id="+str(self.i), self.r)
    def makeXY(self):
        x_s0=[]
        y_s0=[]
        for i in galaxy[self.i].r:
            x_s0.append(i[0])
            y_s0.append(i[1])
        return [x_s0, y_s0]

galaxy = []
#galaxy.append(Star(M, [0, 0], [0, 0], 0 ))
#galaxy.append(Star(1, [1, 0], [0, 8.4138888], 1 ))

#galaxy.append(Star(M, [1, 0], [1, 3**0.5], 0 ))
#galaxy.append(Star(M, [-1, 0], [1, -(3**0.5)], 1 ))
#galaxy.append(Star(M, [0, 3**0.5], [-2, 0], 2 ))
for i in range (0, N):
    galaxy.append(Star(M, ranvec(10), ranvec(10), i ))
    galaxy[i].printstar()

for n in range (1, end):
    for ss in galaxy:
        #ss.printstar()
        ss.iteration(galaxy, n, dt, ss.i)

#print(galaxy[0].r)
#print( len(galaxy[1].r) )

#p = Vis.vis_1_23D(galaxy[0].makeXY()[0], galaxy[0].makeXY()[1], galaxy[0].t )
p2 = Vis.vis_N_2D(galaxy)
p3 = Vis.vis_N_3D(galaxy)

#p.show
p2.show
p3.show
