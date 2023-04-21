import Matrix_3 as mx

config = open('Config.txt', 'r')

mode = mx.nbl.find_value_by_name('Mode', config)
method = mx.nbl.find_value_by_name('Method', config)

N = mx.nbl.count_objects('obj_', config)

end_time = int(float( mx.nbl.find_value_by_name('End_time', config) ))
time_step = float( mx.nbl.find_value_by_name('Time_step', config) )
time_direction = int( mx.nbl.find_value_by_name('Time_direction', config) )
#pulse_table = bool(int( mx.nbl.find_value_by_name('Pulse_table', config) ))
config.close()

system = open('System.txt', 'r')
objects = mx.nbl.format_objects('obj_', system)
system.close()
print(*objects, sep = "\n") #ПЕЧАТАТЬ С РАЗДЕЛИТЕЛЕМ \n
print('========= ^ Config Content ^ =========')


method = 'e'
s = mx.gn.spherical(N, [1, 1], 3, 0, 2, 0.4, [0.2, 0.3], 0.1, 0)
ms = mx.gn.formatting(objects)
dir = 1
end = 1
h = 10e-3

mx.simulation(method, ms, dir, end, h)