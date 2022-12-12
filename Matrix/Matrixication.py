import pyopencl as cl
import numpy as np
import numpy.linalg as la

def scal(v): #Модуль (скаляр, длиннна) вектора
    return (v[0]**2 + v[1]**2)**0.5
def v(v1): #вектор
    v = np.array(v1)
    return v
def unvec(v): #еденичный вектор
    uv = v / scal(v)
    return uv
def dist(v1, v2): #расстояние между двумя точками (концами векторов v1 и v2)
    return scal(v1-v2)
def v12(v1, v2):
    return (v2-v1)
def v12(v2, v1):
    return (v1-v2)
def ranvec(r): #Случайный радиус-вектор длинны r
    rv = v(  [uniform(-r, r), 2*(getrandbits(1)-0.5) *(r**2 - uniform(-r, r)**2)**0.5]  )
    return rv
def ranrv(r): #Случайный радиус-вектор длинны r
    a = uniform(0, 2*math.pi)
    rr = uniform(0, r)
    rv = v( [rr*math.cos(a), rr*math.sin(a)]  )
    return rv

def openCL_multiplication(matrix1, matrix2, res):

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
    b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix1.nbytes )


    prg = cl.Program(ctx, """
        __kernel void multiplymatrices(const unsigned int size, __global float * matrix1, __global float * matrix2, __global float * res) {
    
        int i = get_global_id(1); 
        int j = get_global_id(0);
    
        res[i + size * j] = 0;
    
        for (int k = 0; k < size; k++)
        {
            res[i + size * j] += matrix1[k + size * i] * matrix2[j + size * k];
        }
    
        }
        """).build()
    #res[i + size * j] += matrix1[i + size * k] * matrix2[k + size * j];

    t0 = datetime.datetime.now()

    prg.multiplymatrices(queue, matrix1.shape, None,np.int32(len(matrix1)) ,a_buf, b_buf, dest_buf)

    final_matrix = np.empty_like(matrix1)
    cl.enqueue_copy(queue, final_matrix , dest_buf)

    print( final_matrix )

    delta_t = datetime.datetime.now() - t0
    print( 'OpenCL Multiplication: ' + str(delta_t) )

    return final_matrix

matrix1 = v([[0.99114645, 0.09327769, 0.90075564, 0.8913309],
           [0.59739089, 0.13906649, 0.94246316, 0.65673178],
           [0.24535166, 0.68942326, 0.41361505, 0.5789603],
           [0.31962237, 0.17714553, 0.49025267, 0.21861202]] )

matrix2 = v( [[0.99114645, 0.09327769, 0.90075564, 0.8913309],
          [0.59739089, 0.13906649, 0.94246316, 0.65673178],
          [0.24535166, 0.68942326, 0.41361505, 0.5789603],
          [0.31962237, 0.17714553, 0.49025267, 0.21861202]] )

res = v( [[1.57981943, 1.63210835, 2.12016045, 1.80288424],
       [1.3391085, 1.15248911, 1.7403561, 1.58199609],
       [1.31099532, 0.70041376, 1.20338154, 1.14162762],
       [0.71769556, 0.52246746, 0.88158722, 0.8039138]] )

openCL_multiplication(matrix1, matrix2, res)