import NBodyLib as nbl
import Generator as gn
import datetime3
import logging
import sys
import os
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
original_stdout = sys.stdout

def print_config(config):
    for key, value in config.items():
        print(key + ":   " + str(value))

print('[] [] [] MATRIX VERSION RUNNING [] [] []')

stream = open("nbody/Config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)
print_config(config)
mode = config["Mode"]
method = config["Method"]
end_time = float(config["End time"])
time_step = float(config["Time step"])
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

system = nbl.pd.read_csv('nbody/systems_data/Solar System.csv')
N = len(system)
objects = nbl.format_table(system)

print('========= ^ Config Content ^ =========')


if mode == "Simulation":
    directory = '/Users/ilyabelov/PycharmProjects/N-Body/nbody/Results/Simulations' + str(datetime3.datetime.now())
    os.mkdir(directory)
    # results = open(directory + '/Results.txt', 'w')
    # results.writelines(config)
    # results.close()

    with open(directory + '/Results.txt', 'w') as file:
        sys.stdout = file

        print('All saved in ', directory)
        print_config(config)
        
        ms = gn.formatting(objects) # Making special matrices from objects
        nbl.simulation(method, ms, time_direction, end_time, time_step) # Run simulation with config settings
    file.close()

sys.stdout = original_stdout
print('Finish!', '\n', 'All saved in ', directory)
