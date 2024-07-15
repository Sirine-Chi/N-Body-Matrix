from pandas import read_csv, DataFrame

class TableManager:
    """
    Class to work with configuration tables
    """

    @staticmethod
    def get_table_sliced(path_to_table: str, limit_down=0, limit_up=-1) -> DataFrame:
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
                    'mass': line[2],
                    'start_position': v([line[3], line[4], line[5]]),
                    'start_velocity': v([line[6], line[7], line[8]]),
                    'color': str(line[9]),
                    'start_angle': line[10]
                }
            )
        return dicts