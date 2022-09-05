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
end = 3 * 10**6
dt = 0.000005
que = 1 + 0.000026*dt

G = 0.000118406909138
M = 332840
m = 1

r_0 = v([1, 0])
v_0 = v([0, 8.4138888])
f_0 = v( -1 * unvec(r_0) * (m*M*G / scal(r_0)**2) )

f_1 = v( -1 * unvec(r_0) * (m*M*G / scal(r_0)**2) )
a_1 = f_1/m
v_1 = v( v_0+dt*a_1)
r_1 = v( r_0+dt*v_1 )

f_v = []
a_v = []
v_v = []
r_v = []
t_s = []

f_v.append(f_0)
f_v.append(f_1)
a_v.append(f_0/m)
a_v.append(f_1/m)
v_v.append(v_0)
v_v.append(v_1)
r_v.append(r_0)
r_v.append(r_1)
t_s.append(0)
t_s.append(dt)

for n in range (2, end):
    t_s.append(dt*n)
    f_v.append(v( -1 * unvec(r_v[n-1]) * (m*M*G / scal(r_v[n-1])**2) ))
    a_v.append(v( f_v[n]/m ))
    v_v.append(v( v_v[n-1] + dt/2*(3*a_v[n-1] - a_v[n-2]) ))
    #v_v.append(v( v_v[n-1] + dt*(a_v[n]) ))
    r_v.append(v( r_v[n-1] + dt/2*(3*v_v[n-1] - v_v[n-2]) ))
    #r_v.append(v( r_v[n-1] + dt*(v_v[n]) ))

    if scal(r_v[n]) < 0.15 or scal(r_v[n]) > 200:
        break
    else:
        continue
    n += 1

vecs = pd.DataFrame(
    {
        "t_s":t_s,
        "r_v":r_v,
        "v_v":v_v,
        "a_v":a_v,
    }
)

x_s = []
y_s = []
for i in range (0, len(r_v)):
    x_s.append( (r_v[i])[0] )
    y_s.append( (r_v[i])[1] )

xyt = pd.DataFrame(
    {
        "t_s":t_s,
        "x_s":x_s,
        "y_s":y_s
    }
)

print(vecs)
#print(xyt)
#vecs.to_csv('Eiler_2b_vec.csv')
#xyt.to_csv('Eiler_2b_xyt.csv')
p = Vis.vis_1_23D(x_s, y_s, t_s)
p.show
