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

        # FOR ADAMS
        self.r.append(v(self.r[0] + dt * self.v[0]))
        self.v.append(v(self.v[0] + dt * self.f[0] / self.m))
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
        # devider = 1
        # devider = int(devider)
        x_s0 = []
        y_s0 = []
        for i in self.r:
            x_s0.append(i[0])
            y_s0.append(i[1])
            # x_s0 = x_s0[::devider]
            # y_s0 = y_s0[::devider]
        return [x_s0, y_s0]

    def reper(self, n):
        self.r[n] = self.r[n] - system[0].r[n]


class DynamicObject(Object):
    def iteration(self, system, n, dt):
        # Objects which trajectory deternined by others with force
        def eiler_method(fs, vs, rs, m):
            vs.append(eiler(vs[n - 1], (fs[n - 1] / m), dt))
            rs.append(eiler(rs[n - 1], vs[n], dt))

        def midpoint_method(fs, vs, rs, ms):
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

def simul(method, objects: list[Object], dir, end, dt, delta_cur, inum, pulse_table, field, dir_n):
    simulation_time = time.time()

    def f12(obj1, obj2, n):  # Force between first and second given objects on time step n. Uses lambda f_ij
        return f_ij(obj1.r[n - 1], obj2.r[n - 1], obj1.m, obj2.m)

    def f(obj, system, n):  # Sum of forces affected on given object in system on time step n. Uses lambda f_ij
        obj.fn = []
        for other in system:
            if obj != other:
                obj.fn.append(f12(obj, other, n))
        return vsum(obj.fn)
        obj.fn.clear()

    enn = int(end / dt)
    dt = dir * dt

    system = []
    for ob in objects:
        # system.append(object( ob[1], ob[2]+ranrv(delta_cur), ob[3], ob[4], system, ob[6].replace("'", '') ))
        system.append(DynamicObject(ob[1], ob[2] + ranrv(delta_cur), ob[3], system, ob[4].replace("'", ''), ob[5]))

    if field == True:
        inum = 'f'
        delta_cur = 0
        Vis.vis_field(U_matrix(system, 0), system, inum, delta_cur, dir_n)  # 0 is case of n

    # --define function for pulse---
    if pulse_table == True:
        def Pn(system, n):
            ps = []
            for ob in system:
                ps.append(ob.Ps[n - 1])
            return scal(vsum(ps))

    # ---Iterator---
    for n in range(2, enn):
        # dtn = dt #FOR DYNAMIC TIME STEP!!!
        # Star.iter(galaxy, n, dt)
        for ss in system:
            ss.iteration(system, n, dt)
            ss.reper(n)
            # ss.print_object() #вывести всё про точку

    # ---PULSE TABLE---
    if pulse_table == True:
        PS = []  # Добавляем в список значения полного импульса с итераций
        for n in range(0, enn):
            PS.append(Pn(galaxy, n))
        tP = pd.DataFrame(
            {
                "t": galaxy[0].t,
                "P": PS
            })
        tP.to_csv('tP.csv')
        print(PS[1] - PS[-1])

    print('sim num= ' + str(inum) + ' ', 'delta= ' + str(delta_cur) + ' ')

    print('Finished!', 'simulation time')
    timee = time.time() - simulation_time
    print("--- %s seconds ---" % (timee))
    return timee

    print('Vis is turned off')
    # Vis.vis_N_2D(system, inum, delta_cur, 'Progons', dir_n)
    # MAIN VISUALISER CALL!!!!! ^^^^

    if field == True:
        Vis.vis_N_2D(system, inum, delta_cur, 'Field', dir_n)
    # Vis.vis_N_3D(galaxy).show
    # Vis.vis_N_anim(galaxy, enn).save('Galaxy.gif', writer='imagemagic', fps=60)

class Simulation:
    def __init__(self):
