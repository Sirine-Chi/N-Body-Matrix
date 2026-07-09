# Installing MLX (GPU backend, Apple silicon)

[MLX](https://github.com/ml-explore/mlx) is Apple's array framework for Apple silicon, with a C++ API
(`mlx::core`) that mirrors NumPy and runs on the GPU through Metal using **unified memory**. This is the
chosen GPU backend. **Apple silicon only** (M1–M4); it will not build on Intel Macs / Linux / Windows,
which is why `CMakeLists.txt` builds it conditionally.

## Prerequisites

1. **macOS 13.5+** on an M-series chip (your M4 qualifies).
2. **Xcode command-line tools** (compiler + Metal toolchain):
   ```bash
   xcode-select --install
   ```
   For the full Metal **shader compiler** (needed when MLX builds its Metal kernels from source), install
   **Xcode** from the App Store, then point the toolchain at it once:
   ```bash
   sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
   xcodebuild -version          # confirm
   ```
   The prebuilt `pip` wheel below already contains compiled Metal kernels, so for most users the
   command-line tools alone are enough — you only need full Xcode if you build MLX from source.
3. **CMake ≥ 3.27** and **Python ≥ 3.9**:
   ```bash
   brew install cmake
   ```

## Install MLX (recommended: pip wheel)

```bash
pip install -U mlx
```

This ships the prebuilt C++ library *and* a CMake config. Confirm it works and is on the GPU:

```bash
python -c "import mlx.core as mx; print(mx.default_device()); print((mx.array([1,2,3])+1))"
# -> Device(gpu, 0)
python -m mlx --cmake-dir          # prints the path CMake will use
```

## How CMake finds it

`cpp/CMakeLists.txt` already does the standard MLX dance (from the official C++ guide): it asks your
Python for MLX's CMake dir, then `find_package(MLX CONFIG)`. So as long as the **same Python** that has
MLX installed is the one CMake picks up, no manual paths are needed:

```cmake
find_package(Python 3.9 COMPONENTS Interpreter Development.Module)
execute_process(COMMAND "${Python_EXECUTABLE}" -m mlx --cmake-dir
                OUTPUT_VARIABLE MLX_ROOT OUTPUT_STRIP_TRAILING_WHITESPACE)
find_package(MLX CONFIG REQUIRED)
target_link_libraries(mlx_backend PRIVATE mlx)
```

If you use a virtualenv, configure CMake with it so the right interpreter is found:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release -DPython_EXECUTABLE=$(which python)
```

## Build & run

```bash
cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target mlx_backend
./build/mlx_backend
```

Expected: a timing line and the same nested-orbit ASCII plot as the Eigen backend. At N=5 it will be
*slower* than Eigen (GPU launch overhead on tiny arrays) — that's expected; the GPU wins at large N.

## Alternative: build MLX from source (needs full Xcode)

```bash
git clone https://github.com/ml-explore/mlx.git
cd mlx && mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DMLX_BUILD_METAL=ON
make -j && sudo make install        # installs to a system prefix CMake can find
```

## VSCodium

Install **CMake Tools**. Because MLX is discovered through your Python interpreter, either launch VSCodium
from a shell where that env is active, or set `"cmake.configureSettings": {"Python_EXECUTABLE": "..."}` in
`.vscode/settings.json`. Pick an AppleClang kit. If the configure step prints
`MLX not found - skipping mlx_backend`, MLX isn't visible to the chosen Python — fix that and re-configure.

## Troubleshooting

- **`MLX not found`** → `pip install -U mlx`, and make sure CMake's `Python_EXECUTABLE` is the env that has it.
- **`Device(cpu)` instead of gpu** → your wheel was built without Metal, or you're on an Intel Mac. Reinstall on Apple silicon.
- **Metal compiler errors building from source** → install full Xcode and run the `xcode-select -s` line above.
