import numpy as np
import pandas as pd
import math
import Visualise as Vis

def dist(v1, v2): #расстояние между двумя точками (концами векторов v1 и v2)
    d = ( (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2 )**0.5
    return d
def scal(v): #Модуль (скаляр, длиннна) вектора
    l = (v[0]**2 + v[1]**2 )**0.5
    return l
def v(v1): #вектор
    v = np.array(v1)
    return v
def unvec(v): #еденичный вектор с тем же направлением
    uv = v / scal(v)
    return uv

#end = int(input('Iterations = '))
#dt = float(input('Delta time = '))
dur = 1
end = 3 * 10**5
dt = dur *0.000005

G = 0.000118406909138
M = 332840
m = 1

r_0 = v([1, 0])
v_0 = v([0, 8.4138888])
f_0 = v( -1 * unvec(r_0) * (m*M*G / scal(r_0)**2) )

f = []
a = []
vs = []
r = []
t = []

f.append(f_0)
a.append(f_0/m)
vs.append(v_0)
r.append(r_0)
t.append(0)

for n in range (1, end):
    t.append(dt*n)
    f.append(v( -1 * unvec(r[n-1]) * (m*M*G / dist([0, 0], r[n-1])**2) ))
    a.append(v( f[n]/m ))
    vs.append(v( vs[n-1] + dt*(a[n]) ))
    r.append(v( r[n-1] + dt*(vs[n]) ))

    if scal(r[n]) < 0.15 or scal(r[n]) > 200:
        break
    else:
        continue
    #n += 1

vecs = pd.DataFrame(
    {
        "t_s":t,
        "r_v":r,
        "v_v":v,
        "a_v":a,
    }
)

x_s = []
y_s = []
for i in range (0, len(r)):
    x_s.append( (r[i])[0] )
    y_s.append( (r[i])[1] )

xyt = pd.DataFrame(
    {
        "t_s":t,
        "x_s":x_s,
        "y_s":y_s
    }
)

print(vecs)
#print(xyt)
#vecs.to_csv('Eiler_2b_vec.csv')
#xyt.to_csv('Eiler_2b_xyt.csv')
p = Vis.vis_1_23D(x_s, y_s, t)
p.show
