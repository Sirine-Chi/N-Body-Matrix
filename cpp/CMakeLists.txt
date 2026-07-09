cmake_minimum_required(VERSION 3.27)
project(nbody_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# ---------------------------------------------------------------------------
# CPU backend — Eigen (header-only). Always built.
#   brew install eigen   (see docs/INSTALL_eigen.md)
# ---------------------------------------------------------------------------
find_package(Eigen3 3.4 REQUIRED NO_MODULE)

add_executable(eigen_backend src/eigen_backend.cpp)
target_link_libraries(eigen_backend PRIVATE Eigen3::Eigen)
target_include_directories(eigen_backend PRIVATE src)

# ---------------------------------------------------------------------------
# GPU backend — MLX (Metal). Built only when MLX is found, so the project still
# configures on Linux/Windows where MLX is absent.
#   pip install -U mlx   (see docs/INSTALL_mlx.md)
# Point CMake at MLX installed in your active Python env:
# ---------------------------------------------------------------------------
option(NBODY_BUILD_MLX "Build the MLX GPU backend" ON)

if(NBODY_BUILD_MLX)
  find_package(Python 3.9 COMPONENTS Interpreter Development.Module)
  if(Python_FOUND)
    execute_process(
      COMMAND "${Python_EXECUTABLE}" -m mlx --cmake-dir
      OUTPUT_STRIP_TRAILING_WHITESPACE
      OUTPUT_VARIABLE MLX_ROOT
      RESULT_VARIABLE MLX_QUERY_RESULT)
  endif()

  find_package(MLX CONFIG QUIET)
  if(MLX_FOUND)
    add_executable(mlx_backend src/mlx_backend.cpp)
    target_link_libraries(mlx_backend PRIVATE mlx)
    target_include_directories(mlx_backend PRIVATE src)
    message(STATUS "MLX found - building mlx_backend (Metal GPU)")
  else()
    message(STATUS "MLX not found - skipping mlx_backend. "
                   "Run `pip install -U mlx` and re-configure (see docs/INSTALL_mlx.md).")
  endif()
endif()
