# Installing metal-cpp (low-level GPU alternative)

[metal-cpp](https://developer.apple.com/metal/cpp/) is Apple's **header-only** C++ interface to Metal.
Unlike MLX it gives you no array math — you write the GPU compute kernel yourself in a `.metal` shader and
drive it from C++. Use it only if you want a hand-tuned tiled N-body kernel (the canonical max-performance
approach) and MLX's generic ops aren't enough. For everyday system-vector work, prefer MLX.

> Apple silicon only. Needs **Xcode** (not just command-line tools) because you compile `.metal` shaders.

## Prerequisites

```bash
xcode-select --install                                   # command-line tools
# plus full Xcode from the App Store, then:
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
xcrun -sdk macosx metal --version                        # confirm the Metal compiler
brew install cmake
```

## Download the headers

1. Go to <https://developer.apple.com/metal/cpp/> and download the metal-cpp ZIP that matches your macOS.
2. Extract it into the project, e.g. `cpp/third_party/metal-cpp/`.

It's header-only: `Foundation/`, `Metal/`, `QuartzCore/` subfolders of `.hpp` files. C++17 minimum.

### Optional single-header

```bash
cd metal-cpp
./SingleHeader/MakeSingleHeader.py Foundation/Foundation.hpp QuartzCore/QuartzCore.hpp Metal/Metal.hpp
# -> ./SingleHeader/Metal.hpp
```

## One translation unit must define the implementation

In exactly **one** `.cpp` file, before including the headers:

```cpp
#define NS_PRIVATE_IMPLEMENTATION
#define CA_PRIVATE_IMPLEMENTATION
#define MTL_PRIVATE_IMPLEMENTATION
#include <Foundation/Foundation.hpp>
#include <Metal/Metal.hpp>
#include <QuartzCore/QuartzCore.hpp>
```

## CMake integration

metal-cpp needs the headers on the include path and three Apple frameworks linked:

```cmake
add_executable(metal_backend src/metal_backend.cpp)          # your code + a .metal kernel
target_include_directories(metal_backend PRIVATE third_party/metal-cpp)
target_compile_features(metal_backend PRIVATE cxx_std_17)
target_link_libraries(metal_backend PRIVATE
  "-framework Foundation" "-framework Metal" "-framework QuartzCore")
```

Compile the shader separately into a `.metallib` and load it at runtime:

```bash
xcrun -sdk macosx metal   -c kernels/nbody.metal -o nbody.air
xcrun -sdk macosx metallib  nbody.air            -o nbody.metallib
```

A community CMake helper that automates the headers + single-header generation is
[`cmake-metal-cpp`](https://github.com/arauzca/cmake-metal-cpp): copy its `metal-cmake/` dir, then
`add_subdirectory(metal-cmake)` and `target_link_libraries(<target> METAL_CPP)`.

## Build & run

```bash
cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target metal_backend
./build/metal_backend
```

## VSCodium

**CMake Tools** extension, AppleClang kit. Building `.metal` shaders is done by the `xcrun` calls above (or
a custom CMake command), so a working full-Xcode install is required — verify with
`xcrun -sdk macosx metal --version` before configuring.

## When to choose this over MLX

| Want | Use |
|---|---|
| NumPy-style array code, fast to write, unified memory | **MLX** |
| A hand-written tiled kernel, shared-memory blocking, every last GFLOP | **metal-cpp** |
| Both — prototype in MLX, then drop a metal-cpp kernel into the hot path | layer them |
