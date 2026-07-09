// eigen_backend.cpp — CPU backend.
// Whole system held as one contiguous (N,3) matrix; force kernel is a tight
// pairwise loop (NO (N,N,3) temporary — in C++ the explicit loop is faster and
// O(N) memory). This is the direct C++ analogue of the NumPy system-vector.
//
// Build: see cpp/CMakeLists.txt  (needs Eigen3 — docs/INSTALL_eigen.md)

#include <Eigen/Dense>
#include <chrono>
#include <iostream>
#include "nbody_common.hpp"

using Mat = Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>;  // (N,3)
using Vec = Eigen::VectorXd;

// a[i] = G * sum_{j!=i} m_j (r_j - r_i) / (|r_j-r_i|^2 + eps^2)^{3/2}
static Mat accel(const Mat& pos, const Vec& mass, double G, double eps2) {
    const int N = static_cast<int>(pos.rows());
    Mat a = Mat::Zero(N, 3);
    for (int i = 0; i < N; ++i) {
        Eigen::RowVector3d ai = Eigen::RowVector3d::Zero();
        for (int j = 0; j < N; ++j) {
            if (i == j) continue;
            const Eigen::RowVector3d d = pos.row(j) - pos.row(i);
            const double r2  = d.squaredNorm() + eps2;
            const double inv = 1.0 / (r2 * std::sqrt(r2));   // r2^{-1.5}
            ai += (G * mass(j) * inv) * d;
        }
        a.row(i) = ai;
        // (Newton's 3rd law could halve this: a[j] -= m_i/m_j * contribution.)
    }
    return a;
}

int main() {
    const auto sys = nbody::solar_inner();
    const int N = sys.size();

    Mat pos(N, 3), vel(N, 3);
    Vec mass(N);
    for (int i = 0; i < N; ++i) {
        pos.row(i) << sys.pos[i][0], sys.pos[i][1], sys.pos[i][2];
        vel.row(i) << sys.vel[i][0], sys.vel[i][1], sys.vel[i][2];
        mass(i) = sys.mass[i];
    }

    const double h = 1e-4, eps2 = 1e-6;
    const int n_steps = 12000, record_every = 100;

    nbody::Frames frames;
    auto t0 = std::chrono::steady_clock::now();
    for (int s = 0; s < n_steps; ++s) {
        const Mat a = accel(pos, mass, nbody::G, eps2);
        vel += h * a;          // semi-implicit Euler (same as the notebook)
        pos += h * vel;
        if (s % record_every == 0) {
            nbody::Frame f(N);
            for (int i = 0; i < N; ++i) f[i] = {pos(i, 0), pos(i, 1)};
            frames.push_back(std::move(f));
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    const double secs = std::chrono::duration<double>(t1 - t0).count();

    std::cout << "[eigen/CPU] N=" << N << "  steps=" << n_steps
              << "  time=" << secs << " s  ("
              << n_steps / secs << " steps/s)\n";
    std::cout << "Earth final: " << pos.row(1) << "\n\n";
    nbody::ascii_plot(frames, sys.names);
    return 0;
}
