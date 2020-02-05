import copy
import math
import numpy as np
import random as rand


def fill_empty_places(matrix):
    block_xs = [0, 3, 6]
    block_ys = [0, 3, 6]

    for block_x in block_xs:
        for block_y in block_ys:
            xs = [block_x, block_x+1, block_x+2]
            ys = [block_y, block_y+1, block_y+2]

            numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            for x in xs:
                for y in ys:
                    if matrix[x, y] in numbers:
                        numbers.remove(matrix[x, y])

            for x in xs:
                for y in ys:
                    if matrix[x, y] == 0:
                        matrix[x, y] = numbers.pop()

    return matrix


# file should be in format: empty spaces or zeroes as spaces, filled as integers from 1 to 9
# 9 lines with 9 characters in each
def load_sudoku(file_name):
    matrix = np.zeros((9, 9))
    starting_positions = set([])
    with open(file_name, "r") as file:
        row = 0
        for line in file:
            column = 0
            for char in line:
                if char == "\n":
                    continue
                if char != " ":
                    matrix[row][column] = int(char)
                    if char != "0":
                        starting_positions.add((row, column))
                else:
                    matrix[row][column] = 0
                column += 1
            row += 1

    print(matrix)
    matrix = fill_empty_places(matrix)
    return matrix, starting_positions


# cost should be as small as possible
# cost = -1 for each unique entry
# best cost = -162
def cost(matrix):
    result = 0
    for i in range(0, 9):
        numbers = set([])
        for j in range(0, 9):
            numbers.add(matrix[i][j])
        result -= len(numbers)

    for i in range(0, 9):
        numbers = set([])
        for j in range(0, 9):
            numbers.add(matrix[j][i])
        result -= len(numbers)

    return result


# randomly choose one of 9 blocks, then swap random elements there
def neighbor_state(matrix, starting_positions):
    block_x = rand.choice([0, 3, 6])
    block_y = rand.choice([0, 3, 6])

    x1 = rand.choice([block_x, block_x+1, block_x+2])
    y1 = rand.choice([block_y, block_y+1, block_y+2])
    while (x1, y1) in starting_positions:
        x1 = rand.choice([block_x, block_x + 1, block_x + 2])
        y1 = rand.choice([block_y, block_y + 1, block_y + 2])

    x2 = rand.choice([block_x, block_x + 1, block_x + 2])
    y2 = rand.choice([block_y, block_y + 1, block_y + 2])
    while ((x2, y2) in starting_positions) or (x2 == x1 and y2 == y1):
        x2 = rand.choice([block_x, block_x + 1, block_x + 2])
        y2 = rand.choice([block_y, block_y + 1, block_y + 2])

    neighbor_matrix = copy.copy(matrix)
    neighbor_matrix[x1, y1], neighbor_matrix[x2, y2] = neighbor_matrix[x2, y2], neighbor_matrix[x1, y1]

    return neighbor_matrix


def simulated_annealing(sudoku, T_0, decay_rate, iterations):
    curr_matrix = sudoku[0]
    starting_positions = sudoku[1]

    best_matrix = curr_matrix
    best_cost = cost(best_matrix)

    T = T_0
    iters_without_change = 0
    for iter in range(iterations):
        new_matrix = neighbor_state(curr_matrix, starting_positions)
        new_cost = cost(new_matrix)

        curr_cost = cost(curr_matrix)

        if new_cost < curr_cost:
            curr_matrix = new_matrix
            curr_cost = new_cost
            iters_without_change = 0
            if curr_cost < best_cost:
                best_matrix = curr_matrix
                best_cost = curr_cost
                #print(best_cost)
                if best_cost == -162:
                    return best_matrix, best_cost
        elif math.exp(-(new_cost - curr_cost)/T) > rand.uniform(0, 1):
            curr_matrix = new_matrix
            iters_without_change = 0
        else:
            iters_without_change += 1

        T *= decay_rate

        if iters_without_change == 100:
            T += 0.3 * T_0
            iters_without_change = 0

    return best_matrix, best_cost


def solve_sudoku(filename):
    sudoku = load_sudoku(filename)

    T_0 = 0.5
    decay_rate = 0.9999
    iterations = 20000

    solved_sudoku, cost = simulated_annealing(sudoku, T_0, decay_rate, iterations)
    while cost != -162:
        print(cost)
        solved_sudoku, wrong_digits = simulated_annealing(sudoku, T_0, decay_rate, iterations)

    return solved_sudoku


print("\n")
solved_sudoku = solve_sudoku("sudoku3.txt")
print("\n\n")
print(solved_sudoku)
