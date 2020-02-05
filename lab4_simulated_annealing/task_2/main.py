import copy
import energy_functions as en_fun
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import random as rand
import time as time


def save_image(filename, matrix):
    compressed_image = Image.fromarray(matrix)
    compressed_image = compressed_image.convert("L")
    filename = filename + ".jpg"
    compressed_image.save(filename)


def get_random_bitmap(n, black_density):
    matrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            if rand.random() >= black_density:
                matrix[i, j] = 255
    return matrix


def calculate_full_energy_map(bitmap, energy_function):
    n = bitmap.shape[0]
    energy_map = np.zeros((n, n))
    for i in range(0, n):
        for j in range(0, n):
            point = (i, j)
            energy_map = energy_function(point, bitmap, energy_map)
    return energy_map


def calculate_new_energy_map(bitmap, energy_map, energy_function, point1, point2):
    points_to_recalculate = set([])
    n = bitmap.shape[0]

    x1 = point1[0]
    y1 = point1[1]

    if x1-1 >= 0:
        if y1-1 >= 0:
            points_to_recalculate.add((x1-1, y1-1))

        points_to_recalculate.add((x1-1, y1))

        if y1+1 < n:
            points_to_recalculate.add((x1-1, y1+1))

    if y1-1 >= 0:
        points_to_recalculate.add((x1, x1-1))

    points_to_recalculate.add((x1, y1))

    if y1+1 < n:
        points_to_recalculate.add((x1, y1+1))

    if x1+1 < n:
        if y1-1 >= 0:
            points_to_recalculate.add((x1+1, y1-1))

        points_to_recalculate.add((x1+1, y1))

        if y1+1 < n:
            points_to_recalculate.add((x1+1, y1+1))

    x2 = point2[0]
    y2 = point2[1]

    if x2 - 1 >= 0:
        if y2 - 1 >= 0:
            points_to_recalculate.add((x2 - 1, y2 - 1))

        points_to_recalculate.add((x2 - 1, y2))

        if y2 + 1 < n:
            points_to_recalculate.add((x2 - 1, y2 + 1))

    if y2 - 1 >= 0:
        points_to_recalculate.add((x2, x2 - 1))

    points_to_recalculate.add((x2, y2))

    if y2 + 1 < n:
        points_to_recalculate.add((x2, y2 + 1))

    if x2 + 1 < n:
        if y2 - 1 >= 0:
            points_to_recalculate.add((x2 + 1, y2 - 1))

        points_to_recalculate.add((x2 + 1, y2))

        if y2 + 1 < n:
            points_to_recalculate.add((x2 + 1, y2 + 1))

    new_energy_map = copy.copy(energy_map)
    for point in points_to_recalculate:
        new_energy_map = energy_function(point, bitmap, new_energy_map)
    return new_energy_map


def get_map_quality(energy_map):
    quality = 0
    for i in range(0, energy_map.shape[0]):
        for j in range(0, energy_map.shape[0]):
            quality += energy_map[i, j]
    return quality


def generate_neighbor_state(bitmap):
    x1 = rand.randint(0, bitmap.shape[0]-1)
    y1 = rand.randint(0, bitmap.shape[0]-1)

    x2_range = [x1-1, x1, x1+1]
    if x1-1 < 0:
        x2_range.remove(x1-1)
    if x1+1 >= bitmap.shape[0]:
        x2_range.remove(x1+1)

    y2_range = [y1-1, y1, y1+1]
    if y1-1 < 0:
        y2_range.remove(y1-1)
    if y1+1 >= bitmap.shape[0]:
        y2_range.remove(y1+1)

    x2 = rand.choice(x2_range)
    y2 = rand.choice(y2_range)
    while x2 == x1 and y2 == y1:
        x2 = rand.choice(x2_range)
        y2 = rand.choice(y2_range)

    bitmap[x1, y1], bitmap[x2, y2] = bitmap[x2, y2], bitmap[x1, y1]
    return bitmap, (x1, y1), (x2, y2)


def simulated_annealing(T_0, iterations, bitmap, energy_function, reheats):
    energy_map = calculate_full_energy_map(bitmap, energy_function)

    best_quality = get_map_quality(energy_map)
    best_bitmap = copy.copy(bitmap)

    curr_bitmap = bitmap
    curr_energy_map = energy_map
    curr_quality = best_quality

    iters = []
    qualities = []

    temperature = T_0
    reheats_counter = 0
    for i in range(iterations):
        new_bitmap = copy.copy(curr_bitmap)
        new_bitmap, point1, point2 = generate_neighbor_state(new_bitmap)
        new_energy_map = copy.copy(curr_energy_map)
        new_energy_map = calculate_new_energy_map(new_bitmap, new_energy_map, energy_function, point1, point2)

        new_quality = get_map_quality(new_energy_map)

        iters.append(i)
        qualities.append(new_quality)

        if new_quality > curr_quality:
            curr_bitmap = new_bitmap
            curr_energy_map = new_energy_map
            curr_quality = new_quality
            if new_quality > best_quality:
                best_bitmap = new_bitmap
        elif math.exp((new_quality - curr_quality)/temperature) > rand.random():
            curr_bitmap = new_bitmap
            curr_energy_map = new_energy_map
            curr_quality = new_quality

        temperature *= 0.999
        if reheats_counter < reheats and i == iterations // reheats:
            temperature += 0.1 * T_0

    return best_bitmap, iters, qualities


# T_0 should be roughly the same order of magnitude as n^2
T_0 = 1
iterations = 50000

# testing one size and generating images
"""
i = 2
for function in [en_fun.white_squares]:
    function_name = ""
    if i == 0:
        function_name = "black_cross"
    elif i == 1:
        function_name = "chessboard"
    elif i == 2:
        function_name = "white_squares"
    for reheats in [0, 10, 25, 50]:
        for black_density in [0.1, 0.3, 0.5, 0.7]:
            print("before_" + function_name + "_" + str(reheats) + "_" + str(black_density))

            test_bitmap = get_random_bitmap(100, black_density)
            name = "before_" + function_name + "_" + str(reheats) + "_" + str(black_density)
            save_image(name, test_bitmap)

            test_bitmap, xs, ys = simulated_annealing(T_0, iterations, test_bitmap, function, reheats)

            plt.plot(xs, ys)
            plt.title("Quality")
            name = "quality_" + function_name + "_" + str(reheats) + "_" + str(black_density) + ".jpg"
            plt.savefig(name)

            name = "after_" + function_name + "_" + str(reheats) + "_" + str(black_density)
            save_image(name, test_bitmap)
    i += 1
"""

iterations = 25000

# testing efficiency for different sizes
for size in [100, 256, 512, 1024]:
    test_bitmap = get_random_bitmap(size, 0.5)
    name = "before_" + str(size)
    save_image(name, test_bitmap)

    print("Size: " + str(size))

    start_time = time.time()
    test_bitmap, xs, ys = simulated_annealing(T_0, iterations, test_bitmap, en_fun.white_squares, 50)
    end_time = time.time()

    SA_time = end_time - start_time

    print("Time: " + str(SA_time) + "s" + "\n")

    name = "after_" + str(size)
    save_image(name, test_bitmap)
