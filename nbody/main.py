from simulator import SimulatorCPU
from data_manager import ConfigManager, TableManager, Report
from n_body_lib import *
import os
import sys
from datetime3 import datetime


def main():
    """
    Simple CPU simulation example
    """

    path_to_yaml = 'nbody/Config.yaml'
    path_to_table = 'nbody/systems_data/Solar System.csv'
    path_to_results = 'nbody/Results/CPU_Simulations' + '/' + str(datetime.now()).replace(':', '-')

    os.mkdir(path_to_results)
    config = ConfigManager(path_to_yaml).get_config(path_to_yaml)
    table = TableManager.get_table_sliced(path_to_table, 0, 2)

    report = Report()
    report.add_to_report(config)  # , logger.trace(config)
    report.add_to_report({'Number of objects': len(table)})

    particles_f = TableManager.format_table_dicts(table)

    sim = SimulatorCPU(particles_f, config['End time'], config["Time step"])
    for _ in tqdm(sim.simulation(), desc="Runtime", ncols=100):
        pass
    sim.vis(path_to_results)
    # log.add_to_log(sim.get_last_positions())
    report.add_to_report({'Runtime': sim.get_runtime()})
    print('REPORT: ')
    report.print_report_to_console()
    # report.save_report_to_txt(path_to_report=path_to_results)
    report.save_report_to_yaml(path_to_report=path_to_results)
    print(sim.get_last_positions())


if __name__ == '__main__':
    main()
