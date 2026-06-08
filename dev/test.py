from mylinal import Array
from matplotlib import pyplot as plt

vecs: list = []
for i in range (1, 1000):
    v = Array.randarr_less_than_lenght(lenght=1, dimensions=2).give_list()
    vecs.append(v)


# plt.imshow(vecs, cmap='hot', interpolation='nearest')

plt.xlim = (-10, 10)
plt.ylim = (-10, 10)
plt.scatter(vecs[0], vecs[1])
plt.show()

