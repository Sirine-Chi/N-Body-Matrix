import pyopencl as cl
import numpy as np
from mydatatypes import timer

PYOPENCL_CTX='0'

"""
# FIXME make functions

Ideas: write euler as one kerlnel
and force as one kernel
"""

def add_cl(a: np.array, b: np.array) -> np.array:
    """
    Adds two matrices using OpenCL for parallel computation.

    Args:
        a (np.array): The first input matrix.
        b (np.array): The second input matrix.

    Returns:
        np.array: The resulting matrix after addition.

    Raises:
        TypeError: If the input matrices have different dimensions.

    Example:
        >>> a = np.array([[1, 2], [3, 4]], dtype=np.float32)
        >>> b = np.array([[5, 6], [7, 8]], dtype=np.float32)
        >>> add_cl(a, b)
        array([[ 6.,  8.],
            [10., 12.]], dtype=float32)
    """

    a_rows = np.size(a, axis=0)
    a_cols = np.size(a, axis=1)

    b_rows = np.size(b, axis=0)
    b_cols = np.size(b, axis=1)

    if a_rows != b_rows or a_cols != b_cols:
        raise TypeError(f"Matrices have different dimensions: \nA: {a_rows}:{b_rows}, B: {a_cols}:{b_cols}")
    else:
        rows = a_rows
        cols = a_cols

        c = np.zeros((rows, cols), dtype=np.float32)

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
        a_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
        b_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
        c_device = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

        # Execute the OpenCL kernel
        program.matrix_add(queue, (rows, cols), None, a_device, b_device, c_device, np.int32(rows), np.int32(cols))

        # Read the result from the device to the host
        cl.enqueue_copy(queue, c, c_device).wait()

        return c

def sub_cl(a:np.array, b:np.array) -> np.array:
    """
    Matrix substraction using OpenCL.
    Args:
        a (np.array): The first input numpy array.
        b (np.array): The second input numpy array to be subtracted from the first.
    Returns:
        np.array: The result of the subtraction (a - b).
    """
    
    return add_cl(a, -b)

def hadamar_cl(a: np.array, b:np.array) -> np.array:
    """
    Compute the Hadamard product (element-wise multiplication) of two matrices using OpenCL.

    Args:
        a (np.array): The first input matrix.
        b (np.array): The second input matrix.

    Returns:
        np.array: The resulting matrix after performing the Hadamard product.

    Raises:
        TypeError: If the input matrices have different dimensions.
    
    Example:
        >>> a = np.array([[1, 2], [3, 4]], dtype=np.float32)
        >>> b = np.array([[5, 6], [7, 8]], dtype=np.float32)
        >>> hadamar_cl(a, b)
        array([[ 5., 12.],
               [21., 32.]], dtype=float32)

    """

    a_rows = np.size(a, axis=0)
    a_cols = np.size(a, axis=1)

    b_rows = np.size(b, axis=0)
    b_cols = np.size(b, axis=1)

    if a_rows != b_rows or a_cols != b_cols:
        raise TypeError(f"Matrices have different dimensions: \nA: {a_rows}:{a_cols}, B: {b_rows}:{b_cols}")
    else:
        rows = a_rows
        cols = a_cols

        c = np.zeros((rows, cols), dtype=np.float32)

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)

        mf = cl.mem_flags
        a_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
        b_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
        c_device = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

        kernel_code = """
        __kernel void hadamard_product(__global const float *a,
                                        __global const float *b,
                                        __global float *c,
                                        const int rows,
                                        const int cols) {
        int i = get_global_id(0);
        int j = get_global_id(1);

        if (i < rows && j < cols) {
            c[i * cols + j] = a[i * cols + j] * b[i * cols + j];
        }
        }
        """

        program = cl.Program(ctx, kernel_code).build()
        program.hadamard_product(queue, (rows, cols), None, a_device, b_device, c_device, np.int32(rows), np.int32(cols))
        cl.enqueue_copy(queue, c, c_device).wait()

        return c

def dot_cl(a:np.array, b:np.array) -> np.array:
    """
    Perform matrix dot multiplication using OpenCL.
    Args:
        a (np.array): The first input matrix with dimensions (a_rows, a_cols).
        b (np.array): The second input matrix with dimensions (b_rows, b_cols).
    Returns:
        np.array: The resulting matrix after multiplication with dimensions (a_rows, b_cols).
    Raises:
        TypeError: If the dimensions of the input matrices are not compatible for multiplication.
    """

    a_rows = np.size(a, axis=0)
    a_cols = np.size(a, axis=1)

    b_rows = np.size(b, axis=0)
    b_cols = np.size(b, axis=1)

    if (a_rows != b_cols) or (a_cols != b_rows):
        raise TypeError(f"Matrices have unpropper dimensions: \nA: {a_rows}:{a_cols}, B: {b_rows}:{b_cols}")
    else:
        c = np.zeros((a_rows, b_cols), dtype=np.float32)

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)

        mf = cl.mem_flags
        a_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
        b_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
        c_device = cl.Buffer(ctx, mf.WRITE_ONLY, c.nbytes)

        kernel_code = """
        __kernel void matrix_dot(__global const float *a,
                                __global const float *b,
                                __global float *c,
                                const int a_rows,
                                const int a_cols,
                                const int b_cols) {
        int row = get_global_id(0);
        int col = get_global_id(1);

        if (row < a_rows && col < b_cols) {
            float sum = 0.0f;
            for (int k = 0; k < a_cols; k++) {
            sum += a[row * a_cols + k] * b[k * b_cols + col];
            }
            c[row * b_cols + col] = sum;
        }
        }
        """

        program = cl.Program(ctx, kernel_code).build()
        program.matrix_dot(queue, (a_rows, b_cols), None, a_device, b_device, c_device,
                  np.int32(a_rows), np.int32(a_cols), np.int32(b_cols))
        cl.enqueue_copy(queue, c, c_device).wait()

        return c

def euler_cl(x_n: np.array, y_n: np.array, h: float) -> np.array:
    x_rows = np.size(x_n, axis=0)
    x_cols = np.size(x_n, axis=1)

    y_rows = np.size(y_n, axis=0)
    y_cols = np.size(y_n, axis=1)

    if x_rows != y_rows or x_cols != y_cols:
        raise TypeError(f"Matrices have different dimensions: \nX: {x_rows}:{x_cols}, Y: {y_rows}:{y_cols}")
    else:
        rows = x_rows
        cols = y_cols

        n = x_n.shape[0]

        x = np.zeros((rows, cols), dtype=np.float32)

        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)

        kernel_code = """
        __kernel void vector_add_scaled(__global const float *x_n,
                                        __global const float *y_n,
                                        __global float *x,
                                        const float h,
                                        const int n) {
        int i = get_global_id(0);
        if (i < n) {
            x[i] = x_n[i] + h * y_n[i];
        }
        }
        """

        mf = cl.mem_flags
        x_n_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf= x_n.astype(np.float32))
        y_n_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf= y_n.astype(np.float32))
        x_device = cl.Buffer(ctx, mf.WRITE_ONLY, x_n.nbytes)

        program = cl.Program(ctx, kernel_code).build()
        program.vector_add_scaled(queue, (n,), None, x_n_device, y_n_device, x_device, np.float32(h), np.int32(n))
        cl.enqueue_copy(queue, x, x_device).wait()

        return x


@timer
def sum_np(a_host, b_host):
    return a_host + b_host


# --- --- --- --- --- TESTING

# Define matrix dimensions
rows = 1
cols = 1

# Create host matrices
a_host = np.random.rand(rows, cols).astype(np.float32)
b_host = np.random.rand(rows, cols).astype(np.float32)

some_a = np.array([1.0])

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


print(np.dot(some_a, 0))
print(dot_cl(some_a, np.array([1])))

# res_dot_cl = dot_cl(a_host, b_host)
# print(f"Dot cl {res_dot_cl}")

# print(f"Dot np {np.dot(a_host, b_host)}")

# print("\nResult verification:", np.allclose(res, res_np))
