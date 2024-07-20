from generator import TableGenerator
from nbody.modules.data.table_manager import TableManager
from nbody.modules.linal.mylinal import Array

# TODO make more global class

class Command():
    def simulation(self, path_to_config, path_to_results_folder):
        pass

    def benchmark(self):
        pass

    def benchmark_n(self):
        self.benchmark()

    def generate_table(self):

        # TODO incapsulate this

        my_pattern = {
            "number of objects": 1000,
            "center": Array.new_mx_from_list([0.0, 0.0, 0.0]),
            "medium radius": 50.0,
            "crit radius delta": 0.0,
            "medium mass": 10.0,
            "crit mass delta": 0.0,
            "mass center velocity": Array.new_mx_from_list([0.0, 0.0, 0.0]),
            "medium velocity scalar": 2.0,
            "velocity crit delta": 0.0
            }

        gen = TableGenerator()
        TableManager.write_to_table(objects_data=TableGenerator.spherical(gen, pattern=my_pattern), path_to_table="nbody/data_tables")

c = Command()
c.generate_table()
