import NBodyLib as nbl
import time
import numpy as np
import random2

def v(lisst):
    return np.array(lisst)

# Типо много тел на прямой с разными координатами

class Simulator():
    def __init__(self, r, v, m, time, step, *args, **kwargs):
        self.m = m
        self.time = time
        self.step = step
        self.delta_time = 0

        self.ts = []
        self.rs = []
        self.vs = []
        self.ts.append(0)
        self.rs.append(r)
        self.vs.append(v)

        print("Simulator Initialized!")

    def iteration(self, step):
        self.vs.append(self.vs[-1])
        self.rs.append(self.rs[-1] + step*self.vs[-1]/(self.m**2))
        # print(self.rs)

    def render_simulation(self, total_time, step):
        start_time = time.time()
        tau = step
        while tau < total_time:
            Simulator.iteration(self, step)
            self.ts.append(tau)
            tau += step
        self.delta_time = time.time() - start_time


    def get_time(self):
        return self.delta_time
    
    def get_plot_data(self):
        return self.rs[-1]

N = 10 # Bodies
r_s = []
v_s = []
m_s = []
for i in range(1, N, 1):
    r_s.append(random2.uniform(-10, 10))
    v_s.append(random2.uniform(-2, 2))
    m_s.append(random2.uniform(0, 6))
print('R', r_s, '\n', 'V', v_s, '\n', 'M', m_s)
total_time = 100
step = 0.1

s = Simulator(v(r_s), v(v_s), v(m_s), time, step)
s.render_simulation(total_time, step)
print(s.get_plot_data())
