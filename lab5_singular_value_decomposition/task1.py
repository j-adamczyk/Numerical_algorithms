import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy.linalg import svd
from random import random


def get_sphere(n):
    s = [(2 * np.pi) * random() for i in range(n)]
    t = [np.pi * np.random.random() for i in range(n)]
    x = np.cos(s) * np.sin(t)
    y = np.sin(s) * np.sin(t)
    z = np.cos(t)
    return x, y, z


x, y, z = get_sphere(300)
S = np.row_stack([x, y, z])

A1 = np.random.rand(3, 3)
A2 = np.random.rand(3, 3)
A3 = np.random.rand(3, 3)

ellipsoid1 = A1 @ S
ellipsoid2 = A2 @ S
ellipsoid3 = A3 @ S

U1, sigma1, V1 = svd(A1)
U2, sigma2, V2 = svd(A2)
U3, sigma3, V3 = svd(A3)

x_start, y_start, z_start = [[0] * 3] * 3
x_end = [0] * 3
y_end = [0] * 3
z_end = [0] * 3

for i, s1 in enumerate(np.diag(sigma1)):
    a = np.dot(U1, s1)
    x_end[i] = a[0]
    y_end[i] = a[1]
    z_end[i] = a[2]
quiver1 = [x_start, y_start, z_start, x_end, y_end, z_end]

# plot 1

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid1[0], ellipsoid1[1], ellipsoid1[2], color='red')
ax.quiver(x_start, y_start, z_start, x_end, y_end, z_end, color='black')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

for i, s2 in enumerate(np.diag(sigma2)):
    a = np.dot(U2, s2)
    x_end[i] = a[0]
    y_end[i] = a[1]
    z_end[i] = a[2]
quiver2 = [x_start, y_start, z_start, x_end, y_end, z_end]

# plot 2

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid2[0], ellipsoid2[1], ellipsoid2[2], color='orange')
ax.quiver(x_start, y_start, z_start, x_end, y_end, z_end, color='black')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

# plot 3

for i, s3 in enumerate(np.diag(sigma3)):
    a = np.dot(U3, s3)
    x_end[i] = a[0]
    y_end[i] = a[1]
    z_end[i] = a[2]
quiver3 = [x_start, y_start, z_start, x_end, y_end, z_end]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid3[0], ellipsoid3[1], ellipsoid3[2], color='yellow')
ax.quiver(x_start, y_start, z_start, x_end, y_end, z_end, color='black')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

# ellipsoid with max/min singular value > 100

A = np.random.rand(3, 3)
U, sigma, V = svd(A)

while sigma[0] / sigma[2] < 100:
    A = np.random.rand(3, 3)
    U, sigma, V = svd(A)

print(A)

ellipsoid = A @ S

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_title("Max/min singular value > 100")
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid[0], ellipsoid[1], ellipsoid[2], color='green')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

# plot S V^T, S sigma V^T, S U sigma V^T

U, sigma, V = svd(A1)
ellipsoid = S.transpose() @ V
ellipsoid = ellipsoid.transpose()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_title("S * V^T")
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid[0], ellipsoid[1], ellipsoid[2], color='red')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

ellipsoid = S.transpose() * sigma @ V
ellipsoid = ellipsoid.transpose()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_title("S * sigma * V^T")
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid[0], ellipsoid[1], ellipsoid[2], color='orange')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()

ellipsoid = S.transpose() @ U * sigma @ V
ellipsoid = ellipsoid.transpose()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_title("S * U * sigma * V^T")
ax.set_aspect('equal')
ax.scatter(x, y, z)
ax.scatter(ellipsoid[0], ellipsoid[1], ellipsoid[2], color='yellow')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)
plt.show()
