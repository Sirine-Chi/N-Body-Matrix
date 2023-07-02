import NBodyLib as nbl
import Generator as gn
import datetime3
import sys
import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
original_stdout = sys.stdout

print('[] [] [] MATRIX VERSION RUNNING [] [] []')

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

system = nbl.pd.read_csv('System.csv')
N = len(system)
objects = nbl.format_table(system)

print('========= ^ Config Content ^ =========')


if mode == "Simulation":
    dir_n = '/Users/ilyabelov/PycharmProjects/N-body/Plots/Simulation/' + str(datetime3.datetime.now())
    os.mkdir(dir_n)
    with open(dir_n + '/Results.txt', 'w') as file:
        sys.stdout = file

        method = 'e'
        delta_cur = 0
        inum = 's'
        print('mode =', mode, '  method =', method)
        print('All saved in ', dir_n)
        print('N =', N, '  time_direction =', time_direction, '  end_time =', end_time, '  time_step =', time_step,
              '  delta_cur =', delta_cur, '  inum =', inum, '  pulse_table =', pulse_table)
        ms = gn.formatting(objects) # форматирование под матрицы
        dir = time_direction
        end = end_time
        h = time_step
        nbl.simulation(method, ms, dir, end, h)
        # запуск симуляции с параметрами из конфига
    file.close()

sys.stdout = original_stdout
print('finish!')
print('All saved in ', dir_n)