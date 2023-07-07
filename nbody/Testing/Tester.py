import nbody.NBodyLib as nbl
import matplotlib.pyplot as plt
import Generator as gen
import datetime3
import sys
import csv
import os
import yaml

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

    delta_cur = 0
    inum = 's'

    directory = '/Plots/Simulation/' + str(datetime3.datetime.now()).replace(':', '-')
    os.mkdir(directory)

    results = open(directory + '/Results.txt', 'w')
    results.writelines(config)
    results.writelines(*objects, sep="\n")
    results.write('All saved in ' + directory)
    results.close()

    print(N, calc_time, "\n")
    with open(r"Testing/Time loop.csv", 'a') as ta:
        writer = csv.writer(ta)
        writer.writerow([N, calc_time])
    # test_data._append([N, calc_time], ignore_index=True)
    file.close()

print('finish!', "\n",'All saved in ', directory)
# time_data = nbl.pd.DataFrame(test_data)
