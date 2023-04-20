import Matrix_3 as mx

method = 'e'
ms = mx.format()
N = 20
dir = 1
end = 1
h = 10e-4

mx.simulation(method, ms, N, dir, end, h)