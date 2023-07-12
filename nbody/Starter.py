import n_body_lib as nbl
import generator as gn
import datetime3
import logging
import sys
import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def print_config(config):
    for key, value in config.items():
        print(key + ":   " + str(value))

print('[] [] [] MATRIX VERSION RUNNING [] [] []')

stream = open("Config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)
print_config(config)
mode = config["Mode"]
method = config["Method"]
end_time = float(config["End time"])
time_step = float(config["Time step"])
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

system = nbl.pd.read_csv('systems_data/Solar System.csv')
system = system[0:2]
N = len(system)
objects = nbl.format_table(system)

print('========= ^ Config Content ^ =========')


if mode == "Simulation":
    directory = ('nbody/Results/Simulations/' + str(datetime3.datetime.now())).replace(':', '-')
    os.mkdir(directory)
    results = open(directory + '/Results.txt', 'w')
    results.writelines(config)
    results.write('All saved in ' + directory)
    results.close()

    nbl.simulation(method, objects, time_direction, end_time, time_step) # Run simulation with config settings

# sys.stdout = original_stdout
print('Finish!', '\n', 'All saved in ', directory)
