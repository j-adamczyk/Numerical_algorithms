import numpy as np
from scipy import integrate


def simpson_rule(xs, ys):
    n = len(xs)
    h = (xs[len(xs) - 1] - xs[0]) / n

    integral = ys[0]
    for i in range(0, int(n/2)):
        integral += 4 * ys[2 * i]

    for i in range(0, int(n/2 + 1)):
        integral += 2 * ys[2 * i - 1]

    integral += ys[len(ys) - 1]
    integral *= h / 3
    return integral


xs = list(np.arange(1, 100, 0.1))
ys = [np.exp(-x**2) * np.log(x)**2 for x in xs]

custom_int = simpson_rule(xs, ys)
lib_int = integrate.simps(ys, xs)

print("Custom 1: " + str(custom_int))
print("Library 1: " + str(lib_int))

ys = [1 / (x**3-2*x-5) for x in xs]

custom_int = simpson_rule(xs, ys)
lib_int = integrate.simps(ys, xs)

print("Custom 2: " + str(custom_int))
print("Library 2: " + str(lib_int))

ys = [x**5 * np.exp(-x) * np.sin(x) for x in xs]

custom_int = simpson_rule(xs, ys)
lib_int = integrate.simps(ys, xs)

print("Custom 3: " + str(custom_int))
print("Library 3: " + str(lib_int))
