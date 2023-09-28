import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from n_body_lib import *


def dist_check():
    r = 0
    delta = 10
    values= []
    for i in range (0,  1000):
        values.append( float(abs(np.random.normal(r, delta, size=1))))

    print(f"1 {values}")
    # values2 = np.random.standard_normal(1000)
    # print(f"2 {values2}")

    plt.clf()
    plt.hist(values, bins=len(values)//10)
    plt.show()

def dist_check_2d():
    r = 10
    values = []
    for i in range (0, 1000):
        values.append(list(ranrv(10)))
    print(values)
    
    plt.clf()
    plt.hist(
        list(v(values).reshape(2*len(values), 1)),
        bins=len(values)//10
        )
    plt.show()

dist_check_2d()
