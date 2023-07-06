import nbody.NBodyLib as nbl
import matplotlib.pyplot as plt
import Generator as gen
import datetime3
import sys
import csv
import os
import yaml
original_stdout = sys.stdout

# --- --- GENERATING DATA --- ---

# gen.write_table(gen.spherical_sc(100, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))

# --- --- SETTINGS --- ---

stream = open("Config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)
for key, value in config.items():
    print(key + ":   " + str(value))
mode = config["Mode"]
method = config["Method"]
end_time = float(config["End time"])
time_step = float(config["Time step"])
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

# test_data = nbl.pd.DataFrame([])
# test_data.to_csv("Time loop.csv", index=False) # header=["Number of objects", "Time"],

# --- --- LOOP FOR SIMULATIONS, getting T, N from each --- ---

for i in range(100, 102, 2):
    system = nbl.pd.read_csv('Table.csv')
    system = system[0:i]
    N = len(system)
    objects = nbl.format_table(system)

    directory = '/Users/ilyabelov/PycharmProjects/N-body/Plots/Simulation/' + str(datetime3.datetime.now())
    os.mkdir(directory)
    with open(directory + '/Results.txt', 'w') as file:
        sys.stdout = file
        # ms = gen.formatting(objects)  # форматирование под матрицы
        delta_cur = 0
        inum = 's'
        print(*objects, sep="\n")  # ПЕЧАТАТЬ С РАЗДЕЛИТЕЛЕМ \n
        print('mode =', mode, '  method =', method)
        print('All saved in ', directory)
        print('N =', N, '  time_direction =', time_direction, '  end_time =', end_time, '  time_step =', time_step,
              '  delta_cur =', delta_cur, '  inum =', inum, '  pulse_table =', pulse_table)
        calc_time = nbl.simul(method, objects, time_direction, end_time, time_step, delta_cur, inum, pulse_table, 0, directory)
        # calc_time = nbl.simulation(method, ms, time_direction, end_time, time_step)
    sys.stdout = original_stdout
    print(N, calc_time, "\n")
    with open(r"Testing/Time loop.csv", 'a') as ta:
        writer = csv.writer(ta)
        writer.writerow([N, calc_time])
    # test_data._append([N, calc_time], ignore_index=True)
    file.close()

print('finish!', "\n",'All saved in ', directory)
# time_data = nbl.pd.DataFrame(test_data)
