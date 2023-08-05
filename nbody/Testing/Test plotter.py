import matplotlib.pyplot as plt
import numpy as np

import nbody.n_body_lib as nbl

# --- --- PLOT DRAWING --- ---

data = nbl.pd.read_csv("Testing/Time test.csv")
data2 = nbl.pd.read_csv("Testing/Time loop.csv")
ns = data["Number"]
ts = data["Time"]
ns2 = data2["Number"]
ts2 = data2["Time"]

highres_ns = np.linspace(1, 60, 300)
aprx1 = lambda x: 0.13 * (x ** (-2))  # Approximation with POWER
tsa = list(map(aprx1, highres_ns))

# Plot properties

plt.style.use("dark_background")
plt.rcParams["text.usetex"] = True
fig, ax = plt.subplots()
plt.legend()
# plt.semilogy()
# fig.tight_layout()

ax.set(
    xlabel=r"Number of objects (1)",
    ylabel=r"$1/T \quad (sec^{-1})$",
    title="Performance",
)
ax.grid(True, color="grey", alpha=0.25)

ax.plot(ns, 1 / ts, c="lime", label=r"OpenCL")
ax.plot(ns2, 1 / ts2, c="violet", label=r"Loop CPU")

ax.plot(
    highres_ns, tsa, c="red", label=r"Approx $y = 0.13x^{-2}$"
)  # Approximation with POWER

fig.savefig("Test Loop + OpenCl.png", dpi=450)
plt.show()
