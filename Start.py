import NBodyLib as nbl

config = open('config.txt', 'r')

def find_line(name, c_file):
    lines = c_file.readlines()
    for line in lines:
        if line.find(name) != -1:
            return (line)
        # else:
        #     print('Error in config reading \n check directory or format')
        #     return(lines[-1])
def find_value_by_name(name, c_file):
    c_file.seek(0,0)
    line = find_line(name, c_file)
    st = line.find('(')+1
    en = line.find(')')
    var_value = line[st:en]
    return var_value
def list_of_objects(index, c_file):
    c_file.seek(0,0)
    lines = c_file.readlines()
    list_of_objects = []
    for line in lines:
        if line.find(index) != -1:
            list_of_objects.append(line)
        # else:
        #     print("Error in config reading \n maybe there is no objects")
    return list_of_objects
def count_objects(index, c_file):
    return len(list_of_objects(index, c_file))
def format_objects(index, c_file):
    list = list_of_objects(index, c_file)
    values = []
    objs = []
    for line in list:
        line = line.replace(' ', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.replace(')', '')
        line = line.replace('\n', '')
        sk = line.find('(')+1
        line = line[sk:len(line)]
        line_vals = line.split(',')

        obj_vals = []
        obj_vals.append(line_vals[0]) #name
        obj_vals.append( float(line_vals[1]) ) #mass
        obj_vals.append( [float(line_vals[2]), float(line_vals[3])] ) #r0 as vec
        obj_vals.append( [float(line_vals[4]), float(line_vals[5])] ) #v0 as vec
        obj_vals.append(int(line_vals[6])) #id
        obj_vals.append(line_vals[7]) #system, DOESN'T MATTERS!!!
        obj_vals.append(line_vals[8]) #colour

        objs.append(obj_vals)
        print(obj_vals)
    return objs

mode = find_value_by_name('Mode', config)
# force_function =
method = find_value_by_name('Method', config)

N = count_objects('obj_', config)

end_time = int(float( find_value_by_name('End_time', config) ))
time_step = float( find_value_by_name('Time_step', config) )
time_direction = int( find_value_by_name('Time_direction', config) )
pulse_table = bool(int( find_value_by_name('Pulse_table', config) ))

objects = format_objects('obj_', config)

if mode == 'Simulation':
    print('mode =', mode)
    delta_cur = 0
    inum = 's'
    print('N =',N,'  time_direction =',time_direction,'  end_time =',end_time,'  time_step =',time_step,'  delta_cur =',delta_cur,'  inum =',inum,'  pulse_table =',pulse_table)
    nbl.simul(objects, N, time_direction, end_time, time_step, delta_cur, inum, pulse_table) #+force_function

if mode == 'Progons':
    print('mode = ', mode)

    progons_per_delta = 1
    delta_r = 0
    nbl.progons(dur, end, dt, delta_step, k, delta_start, delta_end, pulse_table) #+force_function

# if mode == 'Field':
#     print('mode = ', mode)
    #nbl.field_simulation(force_function, N, end_time, time_step, list_of_objects, )


