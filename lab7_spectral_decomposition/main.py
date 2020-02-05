import matplotlib.pyplot as plt
import numpy as np
from scipy import linalg
import time


def power_iteration(A, max_iters, epsilon):
    eigvec = np.random.rand(A.shape[0])

    for _ in range(max_iters):
        new_eigvec = np.dot(A, eigvec)
        new_eigvec_norm = np.linalg.norm(new_eigvec)
        new_eigvec /= new_eigvec_norm
        if np.linalg.norm(new_eigvec - eigvec) < epsilon:
            break
        else:
            eigvec = np.transpose(new_eigvec) * A * new_eigvec

    eigval = np.max(np.abs(eigvec))
    eigvec /= np.linalg.norm(eigvec, axis=0)
    return eigvec, eigval


def calculate_and_plot_power_iterations():
    xs = []
    ys = []
    for k in range(100, 2000, 100):
        A = np.random.rand(k, k)
        A = A * np.transpose(A)
        start_time = time.time_ns()
        eigvec, eigval = power_iteration(A, 10000, 1e-9)
        end_time = time.time_ns()
        calc_time = end_time - start_time
        #m = A.shape[0]
        #lib_eigval, lib_eigvec = eigh(A, eigvals=(m-1, m-1))
        #lib_eigvec = np.transpose(lib_eigvec)[0]
        xs.append(k)
        ys.append(calc_time)
    plt.plot(xs, ys)
    plt.show()


def inverse_power_iteration(A, u, max_iters, epsilon):
    v0 = np.identity(A.shape[0])[0]
    AuI = A - u*np.identity(A.shape[0])
    lupiv = linalg.lu_factor(AuI)
    for i in range(max_iters):
        v = v0
        w = linalg.lu_solve(lupiv, v)
        v = w / np.linalg.norm(w)
        if np.linalg.norm(v-v0) < epsilon or np.linalg.norm(v+v0) < epsilon:
            print("Iterations: " + str(i))
            return u, v
        u = v.T @ A @ v
        v0 = v


A = np.random.rand(100, 100)
A = A * np.transpose(A)
eigvec, eigval = inverse_power_iteration(A, 0, 1000, 1e-5)
eigvec2, eigval2 = inverse_power_iteration(A, 10, 1000, 1e-5)
eigvec3, eigval3 = inverse_power_iteration(A, 50, 1000, 1e-5)
