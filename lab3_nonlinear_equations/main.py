import math
import decimal as dec
import numpy as np


class MethodResult:
    number_of_steps = 0
    root = 0


def f1(x):
    return dec.Decimal(math.cos(x) * math.cosh(x))


def f1der(x):
    return dec.Decimal(math.cos(x) * math.sinh(x) - math.sin(x) * math.cosh(x))


def f2(x):
    if math.isclose(x, 0.0, abs_tol=1e-9):
        return dec.Decimal(10000000)
    else:
        return dec.Decimal(1/x) - dec.Decimal(math.tan(x))


def f2der(x):
    return dec.Decimal(-1/x**2) - dec.Decimal(1 / math.cos(x)**2)


def f3(x):
    return dec.Decimal(math.pow(2, -x) + math.pow(math.e, x) + 2*math.cos(x)) - 6


def f3der(x):
    return dec.Decimal(math.pow(math.e, x) - math.pow(2, -x) * math.log(2, math.e) - 2 * math.sin(x))


def f4(x):
    return dec.Decimal(x**3 - 3 * x + 1)


def f4der(x):
    return dec.Decimal(3 * x**2 - 3)


def bisection(function, float_precision, result_precision, a, b):
    f_a = function(a)
    f_b = function(b)

    if np.sign(f_a) == np.sign(f_b):
        print("Function has same signs at " + a + " and " + b + "!")
        return None

    dec.getcontext().prec = float_precision
    error = dec.Decimal(b) - dec.Decimal(a)
    number_of_steps = 0

    while not math.isclose(error, 0, abs_tol=result_precision):
        error = dec.Decimal(b) - dec.Decimal(a)
        error = error / 2
        c = dec.Decimal(a) + error
        f_c = function(c)

        number_of_steps += 1

        if math.isclose(error, 0, abs_tol=result_precision):
            result = MethodResult()
            result.number_of_steps = number_of_steps
            result.root = c
            return result

        if np.sign(f_a) != np.sign(f_c):
            b = c
        else:
            a = c
            f_a = f_c


def Newton_method(function, function_derivative, float_precision, max_iterations, result_precision, x):
    dec.getcontext().prec = float_precision
    x = dec.Decimal(x)

    number_of_steps = 0

    while (not math.isclose(function(x), 0, abs_tol=result_precision)) and (number_of_steps < max_iterations):
        x = x - function(x) / function_derivative(x)
        number_of_steps += 1

    if number_of_steps == max_iterations:
        print("Maximum number of iterations achieved!")
        result = MethodResult()
        result.number_of_steps = number_of_steps
        result.root = x
        return result

    result = MethodResult()
    result.number_of_steps = number_of_steps
    result.root = x
    return result


def secant_method(function, float_precision, max_iterations, result_precision, a, b):
    f_a = function(a)
    f_b = function(b)

    if np.sign(f_a) == np.sign(f_b):
        print("Function has same signs at " + a + " and " + b + "!")
        return None

    dec.getcontext().prec = float_precision

    a_n = dec.Decimal(a)
    b_n = dec.Decimal(b)

    root = a_n - f_a * (b_n - a_n) / (f_b - f_a)
    f_root = function(root)

    number_of_steps = 1

    while (not math.isclose(f_root, 0, abs_tol=result_precision)) and (number_of_steps < max_iterations):
        f_a = function(a_n)
        f_b = function(b_n)

        root = a_n - f_a * (b_n - a_n) / (f_b - f_a)
        f_root = function(root)

        number_of_steps += 1

        if np.sign(f_a) != np.sign(f_root):
            b_n = root
        elif np.sign(f_b) != np.sign(f_root):
            a_n = root
        elif math.isclose(f_root, 0, abs_tol=result_precision):
            result = MethodResult()
            result.number_of_steps = number_of_steps
            result.root = root
            return result

    if number_of_steps == max_iterations:
        print("Maximum number of iterations achieved!")
        result = MethodResult()
        result.number_of_steps = number_of_steps
        result.root = root
        return result

    result = MethodResult()
    result.number_of_steps = number_of_steps
    result.root = root
    return result


for i in [math.pow(10, -7), math.pow(10, -15), math.pow(10, -33)]:
    bisection_result = bisection(f1, 16, 1e-8, 1.5*math.pi, 2*math.pi)
    Newton_method_result = Newton_method(f1, f1der, 16, 50, 1e-8, (1.5*math.pi+2*math.pi)/2)
    secant_result = secant_method(f1, 16, 50, 1e-8, 1.5*math.pi, 2*math.pi)

    print("Function f1, precision : " + str(i))
    print(str(bisection_result.root) + " " + str(bisection_result.number_of_steps))
    print(str(Newton_method_result.root) + " " + str(Newton_method_result.number_of_steps))
    print(str(secant_result.root) + " " + str(secant_result.number_of_steps))

    print("")

    bisection_result = bisection(f2, 16, 1e-8, 0, math.pi/2)
    Newton_method_result = Newton_method(f2, f2der, 16, 50, 1e-8, math.pi/4)
    secant_result = secant_method(f2, 16, 50, 1e-8, 0, math.pi/2)

    print("Function f2, precision : " + str(i))
    print(str(bisection_result.root) + " " + str(bisection_result.number_of_steps))
    print(str(Newton_method_result.root) + " " + str(Newton_method_result.number_of_steps))
    print(str(secant_result.root) + " " + str(secant_result.number_of_steps))

    print("")

    bisection_result = bisection(f3, 16, 1e-8, 1, 3)
    Newton_method_result = Newton_method(f3, f3der, 16, 50, 1e-8, 2)
    secant_result = secant_method(f3, 16, 50, 1e-8, 1, 3)

    print("Function f3, precision : " + str(i))
    print(str(bisection_result.root) + " " + str(bisection_result.number_of_steps))
    print(str(Newton_method_result.root) + " " + str(Newton_method_result.number_of_steps))
    print(str(secant_result.root) + " " + str(secant_result.number_of_steps))

    print("\n")
