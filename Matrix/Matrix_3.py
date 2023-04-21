import numpy as np
import NBodyLib as nbl
import Generator as gn
import datetime
import time

G = 0.0001184069#09138

def gravec(r1, r2): #единичный вектор направления силы, действующей на тело, делённый на квадрат расстояния
    # r1, r2 - коордирнаты тел
    d = nbl.dist(r1, r2)
    #print(d)
    if d == 0.0:
        return nbl.v([0, 0])
    else:
        #print('Dev', r2-r1)
        return nbl.v((r2 - r1) / d**3)

def unit_vectors_matrix(position_vectors): #расчёт матрицы единичных векторов сил, действующих от тела j на тело i
    matrix = []
    for j in position_vectors:
        line = []
        for i in position_vectors:
            #print('gravec', gravec(i, j))
            line.append(gravec(i, j))
            #print('line', line)
        matrix.append(line)
    #print('rs_m', matrix, 'rs_m end')
    return nbl.v(matrix)

def simulation(method, matrices, dir, end, h):
    test1_time = time.time()

    r_sys_mx = []
    v_sys_mx = []
    a_sys_mx = []
    #метод эйлера
    v_sys_mx.append(matrices[3])
    r_sys_mx.append(matrices[2])
    # print('poses ', unit_vectors_matrix(matrices[2]))
    # print('invs ', matrices[1])
    a_sys_mx.append(( G*(matrices[0]).dot((matrices[1]).dot(unit_vectors_matrix(matrices[2]))) )[0])
    #print('s 0')

    num = int(end / h) #количесвто шагов
    for i in range(1, num):
        a_sys_mx.append(( G*(matrices[0]).dot((matrices[1]).dot(unit_vectors_matrix(r_sys_mx[i-1]))) )[0])
        v_sys_mx.append(v_sys_mx[i-1] + h*a_sys_mx[i])
        r_sys_mx.append(r_sys_mx[i-1] + h*v_sys_mx[i])
        #print('s ', i)

    print('test1_time')
    print("--- %s seconds ---" % (time.time() - test1_time))