# only 3x3 types of energy are implemented


# perfect energy for this function (x - black, o - white):
# o x o
# x x x <- middle x is the point
# o x o
def black_cross(point, bitmap, energy_map):
    n = bitmap.shape[0]
    x = point[0]
    y = point[1]
    energy = 0

    # higher row
    if x-1 >= 0:
        if y-1 >= 0 and bitmap[x-1, y-1] == 255:
            energy += 1
        if bitmap[x-1, y] == 0:
            energy += 1
        if y+1 < n and bitmap[x-1, y+1] == 255:
            energy += 1

    # same row
    if y-1 >= 0 and bitmap[x, y-1] == 0:
        energy += 1
    if bitmap[x, y] == 0:
        energy += 1
    if y+1 < n and bitmap[x, y+1] == 0:
        energy += 1

    # lower row
    if x+1 < n:
        if y-1 >= 0 and bitmap[x+1, y-1] == 255:
            energy += 1
        if bitmap[x+1, y] == 0:
            energy += 1
        if y+1 < n and bitmap[x+1, y+1] == 255:
            energy += 1

    energy_map[x, y] = energy
    return energy_map


# perfect energy for this function (x - black, o - white):
# x o x
# o x o <- x here is the point
# x o x
def chessboard(point, bitmap, energy_map):
    n = bitmap.shape[0]
    x = point[0]
    y = point[1]
    energy = 0

    # higher row
    if x-1 >= 0:
        if y-1 >= 0 and bitmap[x-1, y-1] == 0:
            energy += 1
        if bitmap[x-1, y] == 255:
            energy += 1
        if y+1 < n and bitmap[x-1, y+1] == 0:
            energy += 1

    # same row
    if y-1 >= 0 and bitmap[x, y-1] == 255:
        energy += 1
    if bitmap[x, y] == 0:
        energy += 1
    if y+1 < n and bitmap[x, y+1] == 255:
        energy += 1

    # lower row
    if x+1 < n:
        if y-1 >= 0 and bitmap[x+1, y-1] == 0:
            energy += 1
        if bitmap[x+1, y] == 255:
            energy += 1
        if y+1 < n and bitmap[x+1, y+1] == 0:
            energy += 1

    energy_map[x, y] = energy
    return energy_map


# perfect energy for this function (x - black, o - white):
# o o o
# o o o <- o here is the point
# o o o
def white_squares(point, bitmap, energy_map):
    n = bitmap.shape[0]
    x = point[0]
    y = point[1]
    energy = 0

    # higher row
    if x-1 >= 0:
        if y-1 >= 0 and bitmap[x-1, y-1] == 255:
            energy += 1
        if bitmap[x-1, y] == 255:
            energy += 1
        if y+1 < n and bitmap[x-1, y+1] == 255:
            energy += 1

    # same row
    if y-1 >= 0 and bitmap[x, y-1] == 255:
        energy += 1
    if bitmap[x, y] == 255:
        energy += 1
    if y+1 < n and bitmap[x, y+1] == 255:
        energy += 1

    # lower row
    if x+1 < n:
        if y-1 >= 0 and bitmap[x+1, y-1] == 255:
            energy += 1
        if bitmap[x+1, y] == 255:
            energy += 1
        if y+1 < n and bitmap[x+1, y+1] == 255:
            energy += 1

    energy_map[x, y] = energy
    return energy_map
