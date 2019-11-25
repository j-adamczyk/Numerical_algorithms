import networkx as nx
import os
import random
from random import randint

# all graphs return tuple (a,b) of nodes where battery may be put


def generate_random_connected_graph(node_number, file_name, edge_probability):
    G = nx.erdos_renyi_graph(node_number, edge_probability)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(node_number, edge_probability)

    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, "w+")

    for edge in G.edges:
        a = edge[0]
        b = edge[1]
        R = 1
        file.write(str(a) + " " + str(b) + " " + str(R) + "\n")
    file.seek(0, 2)
    file.truncate()
    file.close()

    a = random.choice(list(G.nodes))
    b = random.choice(list(G.nodes))
    while G.has_edge(a, b):
        a = random.choice(list(G.nodes))
        b = random.choice(list(G.nodes))
    return a, b


def generate_random_cubic_graph(node_number, file_name):
    G = nx.random_regular_graph(3, node_number)

    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, "w+")

    for edge in G.edges:
        a = edge[0]
        b = edge[1]
        R = 1
        file.write(str(a) + " " + str(b) + " " + str(R) + "\n")
    file.seek(0, 2)
    file.truncate()
    file.close()

    a = random.choice(list(G.nodes))
    b = random.choice(list(G.nodes))
    while G.has_edge(a, b):
        a = random.choice(list(G.nodes))
        b = random.choice(list(G.nodes))
    return a, b


# graph is generated in the way that battery is in only one part
def generate_random_graph_with_bridge(node_number, file_name, edge_probability):
    node_number = node_number // 2
    G1 = nx.erdos_renyi_graph(node_number, edge_probability)
    while not nx.is_connected(G1):
        G1 = nx.erdos_renyi_graph(node_number, edge_probability)

    G2 = nx.erdos_renyi_graph(node_number, edge_probability)
    while not nx.is_connected(G2):
        G2 = nx.erdos_renyi_graph(node_number, edge_probability)

    n = node_number

    bridge_left = random.choice(list(G1.nodes))
    bridge_right = random.choice(list(G2.nodes))
    bridge_right += n

    R = 1

    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, "w+")

    for edge in G1.edges:
        a = edge[0]
        b = edge[1]
        file.write(str(a) + " " + str(b) + " " + str(R) + "\n")

    for edge in G2.edges:
        a = edge[0] + n
        b = edge[1] + n
        file.write(str(a) + " " + str(b) + " " + str(R) + "\n")

    file.write(str(bridge_left) + " " + str(bridge_right) + " " + str(R))
    file.close()

    a = random.choice(list(G1.nodes))
    b = random.choice(list(G2.nodes)) + n
    while (a == bridge_left and b == bridge_right) or (b == bridge_left and a == bridge_right):
        a = random.choice(list(G1.nodes))
        b = random.choice(list(G2.nodes)) + n

    return a, b


# final node number = node_number ** 2
def generate_random_grid_graph(node_number, file_name):
    G = nx.grid_2d_graph(node_number, node_number)

    if os.path.exists(file_name):
        os.remove(file_name)
    file = open(file_name, "w+")

    for edge in G.edges:
        a = node_number * edge[0][0] + edge[0][1]
        b = node_number * edge[1][0] + edge[1][1]
        R = 1
        file.write(str(a) + " " + str(b) + " " + str(R) + "\n")
    file.seek(0, 2)
    file.truncate()
    file.close()

    a = random.choice(list(G.nodes))
    b = random.choice(list(G.nodes))
    while G.has_edge(a, b):
        a = random.choice(list(G.nodes))
        b = random.choice(list(G.nodes))

    a = node_number * a[0] + a[1]
    b = node_number * b[0] + b[1]
    return a, b
