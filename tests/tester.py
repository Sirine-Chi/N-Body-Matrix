import csv
import datetime
import os
import sys
from pathlib import Path
from data_manager import TableManager
import yaml
import nbody.n_body_lib as nbl

# FIXME: THIS IS NOT A GOOD WAY OF DOING THINGS!!!
# WE NEED NEXT TWO LINE OF CODE ONLY FOR TEMPORARY LAUNCHING tests/tester.py
# IN THE FUTURE ANOTHER WAY OF TESTING SHOULD BE PROVIDED!
ROOT_DIR = str(Path(os.path.abspath(__file__)).parent.parent)
sys.path.append(ROOT_DIR)

# --- --- GENERATING DATA --- ---

# gen.write_table(gen.spherical_sc(100, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0))

# --- --- SETTINGS --- ---

stream = open("nbody/config.yaml", "r")
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


for i in range(2, 50, 2):
    system = nbl.pd.read_csv("nbody/systems_data/Table.csv")
    system = system[0:i]
    N = len(system)
    objects = TableManager.format_table(system)

    delta_cur = 0
    inum = "s"

    # NOTE: Should there be any plots in the correspondig directory?
    # Because there are none for now


    directory = "nbody/Plots/Simulation/" + str(datetime.datetime.now()).replace(
        ":", "-"
    )
    os.mkdir(directory)

    # FIXME: I still couldn't figure out how we are actually supposed
    # to format the file, so it doesn't really works

    results = open(directory + "/Results.txt", "w")
    results.writelines(config)
    results.writelines("\n")

    results.writelines("\n".join(map(lambda x: str(x), objects)))
    results.write("All saved in " + directory)
    results.close()

    # print(N, calc_time, "\n")
    # with open(r"Testing/Time loop.csv", "a") as ta:
    #     writer = csv.writer(ta)
    #     writer.writerow([N, calc_time])
    # test_data._append([N, calc_time], ignore_index=True)
    # results.close()

print("finish!", "\n", "All saved in ", directory)
# time_data = nbl.pd.DataFrame(test_data)
