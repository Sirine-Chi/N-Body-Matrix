from data_manager import YamlManager

class ConfigManager:
    """
    Class to work with config
    """
    def __init__(self, path_to_config: str) -> None:
        self.config: dict = YamlManager.get_yaml(path_to_yaml=path_to_config)

    def get_config(self) -> dict:
        return self.config
    
    def print_config_to_console(self):
        YamlManager.print_yaml(self.config)
    
    # def save_config_to_txt(self, path_to_txt: str, file_name="config.txt"):
    #     YamlManager.save_yaml_to_txt(self, path_to_txt, file_name)
