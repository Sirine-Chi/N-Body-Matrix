# N-body in C++ — system-vector, two backends

This folder ports the **single `(N,3)` state-array** approach from the Python notebook to C++,
with two interchangeable backends sharing one set of initial conditions and one ASCII visualiser:

| File | Backend | Hardware | Library |
|---|---|---|---|
| `src/eigen_backend.cpp` | CPU, tight pairwise loop | any | [Eigen](docs/INSTALL_eigen.md) |
| `src/mlx_backend.cpp` | GPU, broadcast kernel | Apple silicon (Metal) | [MLX](docs/INSTALL_mlx.md) |
| `src/nbody_common.hpp` | shared state + ASCII plot | — | — |

---

## 1. Does the system-vector idea make sense in C++? — Yes, even more than in Python

In Python the `(N,3)` array is essential because Python loops are ~100× too slow, so you push all
the work into one NumPy/Torch call. In C++ the motivation shifts but the conclusion is stronger:

- **Keep the contiguous `(N,3)` state array.** One block of memory for all positions is cache-friendly
  and SIMD-friendly — the single biggest performance lever on CPU. This is the SoA layout your ECS
  should compile down to.
- **But drop the `(N,N,3)` temporary.** That giant intermediate only exists in NumPy to avoid a Python
  loop. In C++ the native pairwise double-loop (`eigen_backend.cpp`) is *faster* and uses **O(N)** memory
  instead of O(N²). So "system vector" in C++ means *contiguous state + a tight kernel*, not *materialise
  a huge broadcast*.
- **On GPU the broadcast kernel is the right shape** (`mlx_backend.cpp`): thousands of threads, one per
  body, each summing over all others. MLX expresses this with the same broadcasting code as NumPy.

Measured here (inner solar system, N=5, 12 000 steps, on a Linux CI box):

```
[eigen/CPU] N=5  steps=12000  time=0.0005 s  (~24,000,000 steps/s)
```

versus ~123 000 steps/s for the NumPy loop in the notebook — roughly **200× faster**, same closed orbits.
The gap widens with N because there is no per-step Python dispatch at all.

## 2. Why a GPU backend at all, and the unified-memory point

Your earlier worry — "we lose time loading to GPU and reading back each step" — is a **discrete-GPU**
problem. On the M4 the CPU and GPU **share the same physical RAM (unified memory)**. MLX arrays are not
copied to a separate device; the GPU reads the same bytes. So the per-step transfer cost that sank the
old per-vector torch code does not exist here as long as you keep the data in MLX arrays and only call
`eval()` to compute. You copy out only the handful of positions you actually draw, every K steps.

That said, at small N the GPU still loses to the CPU (kernel-launch overhead dominates tiny arrays).
The GPU backend is the right tool once N is in the thousands (galaxy-scale, your §6.4 goal).

## 3. GPU linear-algebra options on MacBook Air M4 — comparison

| Option | What it is | System-vector fit | Effort | Verdict |
|---|---|---|---|---|
| **MLX** (`mlx::core`) | Apple's NumPy-like array framework, Metal backend, **unified memory**, lazy eval, C++/Python/Swift APIs | **Excellent** — broadcasting kernel is ~10 lines, mirrors NumPy | Low (`pip install mlx`, one `find_package`) | **Chosen.** Best ergonomics + native M-series perf for array code |
| **metal-cpp** + custom `.metal` kernel | Apple's official low-level C++ bindings to Metal | Good — you hand-write a tiled N-body compute shader (canonical max-perf approach) | High (manage device/buffers/pipeline/shaders) | Best raw control; pick it only when MLX's generic kernels aren't enough |
| **Accelerate / BLAS** (CPU) | Apple's tuned CPU BLAS/LAPACK | N/A for GPU; pairwise isn't a BLAS op | Low | CPU only — Eigen already covers this tier |
| **Vulkan + MoltenVK** | Cross-platform compute over Metal | Possible but not LA-shaped | Very high | Overkill; only if you need one GPU path across vendors |
| **OpenCL** | Old cross-vendor compute | — | — | **Avoid** — deprecated by Apple |
| **SYCL / Kokkos** | Portability layers | — | — | No first-class Apple-GPU backend today |

**Recommendation: MLX as the GPU backend, Eigen as the CPU backend.** MLX is made by Apple for Apple
silicon, array-native (your `accel` is a near-verbatim port), uses unified memory, and installs in one
line. Keep **metal-cpp** in your back pocket for a hand-tuned tiled kernel if you later need to push past
what MLX's generic ops deliver — `docs/INSTALL_metal-cpp.md` covers that path.

## 4. Build (VSCodium + CMake)

```bash
brew install eigen cmake          # CPU backend deps
pip install -U mlx                # GPU backend (Apple silicon only)

cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

./build/eigen_backend             # CPU, runs anywhere
./build/mlx_backend               # GPU, Apple silicon (built only if MLX found)
```

In VSCodium install the **CMake Tools** extension; it reads `CMakeLists.txt` directly — pick a Clang/AppleClang
kit and press Build. The MLX backend needs the **Metal toolchain from Xcode** (`xcode-select --install` gives
the command-line tools; the full Metal shader compiler ships with Xcode). See the per-library docs:

- [docs/INSTALL_eigen.md](docs/INSTALL_eigen.md)
- [docs/INSTALL_mlx.md](docs/INSTALL_mlx.md)
- [docs/INSTALL_metal-cpp.md](docs/INSTALL_metal-cpp.md)

## 5. Notes / next steps
- Initial conditions are hardcoded in `nbody_common.hpp` to keep the backends dependency-free. Swap in a
  TOML reader (`toml++` via `brew install toml11`/FetchContent) to load `nbody/system.toml` directly.
- Integrator is semi-implicit Euler to match the notebook. Promote to leapfrog (energy-conserving, ~3 lines)
  or wire the Adams-Bashforth coefficients from `num.ipynb`.
- For N≫10⁴, switch the CPU kernel to Barnes-Hut and/or hand-write a tiled Metal kernel via metal-cpp.
