import NBodyLib as nbl

config = open('config.txt', 'r')

mode = nbl.find_value_by_name('Mode', config)
# force_function =
method = nbl.find_value_by_name('Method', config)

N = nbl.count_objects('obj_', config)

end_time = int(float( nbl.find_value_by_name('End_time', config) ))
time_step = float( nbl.find_value_by_name('Time_step', config) )
time_direction = int( nbl.find_value_by_name('Time_direction', config) )
pulse_table = bool(int( nbl.find_value_by_name('Pulse_table', config) ))

objects = nbl.format_objects('obj_', config)
print(*objects, sep = "\n") #ПЕЧАТАТЬ С РАЗДЕЛИТЕЛЕМ \n

if mode == 'Simulation':
    print('mode =', mode, '  method =', method)
    delta_cur = 0
    inum = 's'
    print('N =',N,'  time_direction =',time_direction,'  end_time =',end_time,'  time_step =',time_step,'  delta_cur =',delta_cur,'  inum =',inum,'  pulse_table =',pulse_table)
    nbl.simul(method, objects, N, time_direction, end_time, time_step, delta_cur, inum, pulse_table, 0) #+force_function

if mode == 'Progons':
    print('mode =', mode, '  method =', method)

    progons_per_delta = int( find_value_by_name('Progons_per_delta', config) )
    delta_start = float( find_value_by_name('Delta_start', config) )
    delta_end = float( find_value_by_name('Delta_end', config) )
    delta_step = float( find_value_by_name('Delta_step', config) )

    #КАКИЕ ФЙЛЫ СОХРАНИЛИСЬ? СОЗДАВАТЬ НОВУЮ ДИРЕКТОРИЮ ПО ВРЕМЕНИ ЗАПУСКА ПРОГОНОВ
    print('N =',N,'  time_direction =',time_direction,'  end_time =',end_time,'  time_step =',time_step,'  pulse_table =',pulse_table)
    print('Delta step =',delta_step,'  Delta start =',delta_start,'  Delta end =',delta_end,'Progons per delta =',progons_per_delta)
    nbl.progons(method, objects, N, time_direction, end_time, time_step, delta_step, progons_per_delta, delta_start, delta_end, pulse_table) #+force_function

if mode == 'Field':
    print('mode = ', mode, '  method =', method)
    delta_cur = 0
    inum = 's'
    print('N =',N,'  time_direction =',time_direction,'  end_time =',end_time,'  time_step =',time_step,'  delta_cur =',delta_cur,'  inum =',inum,'  pulse_table =',pulse_table)

    nbl.simul(method, objects, N, time_direction, end_time, time_step, delta_cur, inum, pulse_table, bool(1))
