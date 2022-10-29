import NBodyEiler as nbe

#CONSTANTS
G = 0.000118406909138
M = 332840
N = 4
#Parametries
dur = 1
end = 1*(10**1)
dt = dur * 0.0001

k = 10 #количесвто симуляций
delta_v = 0
while delta_v <= 1:
    for inum in range (0, k):
        nbe.simul(dur, end, dt, delta_v, inum)
    delta_v = delta_v + 0.001
