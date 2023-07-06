import pyopencl as cl
import numpy as np
import numpy.linalg as la
import datetime
import time
from random2 import uniform
from random2 import triangular
from random2 import getrandbits
from random2 import randint
import NBodyLib as ndl

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

h = 0.00000001 #time step
G = 0.0001184069#09138

r1t0 = v([1, 1])
r2t0 = v([2, 3])
r3t0 = v([1, 3])
rt0 = v([r1t0, r2t0]) #вектор состояния системы

v1t0 = v([0.5, 0.2])
v2t0 = v([-0.1, -0.1])
v3t0 = v([0.2, 0.4])
vt0 = v([v1t0, v2t0]) #вектор скорости системы

m1 = 100
m2 = 1
m3 = 20
ms = v([m1, m2])
mmx =  v([ [1/m1, 0], [0, 1/m2] ])

#составить матрицу масс
def gravec(r1, r2):
    if r1.all() != r2.all():
        return v( (r2-r1)/dist(r1, r2)**3 )
    else:
        return [0, 0]
def mass_m(ms):
    mx = []
    for i in ms:
        ln = []
        for j in ms:
            ln.append(i*j)
        mx.append(ln)
    return v(mx)
def rs_m(rs):
    rm = []
    for i in rs:
        l = []
        for j in rs:
            #print(gravec(i, j))
            l.append(gravec(i, j))
        rm.append(l)
    return v(rm)

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

        def f12(obj1, obj2, n): #силa, действующая на 1 от 2
            f12 = v( unvec(obj2.r[n-1]-obj1.r[n-1]) * obj1.m*obj2.m*G / (dist(obj2.r[n-1], obj1.r[n-1])**2) )
            return f12
        def f(obj, system, n):
            obj.fn=[]
            for other in system:
                if obj != other:
                    obj.fn.append(f12(obj, other, n))
            return dsum(obj.fn)

            #FOR ADAMS
            self.r.append(v(self.r[0]+dt*self.v[0]))
            self.v.append(v(self.v[0]+dt*self.f[0]/self.m))
            self.t.append(1)
            self.f.append( f(self, system, 2) )

    def print_object(self):
        print("id="+str(self.i), self.m, "f"+str(self.f), "v"+str(self.v), "r"+str(self.r), "t"+str(self.t))
    def print_object_coor(self):
        print("id="+str(self.i), self.r)
    def makeXY(obj):
        x_s0=[]
        y_s0=[]
        for i in obj.r:
            x_s0.append(i[0])
            y_s0.append(i[1])
        return [x_s0, y_s0]

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
            self.v.append(v( self.v[n-1]+dt*self.f[n-1]/self.m )) # Eiler
        elif method == 'Eiler_Reverse':
            self.v.append(v( self.v[n-1]+dt*self.f[n-1]/self.m )) # Eiler anvis
        elif method == 'Midpoint':
            self.v.append(v( self.v[n-1]+ dt*f( self.r[n-1]+ dt/2*f(self.r[n-1]) )/self.m )) # Midpoint
        elif method == 'Adams':
            self.v.append(v( self.v[n-1] + dt/2*( 3*self.f[n]/self.m - self.f[n-1]/self.m) )) # Adams

        if method == 'Eiler':
            self.r.append(v( self.r[n-1]+dt*self.v[n])) #Eiler
        elif method == 'Midpoint':
            self.r.append(v( self.r[n-1]+ dt/2*(self.v[n-1]+self.v[n-2]) )) #midpoint
        elif method == 'Adams':
            self.r.append(v( self.r[n-1] + dt/2*(3*self.v[n-1] - self.v[n-2]) )) # Adams

    def reper(self, n):
        self.r[n] = self.r[n] - system[0].r[n]

class object(Object):
    pass

def test_1(rt0, vt0, ms, mmx):
    test1_time = time.time()

    rss = []
    vss = []
    ass = []
    ass.append(mass_m(ms) * rs_m(rt0) * mmx)
    vss.append(vt0 + h*ass[0])
    rss.append(rt0 + h*vss[0])

    num = int(1/h)
    for i in range (1, num):
        ass.append(mass_m(ms)*rs_m(rss[i-1])*mmx)
        vss.append(vss[i-1] + h*ass[i])
        rss.append(rss[i-1] + h*vss[i])

    print('test1_time')
    print("--- %s seconds ---" % (time.time() - test1_time))


def test_2(rt0, vt0, ms, mmx):
    test2_time = time.time()

    obs = []
    obs.append(['p1', m1, r1t0, v1t0, 0, 'obs', 'w'])
    obs.append(['p2', m2, r2t0, v2t0, 1, 'obs', 'w'])

    NBodyLib.simul('Eiler', obs, 1, 1, 1, h, 0, 's', 0, 0)

    print('test2_time')
    print("--- %s seconds ---" % (time.time() - test2_time))

test_1(rt0, vt0, ms, mmx)
test_2(rt0, vt0, ms, mmx)