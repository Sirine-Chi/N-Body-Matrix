from nbody.modules.generator import TableGenerator
from nbody.modules.data.table_manager import TableManager
from nbody.modules.data.data_manager import YamlManager
# from nbody.modules.core.mylinal import Array

# TODO make more global class

class Command():

    # --- --- --- --- --- General

    def hello(self):
        """
        A short guide to basics of an app and interface
        """
        pass

    def version(self):
        """
        Gives acess to version and general program data
        """
        DEFAULT_INFO_PATH = 'nbody/info.yaml'
        return YamlManager.get_yaml(DEFAULT_INFO_PATH)
    
    def load(self):
        pass

    def generate(self):
        pass

    def generate_table(self):
        gen = TableGenerator()
        TableManager.write_to_table(objects_data=TableGenerator.spherical(gen), path_to_table="nbody/data_tables")


    # --- --- --- --- --- Simulation


    def simulation(self, path_to_config, path_to_results_folder):
        pass

    def simulation_series(self, path_to_config, path_to_results_folder):
        pass


    # --- --- --- --- --- Benchmark

    def benchmark(self):
        pass

    def benchmark_n(self):
        self.benchmark()

    
c = Command()
c.generate_table()
