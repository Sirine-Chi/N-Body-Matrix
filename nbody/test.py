from mylinal import np, Mx

ap = np.array( ((0.7, 1.2), (3.0, 4.0)) )
bp = np.array( ((1.0, 2.0), (0.1, 0.3)) )

a = Mx(ap)
b = Mx(bp)

c = a + b
print(c)
