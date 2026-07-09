# Installing Eigen (CPU backend)

Eigen is a **header-only** C++ linear-algebra library. Nothing to compile or link — CMake just needs to
find the headers. Cross-platform (macOS / Linux / Windows), which keeps this backend runnable by everyone.

## macOS (your M4) — Homebrew

```bash
brew install eigen
```

Installs headers under `/opt/homebrew/include/eigen3` and a CMake config so `find_package(Eigen3)` works
with zero extra flags.

## Linux

```bash
sudo apt install libeigen3-dev      # Debian/Ubuntu
# or: sudo dnf install eigen3-devel  (Fedora)
```

## Windows

```powershell
vcpkg install eigen3
# then configure with: -DCMAKE_TOOLCHAIN_FILE=<vcpkg>/scripts/buildsystems/vcpkg.cmake
```

## Dependency-free alternative (any OS, no package manager)

Eigen is just headers, so you can vendor them via CMake FetchContent — drop this into `CMakeLists.txt`
instead of `find_package(Eigen3 ...)`:

```cmake
include(FetchContent)
FetchContent_Declare(Eigen
  GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
  GIT_TAG 3.4.0)
set(EIGEN_BUILD_DOC OFF)
set(BUILD_TESTING OFF)
FetchContent_MakeAvailable(Eigen)
# target_link_libraries(eigen_backend PRIVATE Eigen3::Eigen)  # still works
```

## Build & run

```bash
cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target eigen_backend
./build/eigen_backend
```

Expected: a timing line and an ASCII plot of nested closed orbits (Sun at center). Closed loops = the
integrator is reliable.

## VSCodium

Install the **CMake Tools** extension. Open the `cpp/` folder, pick an AppleClang/Clang kit when prompted,
then use the Build button (or `cmake --build` in the integrated terminal). No Xcode needed for this backend
— command-line tools (`xcode-select --install`) are enough for the C++ compiler.

## Verify the install

```bash
ls $(brew --prefix eigen)/include/eigen3/Eigen/Dense   # macOS
cmake -B build -DCMAKE_BUILD_TYPE=Release               # should print: Eigen3 found
```
