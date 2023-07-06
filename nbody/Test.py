import math, numpy, time

def sina():
    start = time.time()
    s = numpy.sqrt(34)
    p = math.pi
    return(s, p, str(time.time()-start))


def sinb():
    start = time.time()
    s = math.sqrt(34)
    p = math.pi
    return(s, p, str(time.time()-start))

print(sina(), "\n", sinb())
