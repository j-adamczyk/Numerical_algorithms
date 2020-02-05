import copy
import generators
import math
import neighbor_states as ns
import numpy as np
import plotter
import random as rand


def get_matrix(cities):
    n = len(cities)
    result = np.zeros((n, n))

    for x in range(n):
        for y in range(n):
            x1 = cities[x][0]
            y1 = cities[x][1]
            x2 = cities[y][0]
            y2 = cities[y][1]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            result[x][y] = distance
            result[y][x] = distance
    return result


def path_distance(path, distances):
    distance = 0
    for i in range(len(path) - 1):
        distance += distances[path[i][2]][path[i + 1][2]]
    return distance


def travelling_salesman_problem(n, iterations, temperature, decay_rate, swap_type, low, high, distribution):
    if distribution == "uniform":
        path = generators.get_uniform_distribution_points(low, high, n)
    elif distribution == "normal" or distribution == "gaussian":
        path = generators.get_normal_distribution_points(low, high, n)
    elif distribution == "groups" or distribution == "9 groups":
        path = generators.get_9_groups_of_points(low, high, n)
    else:
        raise ValueError("Error: distribution argument was not uniform, normal or groups!")

    first_path = copy.copy(path)

    if swap_type != "consecutive" and swap_type != "arbitrary":
        raise ValueError("Error: swap type argument was not consecutive or arbitrary!")

    distances = get_matrix(path)

    rand.shuffle(path)

    best_path = path
    min_distance = path_distance(best_path, distances)

    iters = []
    dists = []
    temperatures = []

    for i in range(iterations):
        iters.append(i)

        new_path = copy.copy(path)
        if swap_type == "consecutive":
            new_path = ns.consecutive_swap(new_path)
        else:
            new_path = ns.consecutive_swap(new_path)

        old_path_distance = path_distance(path, distances)
        new_path_distance = path_distance(new_path, distances)

        dists.append(new_path_distance)

        if new_path_distance < old_path_distance:
            path = new_path
            if new_path_distance < min_distance:
                min_distance = new_path_distance
        elif math.exp(-(new_path_distance - old_path_distance)/temperature) > rand.uniform(0, 1):
            path = new_path

        temperatures.append(temperature)
        temperature *= decay_rate

    distances_plot_data = (copy.copy(iters), dists)
    temperatures_plot_data = (iters, temperatures)
    return first_path, best_path, distances_plot_data, temperatures_plot_data


n = 200
iterations = 500000
temperature = 1000
decay_rate = 0.99995
swap_type = "consecutive"
low = 0
high = 1
distribution = "uniform"

first_path, best_path, distances_plot_data, temperatures_plot_data = travelling_salesman_problem(n, iterations, temperature, decay_rate, swap_type, low, high, distribution)

plotter.plot_data(first_path, best_path, distances_plot_data, temperatures_plot_data)
