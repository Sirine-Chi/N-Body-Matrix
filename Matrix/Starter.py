import Matrix_3 as mx
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

print('[] [] [] MATRIX VERSION RUNNING [] [] []')

stream = open("Config.yaml", 'r')
config = yaml.load(stream, Loader=yaml.FullLoader)
for key, value in config.items():
    print(key + ":   " + str(value))
mode = config["Mode"]
method = config["Method"]
end_time = float(config["End time"])
time_step = float(config["Time step"])
time_direction = config["Time direction"]
pulse_table = config["Pulse table"]

system = mx.nbl.pd.read_csv('System.csv')
system = system[0:2]
N = len(system)
objects = mx.nbl.format_table(system)

print('========= ^ Config Content ^ =========')

method = 'e'
ms = mx.gn.formatting(objects) #форматирование под матрицы
dir = time_direction
end = end_time
h = time_step

mx.simulation(method, ms, dir, end, h)
#запуск симуляции, с параметрами из конфига