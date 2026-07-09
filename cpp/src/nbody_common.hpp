// nbody_common.hpp — shared initial conditions, constants, and a tiny ASCII
// trajectory plotter. Backend-agnostic: no Eigen / MLX types appear here, so
// both backends include this and only differ in the force kernel + loop.
#pragma once
#include <array>
#include <string>
#include <vector>
#include <cmath>
#include <cstdio>
#include <utility>

namespace nbody {

constexpr double G = 0.0001184069;  // same constant as the Python mymath.py

using Vec3 = std::array<double, 3>;

struct System {
    std::vector<std::string> names;
    std::vector<Vec3>        pos;   // initial positions
    std::vector<Vec3>        vel;   // initial velocities
    std::vector<double>      mass;
    int size() const { return static_cast<int>(names.size()); }
};

// Inner solar system (Sun + 4 planets), matching nbody/system.toml.
// Hardcoded so the backends need zero parsing dependencies; swap in a TOML
// loader (toml++ / toml11) later if you want to read system.toml directly.
inline System solar_inner() {
    return System{
        {"Sun", "Earth", "Mercury", "Venus", "Mars"},
        {{0,0,0}, {1.0167257,0,0}, {0.4667045,0,0}, {0.72822561,0,0}, {1.66620687,0,0}},
        {{0,0,0}, {0,6.174482536,0}, {0,8.19188772,0}, {0,7.333910803,0}, {0,4.631388915,0}},
        {332840, 1, 0.0553, 0.815, 0.107},
    };
}

// One recorded frame = (x, y) of every body. Backends fill this every K steps.
using Frame  = std::vector<std::pair<double, double>>;
using Frames = std::vector<Frame>;

// Simplest possible terminal visualiser — same idea as the Python ascii_plot.
// Closed loops => reliable integration. Spirals / escapes => step too big.
inline void ascii_plot(const Frames& frames,
                       const std::vector<std::string>& names,
                       int width = 70, int height = 28) {
    if (frames.empty()) return;
    double xmin=1e300, xmax=-1e300, ymin=1e300, ymax=-1e300;
    for (const auto& f : frames)
        for (const auto& p : f) {
            xmin = std::min(xmin, p.first);  xmax = std::max(xmax, p.first);
            ymin = std::min(ymin, p.second); ymax = std::max(ymax, p.second);
        }
    if (xmax == xmin) { xmax += 1; xmin -= 1; }
    if (ymax == ymin) { ymax += 1; ymin -= 1; }
    std::vector<std::string> g(height, std::string(width, ' '));
    auto cell = [&](double x, double y, int& cx, int& cy) {
        cx = int((x - xmin) / (xmax - xmin) * (width - 1));
        cy = height - 1 - int((y - ymin) / (ymax - ymin) * (height - 1));
    };
    const int N = static_cast<int>(names.size());
    for (int j = 0; j < N; ++j) {
        int cx, cy;
        for (const auto& f : frames) {                       // trail
            cell(f[j].first, f[j].second, cx, cy);
            if (g[cy][cx] == ' ') g[cy][cx] = '.';
        }
        const auto& last = frames.back()[j];                 // current position
        cell(last.first, last.second, cx, cy);
        g[cy][cx] = names[j].empty() ? '0' : names[j][0];
    }
    std::string bar = "+" + std::string(width, '-') + "+";
    std::printf("%s\n", bar.c_str());
    for (const auto& row : g) std::printf("|%s|\n", row.c_str());
    std::printf("%s\n", bar.c_str());
    for (const auto& n : names) std::printf("%c=%s  ", n[0], n.c_str());
    std::printf("\n");
}

} // namespace nbody
