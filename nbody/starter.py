import datetime
import os

import generator as gn
import n_body_lib as nbl
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# Importing and initialising libraries for colored terminal
import colorama

colorama.just_fix_windows_console()
colorama.init()
from colorama import Back, Fore, Style

# Set enviromental variable to don't manualy choose device during runtime
os.environ["PYOPENCL_CTX"] = "0"


def print_config(config):
    for key, value in config.items():
        print(Fore.YELLOW, key + ":   " + str(value), Style.RESET_ALL)


def write_config(config, results):
    for key, value in config.items():
        results.write(key + ":   " + str(value) + "\n")


print("[] [] [] MATRIX VERSION RUNNING [] [] []")

# Writing values from config dictionary to variables, converting types
stream = open("nbody/config.yaml", "r")
config = yaml.load(stream, Loader=yaml.FullLoader)
print_config(config)
mode = config["Mode"]
method = config["Method"]
end_time = float(config["End time"])
time_step = float(config["Time step"])
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

system = nbl.pd.read_csv("nbody/systems_data/Solar System.csv")
system = system[0:2]
print(Style.DIM, system, Style.RESET_ALL)
N = len(system)
objects = nbl.format_table(system)

print("========= ^ Config Content ^ =========")

if mode == "Simulation":
    directory = (
        "nbody/Results/GPU_Simulations/" + str(datetime.datetime.now())
    ).replace(":", "-")
    os.mkdir(directory)
    results = open(directory + "/Results.txt", "w")
    write_config(config, results)
    results.write("All saved in " + directory)
    results.close()

    nbl.simulation(
        method, objects, time_direction, end_time, time_step
    )  # Run simulation with config settings

# sys.stdout = original_stdout
print(Fore.GREEN, Style.DIM, "\a\n", "All saved in ", directory, Style.RESET_ALL)
colorama.deinit()
