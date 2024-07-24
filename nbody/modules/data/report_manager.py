from data_manager import YamlManager, parallel

class Report:
    """
    Class to work with report, that stores values as dictionary
    """
    def __init__(self):
        """
        Class constructor
        """
        self.report_dict = {}

    def add_to_report(self, item: dict) -> None:
        """
        Adds any object to log 
        \n
        :param: item: dict | any number of any objects, that we add to log
        """
        for key in item.keys():
            self.report_dict[key] = item[key]
        # recursive_writer(iterable_object=text, func=log_append)

    def get_report(self) -> list:
        return self.report_dict
    
    def print_report_to_console(self) -> None:
        for item in parallel(self.report_dict):
            print(item)

    def save_report_to_txt(self, path_to_report: str) -> None:
        with open(path_to_report + '/report.txt', 'w', encoding='utf-8') as file:
            for item in parallel(self.report_dict):
                if isinstance(item[0], list) or isinstance(item, tuple):
                    for element in item:
                        file.write(str(element) + ', ')
                else:
                    file.write(str(item)[1:-1] + '\n')

    def save_report_to_yaml(self, path_to_report: str) -> None:
        YamlManager.save_to_yaml(self.report_dict, path_to_report, file_name="report.yaml")