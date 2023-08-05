import n_body_lib as nbl
from datetime3 import datetime
import os
import sys
import yaml
import colorama
from colorama import Fore, Back, Style

colorama.just_fix_windows_console()
colorama.init()

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
original_stdout = sys.stdout


def print_config(config):
    for key, value in config.items():
        print(Fore.YELLOW, key + ":   " + str(value), Style.RESET_ALL)


def write_config(config, results):
    for key, value in config.items():
        results.write(key + ":   " + str(value) + "\n")


print("~~~~~~ CLASSIC VERSION IS RUNNING ~~~~~~")

stream = open("nbody/Config.yaml", "r")
config = yaml.load(stream, Loader=yaml.FullLoader)
print_config(config)
mode = config["Mode"]
method = config["Method"]
end_time = config["End time"]
time_step = config["Time step"]
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

system = nbl.pd.read_csv("nbody/systems_data/Solar System.csv")
system = system[0:2]
# with open('nbody/systems_data/Solar System.csv') as st:
#     system_csv = from_csv(st)
# x = from_csv(system_csv)
# print(x)
print(Style.DIM, system, Style.RESET_ALL)
N = len(system)
objects = nbl.format_table(system)

print("========= ^ Config Content ^ =========")

if mode == "Simulation":
    directory = "nbody/Results/CPU_Simulations/" + str(datetime.now()).replace(":", "-")
    os.mkdir(directory)
    with open(directory + "/Results.txt", "w") as results:
        write_config(config, results)
        results.write(f"All saved in {directory}")

    nbl.simul(
        method,
        objects,
        time_direction,
        end_time,
        time_step,
        delta_cur=0,
        inum="s",
        pulse_table=0,
        field=0,
        dir_n=directory,
    )

if mode == "Progons":
    directory = "/nbody/Results/CPU_Stability/" + str(datetime.now())
    os.mkdir(directory)
    with open(directory + "/Results.txt", "w") as f:
        sys.stdout = f

        print("mode =", mode, "  method =", method, "\n")

        progons_per_delta = int(config["Progons per delta"])
        delta_start = float(config["Delta start"])
        delta_end = float(config["Delta end"])
        delta_step = float(config["Delta step"])

        print("All saved in ", directory, "\n")
        print(
            "N =",
            N,
            "  time_direction =",
            time_direction,
            "  end_time =",
            end_time,
            "  time_step =",
            time_step,
            "  pulse_table =",
            pulse_table,
        )
        print(
            "Delta step =",
            delta_step,
            "  Delta start =",
            delta_start,
            "  Delta end =",
            delta_end,
            "Progons per delta =",
            progons_per_delta,
        )
        nbl.progons(
            method,
            objects,
            time_direction,
            end_time,
            time_step,
            delta_step,
            progons_per_delta,
            delta_start,
            delta_end,
            pulse_table,
            directory,
        )  # +force_function

    f.close()

if mode == "Field":
    directory = "/nbody/Results/CPU_Field/" + str(datetime.now())
    os.mkdir(directory)
    with open(directory + "/Results.txt", "w") as f:
        sys.stdout = f

        print("mode = ", mode, "  method =", method)
        delta_cur = 0
        inum = "s"
        print("All saved in ", directory)
        print(
            "N =",
            N,
            "  time_direction =",
            time_direction,
            "  end_time =",
            end_time,
            "  time_step =",
            time_step,
            "  delta_cur =",
            delta_cur,
            "  inum =",
            inum,
            "  pulse_table =",
            pulse_table,
        )

        nbl.simul(
            method,
            objects,
            time_direction,
            end_time,
            time_step,
            delta_cur,
            inum,
            pulse_table,
            bool(1),
        )

    f.close()

sys.stdout = original_stdout
print(Fore.GREEN, f"\nAll saved in {directory}", Style.RESET_ALL)
colorama.deinit()
