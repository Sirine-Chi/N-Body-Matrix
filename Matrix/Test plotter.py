import numpy as np

import NBodyLib as nbl
import matplotlib.pyplot as plt

# --- --- PLOT DRAWING --- ---

data = nbl.pd.read_csv('Time test.csv')
ns = data["Number"]
ts = data["Time"]

aprx1 = lambda x: 0.1*(x**(-9/5))
aprx2 = lambda x: 0.723 * np.exp(-0.4529*x)


tsa = list(map(aprx1, ns))
tsb = list(map(aprx2, ns))

plt.style.use('dark_background')
plt.rcParams['text.usetex'] = True
fig, ax = plt.subplots()

ax.plot(ns, 1/ts, c="lime", label=r'OpenCL')
ax.plot(ns, tsa, c="red", label=(r'Approx $y = 0.1x^{-1.8}$'))
# ax.plot(ns, tsb, c="blue", label=(r'Approx $y = 0.7e^{-0.45x}$'))

ax.set(xlabel=r'Number of objects (1)', ylabel=r'$1/T \quad (sec^{-1})$',
       title='Performance')
ax.grid(True, color='grey', alpha=0.25)
plt.legend()

fig.savefig("Test.png")
plt.show()
