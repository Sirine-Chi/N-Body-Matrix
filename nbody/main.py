from simulator import Simulator, SimulatorCPU
from data_manager import ConfigManager, TableManager, Logger
from n_body_lib import *
import os
import sys
from datetime3 import datetime


def main():
    path_to_yaml = 'nbody/Config.yaml'
    path_to_table = 'nbody/systems_data/Solar System.csv'
    path_to_results = 'nbody/Results/CPU_Simulations' + '/' + str(datetime.now()).replace(':', '-')
    os.mkdir(path_to_results)
    config = ConfigManager.get_config(path_to_yaml=path_to_yaml)
    table = TableManager.get_table_sliced(path_to_table, 0, 5)

    log = Logger()
    log.add_to_log(config)  # , logger.trace(config)
    log.add_to_log({'Number of objects': len(table)})

    particles_f = TableManager.format_table_dicts(table)

    sim = SimulatorCPU(particles_f, config['End time'], config["Time step"])
    sim.simulation()
    for element in sim.particles:
        print(f'{element.name}: {element.get_last_position()}')
    sim.vis(path_to_results)
    # log.add_to_log(sim.get_last_positions())
    # log.add_to_log(sim.get_runtime())
    print('LOG: '), log.print_log_to_console()
    # log.save_log_to_txt(path_to_log=path_to_results)


if __name__ == '__main__':
    main()
