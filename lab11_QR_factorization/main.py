import matplotlib.pyplot as plt
import numpy as np
from numpy import diag
from numpy.linalg import norm, qr, svd
import time


def graham_schmidt(A):
    Q = np.zeros((A.shape[0], A.shape[0]))
    R = np.zeros((A.shape[0], A.shape[1]))

    # first vector
    a_len = norm(A[:, 0])
    for i in range(A.shape[0]):
        Q[i, 0] = A[i, 0] / a_len

    # rest of vectors
    for k in range(1, A.shape[1]):
        for i in range(A.shape[0]):
            Q[i, k] = A[i, k]

        for i in range(k):
            dot_prod = np.dot(Q[:, i], A[:, k])
            for a in range(A.shape[0]):
                Q[a, k] -= dot_prod * Q[a, i]

        a_len = np.linalg.norm(Q[:, k])

        for i in range(A.shape[0]):
            Q[i, k] = Q[i, k] / a_len

    for a in range(A.shape[0]):
        for b in range(A.shape[1]):
            if a <= b:
                R[a, b] = np.dot(Q[:, a], A[:, b])

    return Q, R


# test
"""for n in [4, 8, 20, 50, 100, 300]:
    print("n = ", n)

    A = np.random.rand(n, n)

    custom_time = time.time()
    Q1, R1 = graham_schmidt(A)
    custom_time = time.time() - custom_time
    print("Custom time: ", custom_time)

    custom_time = time.time()
    Q2, R2 = qr(A, mode='complete')
    custom_time = time.time() - custom_time
    print("Library time: ", custom_time)

    if n == 4:
        print("A")
        print(A)
        print("Custom A")
        print(Q1@R1)
        print("Library A")
        print(Q2@R2)"""


# ||I-Q^T*Q|| (cond(A))
"""I = np.identity(8)
cond_to_val = dict()
while len(cond_to_val) < 50:
    A = np.random.rand(8, 8)
    U, S, Vt = svd(A)
    cond = S[0] / S[7]

    if cond not in cond_to_val:
        A = U.dot(diag(S)).dot(Vt)
        Q, R = graham_schmidt(A)
        val = norm(I - Q.transpose() @ Q)
        cond_to_val[cond] = val

to_print = list(cond_to_val.items())
to_print.sort()
xs = [pair[0] for pair in to_print]
ys = [pair[1] for pair in to_print]
plt.plot(xs, ys, 'o')
plt.show()"""


# linear equation system solver
points_xs = [x for x in range(-5, 6)]
points_ys = [2, 7, 9, 12, 13, 14, 14, 13, 10, 8, 4]

# prepare A matrix
A = np.zeros((11, 3))
a = 0
for i in range(-5, 6):
    A[a, 0] = 1
    A[a, 1] = i
    A[a, 2] = i*i
    a += 1

# prepare B matrix
B = np.matrix(points_ys)
B = B.transpose()

# do the actual solving
Q, R = np.linalg.qr(A, mode="complete")

print(Q.shape)
print(R.shape)

R1 = np.zeros((3, 3))
for i in range(0, 3):
    for j in range(0, 3):
        R1[i, j] = R[i, j]

#result = np.linalg.solve((Q@R).transpose() @ (Q@R), (Q@R).transpose() @ B.transpose())
#result = np.linalg.solve(R.transpose() @ Q.transpose() @ Q @ R, R.transpose() @ Q.transpose())
#result = np.linalg.solve(R.transpose() @ R, R.transpose() @ Q.transpose() @ B)
result = np.linalg.solve(R1, Q.transpose() @ B)

approx_xs = [x/10 for x in range(-50, 50)]
approx_ys = [result[0, 0]+x*result[1, 0]+x*x*result[2, 0] for x in approx_xs]

# plot results
plt.plot(points_xs, points_ys)
plt.plot(approx_xs, approx_ys)
plt.show()
