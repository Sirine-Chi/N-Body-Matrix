# N-Body-Matrix — Code Evaluation & Roadmap

Reviewer notes, June 2026. Nothing in your code was modified; this is a standalone report.

---

## 0. TL;DR

Your **architecture instincts are good** — ECS, separated visualisation, a binary force map, a pluggable
"Method" abstraction. The **execution is held back by one fatal performance decision and a handful of real
correctness bugs.** The fatal decision is wrapping every individual 3-vector in its own GPU tensor. That,
not "loading/reading back from GPU," is why your GPU experiments lost. Fix the data layout and most of your
goals become reachable; the rest are a matter of wiring the pieces you already designed.

If you only read three lines:

1. **Stop storing one tensor per particle.** Store the whole system as one `(N, 3)` array.
2. **Stop appending full history every step.** Keep only the last *k* states (you already wrote a `TubeList` ring buffer for exactly this — it's unused).
3. **Wire `numerical.py` into the loop.** Your integrator is currently hardcoded Euler, not the "arbitrary linear multistep method" you intended.

---

## 1. Critical issues (fix these — everything else is noise until they're gone)

### C1. Per-vector GPU tensors — the real performance killer
`mylinal_torch` wraps each 3-element vector as its own `torch.Tensor` on MPS. Every `+`, `-`, `*` on a
3-number vector launches a separate MPS kernel through the full Python→ATen dispatch, and `scal()` calls
`.item()`, which forces a **host↔device sync every single force evaluation.** For 3-element data this is
roughly 100–1000× *slower* than plain NumPy, and far slower than CPU scalars.

This is the misdiagnosis to correct: GPUs are not bad for N-body. *Scalar work on a GPU* is bad. The transfer
cost you noticed is real but secondary — the primary loss is kernel-launch + sync overhead on tiny operands.
The right unit of work is "all N bodies at once," computed in one vectorised kernel, with data resident on the
device for the whole run. Done that way, GPU brute-force scales to ~10⁵–10⁶ bodies.

**Direction:** one state array `pos` of shape `(N, 3)`. Pairwise gravity in ~4 vectorised lines:
`d = pos[None,:,:] - pos[:,None,:]` → `(N,N,3)`; `r3 = (‖d‖²+ε²)^1.5`; `acc = G * Σ_j m_j d / r3`.
That single expression replaces the entire triple-nested Python loop and runs on CPU (NumPy) or GPU (one
backend swap) with no per-pair dispatch.

### C2. Unbounded history growth
`Position.positions`, `Velocity.velocities`, `Acceleration.accelerations` are lists you `.append()` to every
step forever. At `step=5e-5`, `t_end=1` that's 20 000 entries × N bodies of retained objects. Memory is
**O(steps)** and caps your runtime long before CPU does. A linear multistep method of order *k* needs only the
last *k* derivative values — nothing older. You already wrote `TubeList` (a fixed-depth ring buffer) for this
and `Method.check_depth()` to enforce it; they're just never connected. Use them.

### C3. The integrator is hardcoded Euler, not a linear multistep method
`numerical.py` is a nice design — `@new_method(order=k)` decorator, order/depth checking, string introspection.
But `ForceProcessor.process()` ignores it entirely and inlines symplectic-Euler (`v += h·a; x += h·v`). So
your headline requirement ("arbitrary LMM, then minimum past points required") is *designed but not wired in.*
Worse, the method formulas themselves are wrong:

- `euler`: `return xs[-1] + h*f(...)/2` — stray `/2`, and integrates `xs` instead of `ys`.
- `adams`: `xs[-1] + h*3/2*ys[-1] - h/2*ys[-2]` — mixes state and derivative; the real 2-step Adams-Bashforth is `y_{n+1} = y_n + h(3/2·f_n − 1/2·f_{n−1})`, i.e. it must use *f values*, not `ys`.
- `two_step` (leapfrog/midpoint) is the only roughly-correct one.

**Direction:** make the processor call `method(xs, ys, f, h)` and store the AB/AM coefficients as data so
"arbitrary order" is a table lookup, not new code per method. Validate each method against a known solution
(e.g. circular orbit conserves energy to the method's order).

### C4. Kinetic-energy formula is wrong
`MonitoringProcessor.process`:
```python
kinetics.append(l.Array.scal(vel.velocities[-1]) * m.mass)   # |v| · m
...
self.pairs.append((t_cur, 0.5 * l.np.sum(kinetics)))         # 0.5 Σ m|v|
```
`scal` returns the **norm** `|v|`, so you compute `½·Σ m|v|` instead of `½·Σ m|v|²`. Square it:
`scal(v)**2`. (And the conservation check you want needs potential energy too — currently TODO.)

### C5. No softening + fixed-step explicit Euler = energy blow-ups
`gravity_force_ent` is dimensionally correct (`G m₁ m₂ (r₂−r₁)/|r|³`) but has no softening. On any close
approach `|r|→0` the force explodes, and fixed-step Euler can't recover — the system gains energy and flies
apart. Add a softening length: `|r|³ → (|r|²+ε²)^{3/2}`. For accuracy without softening, you need an adaptive
or symplectic integrator (see §4).

---

## 2. Minor issues (note them, don't let them distract you)

- **`color4f.c` is a shared class attribute.** `c = [...]` lives on the class; `__init__` mutates it in place, so *every* `color4f` instance shares and overwrites one list. Move `self.c = [...]` into `__init__`.
- **Modules execute on import.** `generator.py` builds and writes a system at import time; `func_parser.py` prints at import; `mylinal*.py` print device banners. Wrap runnable code in `if __name__ == "__main__":`.
- **`decart_to_polar` returns `decart`** (the input) instead of the computed `pol`.
- **`mylinal.py randarr_fixed_length`**: `args[0] = [lenght]` before `args` exists → `NameError`.
- **`Angle.normalise_angle`** accumulates `p*i` with growing `i` — won't normalise correctly.
- **Newton's third law unused.** You compute F(i,j) and F(j,i) separately — exactly double the work. One pass over `i<j` with `F_ji = −F_ij` halves it.
- **Repo hygiene:** `.venv/` (849 MB) and `nbody/tmp/*.csv` are committed. Add to `.gitignore`; the repo should be a few hundred KB.
- **Backends drift.** `mylinal.py`, `mylinal_cl.py`, `mylinal_torch.py` reimplement the same API three times and have diverged (the numpy one has the `args[0]` bug, the torch one doesn't). Pick one interface, one implementation, swap the array backend underneath.

---

## 3. Performance limits — what each approach can realistically reach

Order-of-magnitude ceilings for a direct (all-pairs) gravitational solve at interactive-ish speeds:

| Approach | Practical N | Why |
|---|---|---|
| **Current** (per-vector torch on MPS) | ~10–20 | Per-pair kernel launch + `.item()` sync dominates; ~ms per body-pair |
| Pure-Python objects (numpy per vector) | ~50 | Python-loop bound, O(N²) calls |
| **NumPy vectorised** `(N,3)` broadcast | ~2 000–5 000 | One C loop; O(N²) compute, O(N²) temp memory |
| Numba / Cython direct kernel | ~10⁴ | Native loop, no temporaries, SIMD |
| **GPU brute-force, one kernel** (tiled) | ~10⁵–10⁶ | Thousands of cores, data resident on device |
| Barnes-Hut (CPU, O(N log N)) | ~10⁵–10⁶ | Tree approximation of far field |
| FMM / GPU treecode (O(N)) | 10⁷+ | Production galaxy/cosmology scale |

Your galaxy-rotation goal (§6.4) lands in the bottom half of this table: N=100 is too few to *see* a rotation
curve; you want N≈10⁴–10⁵, which means vectorised + Barnes-Hut **or** a proper GPU kernel — never per-vector
tensors.

One structural note: even with a perfect solver, **writing every step's full state to a Python list (C2) and
re-drawing every step in pygame caps throughput.** Decouple simulation rate from render rate (render every k-th
step or on a timer) and stream history to disk/`TubeList`, not RAM.

---

## 4. Ready-to-go solutions (you asked me to find and study these)

### If your goal is *science results fast* — don't rebuild the engine
- **REBOUND** (Rein et al.) — the de-facto open-source N-body code. C99 core, `pip install rebound`, clean Python API, cross-platform. Ships exactly the integrators you'd otherwise spend months on: **WHFast** (symplectic Wisdom-Holman, for a dominant central mass — your solar system), **IAS15** (15th-order adaptive, machine-precision close encounters), leapfrog, SABA, and **collision/tree modules.** This is the reference to benchmark yourself against and arguably to *build on*. [[rebound](https://github.com/hannorein/rebound)] [[docs](https://rebound.readthedocs.io)]
- **AMUSE** — Python framework that orchestrates many physics codes (gravity, stellar evolution, hydro) behind one interface. Overkill for you now, but the design is worth studying for how it separates "framework" from "solver." [[amuse]]
- **galpy** (orbits in galactic potentials) and **pynbody** (analysis/visualisation of N-body + SPH snapshots) — useful for §6.4; pynbody in particular can load and plot snapshots so you don't write a viewer. [[galpy](https://docs.galpy.org)] [[pynbody](https://github.com/pynbody/pynbody)]

### Linear-multistep / ODE integrators *already implemented* (your explicit question)
- **SUNDIALS / CVODE** — the gold standard. Variable-order **Adams-Moulton (orders 1–12)** for non-stiff and **BDF (1–5)** for stiff, with adaptive step and order selection. C library, Python bindings (`scikit-sundae`, `sundials-py`). If you want "arbitrary LMM, choose order, minimum past points handled for you" — this *is* that, battle-tested. [[sundials]]
- **scipy** `integrate.solve_ivp` — `LSODA` (auto Adams↔BDF switching) and `BDF` are multistep; `Radau` is implicit RK. Easiest drop-in in Python. [[scipy]]
- **Julia `OrdinaryDiffEq.jl`** — the widest LMM menu anywhere: `AB3/4/5`, `ABM`, `VCABM` (variable-coeff Adams, great for large smooth systems), full BDF. If you ever want a research playground for *method comparison*, Julia is unmatched here. [[SciML ODE solvers](https://docs.sciml.ai/DiffEqDocs/stable/solvers/ode_solve/)]
- **diffrax** (JAX) — multistep + RK with autodiff and GPU, if you go the JAX route.
- **C++ `boost::odeint`** — `adams_bashforth` and `adams_bashforth_moulton` steppers built in; pairs naturally with Eigen.

### C++ N-body engines to study or reuse
- **rakau** — C++17 Barnes-Hut, runs multicore CPU **and** CUDA GPU from the same code; good model for "one source, heterogeneous hardware." [[rakau](https://github.com/bluescarni/rakau)]
- **beltoforion/Barnes-Hut-Simulator** — clean, readable reference implementation to learn the algorithm. [[link](https://github.com/beltoforion/Barnes-Hut-Simulator)]
- **yboetz/nbody_bhtree** — C++ + OpenMP + AVX, called from Python via Cython, visualised with pyqtgraph. This is almost exactly the hybrid architecture I'd suggest for you (§5). [[link](https://github.com/yboetz/nbody_bhtree)]

### Trajectory optimisation (for §6.3)
- **pykep + pygmo** (ESA) — interplanetary trajectory optimisation; Sims-Flanagan low-thrust legs, Lambert solvers, global optimisation via monotonic basin hopping. The right toolbox if "min fuel A→B" becomes a focus. [[pykep example](https://keptoolbox.sourceforge.net/examples/ex1.html)]

---

## 5. Python or C++? — and cross-platform

**Recommended: a hybrid, and it resolves the dilemma cleanly.**

- **Keep Python as the shell** — ECS bookkeeping, config (TOML), the force-map, monitoring, visualisation, experiment scripting. This is where your design already shines and where "others can edit easily" matters most.
- **Push only the hot inner loop down** — the pairwise force/integration kernel. Three escalating options, in order of effort:
  1. **NumPy-vectorised** (`(N,3)` arrays). Zero new dependencies, gets you to N~few-thousand. *Do this first* — it alone fixes C1.
  2. **Numba** `@njit` on the kernel. One decorator, native speed, still pure Python source. N~10⁴.
  3. **C++ core via pybind11** (or use **rakau**/an existing tree code), exposed as a Python module. N~10⁶. This is the `nbody_bhtree` pattern above.

This hybrid means the *answer to "Python or C++"* is "both, layered": Python for everything a human touches,
C++/Numba for the ~50 lines that run a billion times.

**If you go pure C++:** Eigen (linalg) + boost::odeint or SUNDIALS (integrators) + a tree code, built with
**CMake**, dependencies via **vcpkg** or **Conan**. Visualisation: raylib or Magnum, or simplest — write
positions to disk and view in Python. Expose the core with **pybind11** so non-C++ users still drive it from
Python.

**Cross-platform (M-series Mac dev → Windows/Linux users):**
- Avoid OS-specific paths and your current OpenGL-immediate-mode viewer (`glBegin/glEnd` is deprecated and flaky across drivers). For portability use a modern viewer: **moderngl**, **vispy**, or **pyqtgraph** (your `nbody_bhtree` reference uses pyqtgraph).
- Pin the toolchain: `pyproject.toml` + `uv`/`pip` lockfile (you already have `uv.lock` — good). For a C++ core, CMake + GitHub Actions building wheels for macOS/Windows/Linux (`cibuildwheel`) gives one `pip install` for everyone.
- Don't depend on MPS/CUDA being present — make the GPU backend optional with a NumPy fallback, so Windows/Linux users without your hardware still run.

---

## 6. Research questions

### 6.1 Bringing in new questions
Your codebase, once §1 is fixed, is a fine *experiment platform*. Good additional questions: energy/momentum
conservation vs integrator order and step size; sensitivity to initial conditions (Lyapunov time) in the
3-body problem; the statistics of escape/ejection in small clusters; orbital resonance capture. These are all
"set up a system, integrate, measure a conserved/derived quantity" — which is exactly what your
MonitoringProcessor is for (extend it to potential energy, total momentum, angular momentum).

### 6.2 Finding closed / stable periodic orbits — **yes, very doable**
Method: **differential correction (shooting).** Parameterise initial conditions, integrate one period,
define a return error `‖x(T) − x(0)‖`, and Newton-iterate on the initial conditions / period using the
**state-transition (monodromy) matrix** as the Jacobian. Stability comes free: the **eigenvalues of the
monodromy matrix (Floquet multipliers)** tell you if the orbit is stable (on the unit circle) or unstable.
This reproduces the famous **figure-eight three-body choreography** (Chenciner & Montgomery, 2000) and the
Lagrange/Euler central configurations. It's a great, self-contained research module and pairs perfectly with
your existing integrator — you just need a Newton corrector and the variational equations.

### 6.3 Minimising time / fuel from A to B — **doable, but it's a different problem class**
This is **optimal control**, not just integration — flag the scope change. Two standard routes:
- **Indirect** (Pontryagin's maximum principle): derive costate equations, solve the two-point boundary value problem. Accurate, optimal, but needs good initial costate guesses (notoriously sensitive).
- **Direct** (collocation / Sims-Flanagan): discretise the trajectory and hand it to an NLP optimiser (IPOPT, SNOPT). More robust, what pykep/pygmo use.
Recommendation: don't build this from scratch first — prototype with **pykep**, learn the structure, then
decide whether a bespoke version on your engine is worth it.

### 6.4 Galaxy rotation curve (N > 100) — **yes, and it's a great project**
N=100 is too few to *see* a curve; target **N ≈ 10⁴–10⁵** (which forces §1's fixes + Barnes-Hut or a GPU
kernel). Initialise a disk (exponential surface density) with circular velocities, integrate, then bin
particles by radius `r` and plot mean `|v_circ|(r)`. The payoff: a self-gravitating disk of visible matter
alone gives a **Keplerian falloff** `v ∝ r^{-1/2}` at large r; real galaxies are **flat** — the classic
motivation for dark matter / a halo term. Add a static halo potential and watch the curve flatten. Highly
pedagogical, and a clean showcase for the software.

---

## 7. How to make this a *great* N-body study tool — suggested order of work

1. **Collapse to one vectorised state array** `(N,3)` and one vectorised force kernel (kills C1, C5, the N³ loop). NumPy first; make the backend swappable.
2. **Wire `numerical.py` into the loop** with a coefficient table for AB/AM of arbitrary order; use `TubeList` for the *k*-step history (kills C2, C3). Validate each method on a circular orbit.
3. **Finish MonitoringProcessor**: kinetic (fixed, C4) + potential + total energy + linear & angular momentum; assert conservation as your correctness test.
4. **Add softening + an adaptive/symplectic option** (leapfrog is ~10 lines and conserves energy beautifully; reach for IAS15/REBOUND when you need close encounters).
5. **Modernise the viewer** (moderngl/pyqtgraph), decouple render rate from sim rate.
6. **Scale**: Numba kernel → Barnes-Hut → optional GPU/pybind11 C++ core. Benchmark each against REBOUND for a sanity check.
7. **Then** the science modules: periodic-orbit finder (6.2), rotation curve (6.4), optionally trajectory opt via pykep (6.3).
8. **Repo hygiene throughout**: drop `.venv`/tmp CSVs from git, `__main__` guards, one linalg backend, a couple of pytest conservation tests, CI wheels for cross-platform.

A realistic framing: steps 1–4 turn this from "a clever sketch that runs ~10 bodies" into "a correct,
extensible engine that runs thousands and conserves energy." Steps 5–8 turn that into something others can
install, trust, and do research with.

---

## Sources
- REBOUND: <https://github.com/hannorein/rebound>, <https://rebound.readthedocs.io>, <https://rebound.hanno-rein.de/integrators/>
- AMUSE / galpy / pynbody: <https://docs.galpy.org>, <https://github.com/pynbody/pynbody>
- LMM / ODE solvers: <https://docs.sciml.ai/DiffEqDocs/stable/solvers/ode_solve/>, SUNDIALS CVODE, scipy `solve_ivp`
- C++ N-body: <https://github.com/bluescarni/rakau>, <https://github.com/beltoforion/Barnes-Hut-Simulator>, <https://github.com/yboetz/nbody_bhtree>
- Trajectory optimisation: <https://keptoolbox.sourceforge.net/examples/ex1.html>
</content>
</invoke>
