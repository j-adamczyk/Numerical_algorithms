import random as rand


def get_uniform_distribution_points(low, high, n):
    result = set()
    city_number = 0
    while len(result) < n:
        a = rand.uniform(low, high)
        b = rand.uniform(low, high)
        if not (a, b) in result:
            result.add((a, b, city_number))
            city_number += 1
    return list(result)


def get_normal_distribution_points(low, high, n):
    mean = (high + low) / 2
    result = set()
    city_number = 0
    while len(result) < n:
        a = rand.uniform(mean, mean/4)
        b = rand.uniform(mean, mean/4)
        if not (a, b) in result:
            result.add((a, b, city_number))
            city_number += 1
    return list(result)


def get_9_groups_of_points(low, high, n):
    result = set()
    first_group = (low, high * 0.2)
    second_group = (high * 0.4, high * 0.6)
    third_group = (high * 0.8, high)
    list_of_groups = [first_group, second_group, third_group]
    city_number = 0
    while len(result) < n:
        group = rand.choice(list_of_groups)
        a = rand.uniform(group[0], group[1])
        group = rand.choice(list_of_groups)
        b = rand.uniform(group[0], group[1])
        if not (a, b) in result:
            result.add((a, b, city_number))
            city_number += 1
    return list(result)
