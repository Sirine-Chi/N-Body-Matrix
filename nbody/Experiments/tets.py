import n_body_lib as nbl
import os
import time

import colorama
colorama.just_fix_windows_console()
colorama.init()
from colorama import Fore, Back, Style

os.environ["PYOPENCL_CTX"] = '0'

a_m = nbl.v([
    [2.0, 1.0],
    [4.0, 1.0]
])

b_m = nbl.v([
    [3.0, 4.0],
    [1.0, 10.0]
])

t1 = time.time()
print(Fore.BLUE)
print('\n NP: ', nbl.np_mult(a_m, b_m))
print('\n NP time: %.4f seconds' % (time.time() - t1) )
print(Style.RESET_ALL)

t2 = time.time()
print(Fore.GREEN)
print('\n CL: ', nbl.openCL_mult(a_m, b_m))
print('\n CL time: %.4f seconds' % (time.time() - t2) )
print(Style.RESET_ALL)