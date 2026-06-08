import csv
from matplotlib import pyplot as plt

def read_csv(path):
    numbers = []
    times = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            numbers.append( row['N'] )
            times.append( float( row['Time'] ) )
    return [numbers, times]


n_np_1 = read_csv('liiiiist.csv')[0]
t_np_1 = read_csv('liiiiist.csv')[1]

n_np_2 = read_csv('liiiiist_np.csv')[0]
t_np_2 = read_csv('liiiiist_np.csv')[1]

n_np_3 = read_csv('list_np_2.csv')[0]
t_np_3 = read_csv('list_np_2.csv')[1]

n_torch_1 = read_csv('liiiiist_torch.csv')[0]
t_torch_1 = read_csv('liiiiist_torch.csv')[1]

n_torch_2 = read_csv('list_torch_2.csv')[0]
t_torch_2 = read_csv('list_torch_2.csv')[1]

plt.grid(axis='x', color='0.95')

# plt.plot( n_np_1, t_np_1, color = 'blue', label = 'numpy 1' )
# plt.scatter(n_np_1, t_np_1, color = 'blue')

plt.plot( n_np_2, t_np_2, color = 'dodgerblue', label = 'numpy 2' )
# plt.scatter(n_np_2, t_np_2, color = 'dodgerblue')

plt.plot( n_np_3, t_np_3, color = 'royalblue', label = 'numpy 3' )
# plt.scatter(n_np_3, t_np_3, color = 'royalblue')

plt.plot( n_torch_1, t_torch_1, color = 'green', label = 'torch 1' )
# plt.scatter(n_torch_1, t_torch_1, color = 'green')

plt.plot( n_torch_2, t_torch_2, color = 'lightgreen', label = 'torch 2' )
# plt.scatter(n_torch_1, t_torch_1, color = 'lightgreen')

plt.xlabel('Number of objects')
plt.ylabel('Time')

plt.legend()
plt.show()
