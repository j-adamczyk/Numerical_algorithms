import numpy as np


def trapezoidal_rule(xs, ys):
    h = (xs[len(xs)-1] - xs[0]) / len(xs)

    integral = ys[0] / 2
    for i in range(0, len(xs)-1):
        integral += h/2 * (ys[i] + ys[i+1])
    integral += ys[len(ys) - 1] / 2

    integral /= 1000  # change m to km
    return integral


xs = list(np.arange(0, 100, 0.1))
ys = [10 * x for x in xs]
ys = [5/18 * y for y in ys]

custom_int = trapezoid_rule(xs, ys)
lib_int = np.trapz(ys, xs) / 1000

print("Custom: " + str(custom_int))
print("Library: " + str(lib_int))
