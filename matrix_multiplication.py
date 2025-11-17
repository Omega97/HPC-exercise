import numpy as np
import matplotlib.pyplot as plt
import time


def measure_matrix_multiplication(n):
    """
    Measures the time taken by NumPy to multiply two n x n matrices.

    Parameters:
        n (int): Dimension of square matrices.

    Returns:
        float: Elapsed time in seconds.
    """
    # Generate two random n x n matrices
    A = np.random.rand(n, n).astype(np.float64)
    B = np.random.rand(n, n).astype(np.float64)

    # Force garbage collection (optional, for more consistent benchmarks)
    import gc
    gc.collect()

    # Time the matrix multiplication
    start_time = time.perf_counter()
    C = np.dot(A, B)  # or A @ B
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    return elapsed


def plot_time(n1, n2, step, do_log=False):
    x_ = np.array(range(n1, n2+step, step))
    y_ = []
    for n in x_:
        t = measure_matrix_multiplication(n)
        y_.append(t)
    y_ = np.array(y_)

    if do_log:
        plt.title('log time vs log size')
        plt.xlabel('log n')
        plt.ylabel('log t')
        plt.scatter(np.log(x_), np.log(y_))
        plt.plot(np.log(x_), np.log(y_))
    else:
        plt.title('Time vs size')
        plt.xlabel('n')
        plt.ylabel('t [s]')
        plt.scatter(x_, y_)
        plt.plot(x_, y_)

    plt.show()


def test_product(matrix_size=2_000):
    elapsed_time = measure_matrix_multiplication(matrix_size)
    print(f"Time taken: {elapsed_time:.3f} s (size={matrix_size})")


def test_plot(n1=50, n2=2000, step=50, do_log=False):
    plot_time(n1, n2, step, do_log=do_log)


if __name__ == "__main__":
    test_product(matrix_size=1_000)
    test_product(matrix_size=2_000)
    test_product(matrix_size=4_000)
    # test_plot()
