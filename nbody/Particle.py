import n_body_lib as nbl

class Object:
    # Has two underclasses, each real object from table can be initialised as one of them, or as both.
    def __init__(self, m, r0, v0, system, colour, start_angle, *args, **kwargs):
        self.colour = colour
        self.start_angle = start_angle
        self.m = m
        self.r0 = v(r0)
        self.v0 = v(v0)
        self.r = []
        self.v = []
        self.f = []
        self.t = []

        self.r.append(rotvec(r0, start_angle))
        self.v.append(rotvec(v0, start_angle))
        self.t.append(0)
        self.f.append(f(self, system, 1))

        # FOR ADAMS, first iteration with eiler method
        self.r.append(v(self.r[0] + step * self.v[0]))
        self.v.append(v(self.v[0] + step * self.f[0] / self.m))
        self.t.append(1)
        self.f.append(f(self, system, 2))

        if pulse_table == True:
            self.Ps = []
            self.Ps.append(v(self.v[0] * self.m))
            self.Ps.append(v(self.v[1] * self.m))

    def print_object(self):
        print("id=" + str(self.i), self.m, "f" + str(self.f), "v" + str(self.v), "r" + str(self.r),
            "t" + str(self.t))

    def print_object_coor(self):
        print("id=" + str(self.i), self.r)

    def makeXY(self):
        x_s0 = []
        y_s0 = []
        for i in self.r:
            x_s0.append(i[0])
            y_s0.append(i[1])
        return [x_s0, y_s0]

        def reper(self, n):
            self.r[n] = self.r[n] - system[0].r[n]

class DynamicObject(Object):
    def iteration(self, system, n, dt):
        # Objects which trajectory deternined by others with force
        def eiler_method(fs, vs, rs, m):
            vs.append(eiler(vs[n - 1], (fs[n - 1] / m), dt))
            rs.append(eiler(rs[n - 1], vs[n], dt))

        def midpoint_method(fs, vs, rs, m):
            vs.append(v(vs[n - 1] + dt * f(rs[n - 1] + dt / 2 * f(rs[n - 1])) / m))  # Midpoint
            rs.append(v(rs[n - 1] + dt / 2 * (vs[n - 1] + vs[n - 2])))

        def adams_method(fs, vs, rs, m):
            vs.append(adams(vs[n - 1], (fs[n - 1] / m), (fs[n - 2] / m), dt))
            rs.append(adams(rs[n - 1], (vs[n - 1] / m), (vs[n - 2] / m), dt))
            # vs.append(v(vs[n - 1] + dt / 2 * (3 * fs[n] / m - fs[n - 1] / m)))
            # rs.append(v(rs[n - 1] + dt / 2 * (3 * vs[n] - vs[n - 1])))

        self.t.append(self.t[n - 1] + dt)
        self.f.append(f(self, system, n))

        eiler_method(self.f, self.v, self.r, self.m)
        # midpoint_method(self.f, self.v, self.r, self.m)

        if pulse_table == True:
            self.Ps.append(v(self.v[n] * self.m))

class AnalyticObject(Object):
    # Object, on which others don't affect, which is going on it's own independent trajectory
    # But others feel it's force
    def iteration(self, n, dt):
        self.t.append(self.t[n - 1] + dt)
        self.v.append(analytic_f(self.r0, self.v0, (n * dt))[1])
        self.r.append(analytic_f(self.r0, self.v0, (n * dt))[0])
    