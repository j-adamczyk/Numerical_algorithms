import random as rand


def consecutive_swap(cities):
    high = len(cities) - 2
    i = rand.randint(0, high)
    cities[i], cities[i+1] = cities[i+1], cities[i]
    return cities


def arbitrary_swap(cities):
    high = len(cities) - 1
    i = rand.randint(0, high)
    j = rand.randint(0, high)
    while i == j:
        i = rand.randint(0, high)
        j = rand.randint(0, high)
    cities[i], cities[j] = cities[j], cities[i]
    return cities
