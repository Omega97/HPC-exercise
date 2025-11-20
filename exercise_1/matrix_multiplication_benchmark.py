"""This is the matrix benchmark for the laptop."""
import numpy as np
import time
from random import shuffle
import gc


def measure_matrix_multiplication(n):
    A = np.random.rand(n, n).astype(np.float64)
    B = np.random.rand(n, n).astype(np.float64)

    gc.collect()

    start_time = time.perf_counter()
    C = np.dot(A, B)
    end_time = time.perf_counter()

    return end_time - start_time


def fit_power_law(x, y):
    """
    Fit y = k * x^m using log-log linear regression.

    Parameters:
        x (array-like): Input sizes (must be > 0)
        y (array-like): Measured times (must be > 0)

    Returns:
        k (float): Estimated prefactor
        m (float): Estimated exponent
    """
    x = np.asarray(x)
    y = np.asarray(y)

    if np.any(x <= 0) or np.any(y <= 0):
        raise ValueError("x and y must be positive for log transformation.")

    log_x = np.log(x)
    log_y = np.log(y)

    # Build design matrix: [log_x, 1] for slope and intercept
    X = np.vstack([log_x, np.ones_like(log_x)]).T

    # Solve least squares: log_y = m * log_x + log_k
    m, log_k = np.linalg.lstsq(X, log_y, rcond=None)[0]

    k = np.exp(log_k)
    return k, m


def test_performance(start=1000, stop=5000, step=200):
    sizes = list(range(start, stop, step))
    shuffle(sizes)
    times = []

    print('epoch\tsize\tt [s]')
    for i, matrix_size in enumerate(sizes):
        elapsed_time = measure_matrix_multiplication(matrix_size)
        times.append(elapsed_time)
        print(f"{i+1:2} /{len(sizes):2} {matrix_size:4}\t{elapsed_time:.4f}")

    kilo_sizes = np.array(sizes) / 1000
    times = np.array(times)

    # Fit power law
    tau, m = fit_power_law(kilo_sizes, times)
    omega = 1/tau
    print(f"\nFitted model: t = tau * (n/1000)^p")
    print()
    print(f"  tau = {tau:.4f}  <- characteristic time [s]")
    print(f"    p = {m:.3f}  <- power [1]")
    print()
    print(f"omega = {omega:.1f} <- frequency [s^-1] (higher is better)")

    return np.array(kilo_sizes), np.array(times), tau, m


if __name__ == "__main__":
    test_performance()
