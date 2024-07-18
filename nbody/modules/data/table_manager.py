from pandas import read_csv, DataFrame
from datetime3 import datetime

class TableManager:
    """
    Class to work with configuration tables
    """

    @staticmethod
    def get_table_sliced(path_to_table: str, limit_down=0, limit_up=100) -> DataFrame:
        """
        Reads table from files, gives away table, sliced from one object to other
        """

        table = read_csv(path_to_table)
        return table[limit_down:limit_up]

    @staticmethod
    def format_table_dicts(table: DataFrame) -> list[dict]:
        """
        returns list of dicts containing object initialisation parameters
        """

        dicts = []
        for line in table.to_numpy():
            dicts.append(
                {
                    'name': str(line[0]),
                    'type': str(line[1]),
                    'mass': float(line[2]),
                    'start_position': list(map(float, line[3].split())),
                    'start_velocity': list(map(float, line[4].split())),
                    'color': str(line[5])
                }
            )
        return dicts

    @staticmethod
    def write_to_table(objects_data, path_to_table):
        names = ["Name", "Type", "Mass", "R (polar)", "V (polar)", "Color"]
        tab = DataFrame(data=objects_data)
        tab.to_csv(path_to_table + "/" + str(datetime.now()).replace(":", "-") + 'Generated Table.csv', header=names, index=False)
