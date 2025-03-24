import pyopencl as cl
import numpy as np
from mydatatypes import timer

PYOPENCL_CTX='0'

"""
# FIXME make functions
"""

# --- --- --- --- --- DATA

# Define matrix dimensions
rows = 10000
cols = 10000

# Create host matrices
a_host = np.random.rand(rows, cols).astype(np.float32)
b_host = np.random.rand(rows, cols).astype(np.float32)

# --- --- --- --- --- SUM FUNC

@timer
def add_cl(a: np.array, b: np.array) -> np.array:
    c_host = np.zeros((rows, cols), dtype=np.float32)

    # Initialize OpenCL context
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # Define the OpenCL kernel for matrix addition
    kernel_code = """
    __kernel void matrix_add(__global const float *a,
                            __global const float *b,
                            __global float *c,
                            const int rows,
                            const int cols) {
    int i = get_global_id(0);
    int j = get_global_id(1);

    if (i < rows && j < cols) {
        c[i * cols + j] = a[i * cols + j] + b[i * cols + j];
    }
    }
    """

    # Create the OpenCL program
    program = cl.Program(ctx, kernel_code).build()

    # Create OpenCL buffers
    mf = cl.mem_flags
    a_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a_host)
    b_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b_host)
    c_device = cl.Buffer(ctx, mf.WRITE_ONLY, c_host.nbytes)

    # Execute the OpenCL kernel
    program.matrix_add(queue, (rows, cols), None, a_device, b_device, c_device, np.int32(rows), np.int32(cols))

    # Read the result from the device to the host
    cl.enqueue_copy(queue, c_host, c_device).wait()

    return c_host

@timer
def sum_np(a_host, b_host):
    return a_host + b_host

# Print the results
print("Matrix A:")
print(a_host)
print("\nMatrix B:")
print(b_host)
print("\nMatrix C (A + B):")
res = add_cl(a_host, b_host)
# print(res)

#Verify the result
print("\nNumpy result:")
res_np = sum_np(a_host, b_host)
# print(res_np)

print("\nResult verification:", np.allclose(res, res_np))
