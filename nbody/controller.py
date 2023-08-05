import time

import n_body_lib as nbl
import numpy as np
import random2
from simulator_test import Simulator

# === === Set variables === ===

# Global variables
N = 10  # Bodies
total_time = 100
step = 0.1

# Data
r_s = []
v_s = []
m_s = []
for i in range(1, N, 1):
    r_s.append(random2.uniform(-10, 10))
    v_s.append(random2.uniform(-2, 2))
    m_s.append(random2.uniform(0, 6))
print("R", r_s, "\n", "V", v_s, "\n", "M", m_s)

# === === Actual Run === ===

s = Simulator(nbl.v(r_s), nbl.v(v_s), nbl.v(m_s), time, step)
s.render_simulation(total_time, step)
print(s.get_plot_data())
