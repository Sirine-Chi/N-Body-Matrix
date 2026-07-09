// mlx_backend.cpp — GPU backend via Apple MLX (Metal).
// Mirrors the NumPy broadcasting kernel 1:1. On Apple silicon MLX uses UNIFIED
// MEMORY, so there is no host<->device copy each step — exactly the problem the
// old per-vector torch code suffered from. Arrays live where they are; we only
// mx::eval() to force computation and copy a few positions out to draw.
//
// Build: see cpp/CMakeLists.txt  (needs MLX — docs/INSTALL_mlx.md)

#include <mlx/mlx.h>
#include <chrono>
#include <iostream>
#include "nbody_common.hpp"

namespace mx = mlx::core;

// a = G * sum_j  (r_j - r_i) * m_j / (|r_j-r_i|^2 + eps^2)^{3/2}
// pos: (N,3)  mass: (N,)  ->  (N,3)
static mx::array accel(const mx::array& pos, const mx::array& mass,
                       float G, float eps) {
    auto d   = mx::subtract(mx::expand_dims(pos, 0),   // (1,N,3)
                            mx::expand_dims(pos, 1));   // (N,1,3) -> (N,N,3)
    auto r2  = mx::add(mx::sum(mx::square(d), -1), mx::array(eps * eps)); // (N,N)
    auto inv = mx::power(r2, mx::array(-1.5f));                            // (N,N)
    auto m   = mx::reshape(mass, {1, (int)mass.size(), 1});               // (1,N,1)
    auto contrib = mx::multiply(mx::multiply(mx::expand_dims(inv, -1), d), m); // (N,N,3)
    return mx::multiply(mx::sum(contrib, 1), mx::array(G));                // (N,3)
}

int main() {
    const auto sys = nbody::solar_inner();
    const int N = sys.size();

    std::vector<float> p, v, m;
    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < 3; ++k) { p.push_back(sys.pos[i][k]); v.push_back(sys.vel[i][k]); }
        m.push_back((float)sys.mass[i]);
    }
    auto pos  = mx::array(p.data(), {N, 3}, mx::float32);
    auto vel  = mx::array(v.data(), {N, 3}, mx::float32);
    auto mass = mx::array(m.data(), {N},    mx::float32);

    const float h = 1e-4f, eps = 1e-3f;
    const int n_steps = 12000, record_every = 100;

    nbody::Frames frames;
    auto t0 = std::chrono::steady_clock::now();
    for (int s = 0; s < n_steps; ++s) {
        auto a = accel(pos, mass, nbody::G, eps);
        vel = mx::add(vel, mx::multiply(mx::array(h), a));
        pos = mx::add(pos, mx::multiply(mx::array(h), vel));
        mx::eval(pos, vel);                 // bound the lazy graph each step
        if (s % record_every == 0) {
            mx::array host = mx::contiguous(pos);
            mx::eval(host);
            const float* d = host.data<float>();
            nbody::Frame f(N);
            for (int i = 0; i < N; ++i) f[i] = {d[i * 3 + 0], d[i * 3 + 1]};
            frames.push_back(std::move(f));
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    const double secs = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "[mlx/GPU] N=" << N << "  steps=" << n_steps
              << "  time=" << secs << " s  (" << n_steps / secs << " steps/s)\n\n";
    nbody::ascii_plot(frames, sys.names);
    return 0;
}
