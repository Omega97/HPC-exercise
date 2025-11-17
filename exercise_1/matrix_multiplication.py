import numpy as np
import time
import sys

def measure_matrix_multiplication(n):
    A = np.random.rand(n, n).astype(np.float64)
    B = np.random.rand(n, n).astype(np.float64)
    import gc
    gc.collect()
    start = time.perf_counter()
    C = np.dot(A, B)
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 matrix_multiplication.py <n>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except:
        print("Errore: inserire un numero intero")
        sys.exit(1)

    t = measure_matrix_multiplication(n)
    gflops = (2.0 * n**3) / (t * 1e9) if t > 0 else 0
    print(f"Matrix size: {n}x{n}")
    print(f"Time:        {t:.4f} s")
    print(f"Performance: {gflops:.2f} GFLOPS")
