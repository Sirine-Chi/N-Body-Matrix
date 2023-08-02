import numpy as np

def binarize(i):
    new = list(bin(1))
    new.reverse()
    for element in new:
        if not element in {'0', '1'}:
            new.remove(element)
        else:
            element = int(element)
    return new

def subset_i(set: list, i: int) -> list:
    # generating binary number
    set_len = len(set)
    b = binarize(i)
    while len(b) < set_len:
        b.append(0)
    
    combo = []
    for l in range (0, set_len):
        combo.append( [b[l], set[l]] )
    print(combo)
    
    subset = []
    # adding elements to set
    for element in combo:
        if element[0] == 1:
            subset.append(element[1])
    
    return subset

hi = [1, 2, 3]

print('>>>>', subset_i(hi, 4))