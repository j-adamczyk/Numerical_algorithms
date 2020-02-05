import numpy as np
from scipy import integrate


f1 = lambda x, y: 1 / (np.sqrt(x+y) * (1+x+y))
f2 = lambda x, y: x**2 + y ** 2


def trapezoidal_rule_2D(f, xmin, xmax, xnum, ymin, ymax, ynum):
    integral = 0
    hx = (xmax - xmin) / xnum

    for i in range(0, xnum + 1):
        x = xmin + i * hx
        hy = (ymax(x) - ymin(x)) / ynum

        part_int = 0
        for j in range(0, ynum + 1):
            y = ymax(x) + j * hy

            if j in {0, ynum}:
                part_int += 0.5 * f(x, y)
            else:
                part_int += f(x, y)

        part_int *= hy
        if i in {0, xnum}:
            integral += 0.5 * part_int
        else:
            integral += part_int

    integral *= hx
    return integral


f = f1
xmin = 0
xmax = 1
ymin = lambda x: 0
ymax = lambda x: 1 - x
xnum = 1000
ynum = 1000
custom_int = trapezoidal_rule_2D(f, xmin, xmax, xnum, ymin, ymax, ynum) * 10
lib_int = integrate.dblquad(f, xmin, xmax, ymin, ynum)[0]

print("Custom: " + str(custom_int))
print("Library: " + str(lib_int))

f = f2
xmin = -3
xmax = 3
ymin = lambda x: -5
ymax = lambda x: 5
xnum = 1000
ynum = 1000
custom_int = trapezoidal_rule_2D(f, xmin, xmax, xnum, ymin, ymax, ynum) / 10
lib_int = integrate.dblquad(f, xmin, xmax, ymin, ynum)[0]

print("Custom: " + str(custom_int))
print("Library: " + str(lib_int))
