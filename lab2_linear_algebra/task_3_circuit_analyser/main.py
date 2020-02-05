import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Edge:
    a = -1
    b = -1
    R = 0
    edge_num = -1
    I = 0
    current_from = -1
    current_to = -1


class Vertex:
    a = -1
    degree = 0


def load_graph(file_name, vertices, voltage_a, voltage_b):
    G = nx.Graph()

    with open(file_name, "r") as ins:
        line_num = 0
        for line in ins:
            if line in ['\n', '\r\n']:
                continue

            elements = line.split()
            if len(elements) != 3:
                raise AttributeError("Wrong number of arguments for graph in line " + str(line) + "!")

            a = int(elements[0])
            b = int(elements[1])

            R = float(elements[2])

            if a < 0 or b < 0 or R <= 0:
                raise AttributeError("Attribute in line " + str(line) + "was not a nonnegative number!")

            new_edge = Edge()
            new_edge.a = a
            new_edge.b = b
            new_edge.R = R
            new_edge.edge_num = line_num

            G.add_edge(a, b, edge_data=new_edge)

            if a in vertices:
                vertices[a].append((a, b))
            else:
                vertices[a] = [(a, b)]

            if b in vertices:
                vertices[b].append((a, b))
            else:
                vertices[b] = [(a, b)]

            line_num += 1

    new_edge = Edge()
    new_edge.a = voltage_a
    new_edge.b = voltage_b
    new_edge.R = 0
    new_edge.edge_num = line_num

    G.add_edge(voltage_a, voltage_b, edge_data=new_edge)

    if voltage_a in vertices:
        vertices[voltage_a].append((voltage_a, voltage_b))
    else:
        vertices[voltage_a] = [(voltage_a, voltage_b)]

    if voltage_b in vertices:
        vertices[voltage_b].append((voltage_a, voltage_b))
    else:
        vertices[voltage_b] = [(voltage_a, voltage_b)]

    return G


def get_high_degree_vertices(vertices):
    high_degree_vertices = []

    for vertex in vertices:
        if len(vertices[vertex]) >= 2:
            high_degree_vertex = Vertex()
            high_degree_vertex.a = vertex
            high_degree_vertex.degree = len(vertices[vertex])
            high_degree_vertices.append(high_degree_vertex)

    high_degree_vertices.sort(key=lambda x: x.degree, reverse=True)

    result = []
    for vertex in high_degree_vertices:
        result.append(vertex.a)

    return result


def calculate_currents(file_name, voltage_a, voltage_b, V):
    V = float(V)

    vertices = {}
    G = load_graph(file_name, vertices, voltage_a, voltage_b)
    n = len(G.edges)

    high_degree_vertices = get_high_degree_vertices(vertices)

    cycle_basis = nx.cycle_basis(G)

    # get true cycles, starting with X and ending with X
    for cycle in cycle_basis:
        cycle.append(cycle[0])

    A = np.zeros((n, n))
    B = np.zeros(n)

    row = 0
    for cycle in cycle_basis:
        for vertex in range(0, len(cycle) - 1):
            vertex_from = cycle[vertex]
            vertex_to = cycle[vertex + 1]
            edge_num = G.edges[cycle[vertex], cycle[vertex + 1]]['edge_data'].edge_num

            # did not pass through edge before
            if G.edges[vertex_from, vertex_to]['edge_data'].current_from == -1:
                A[row][edge_num] = G.edges[vertex_from, vertex_to]['edge_data'].R
                G.edges[vertex_from, vertex_to]['edge_data'].current_from = vertex_from
                G.edges[vertex_from, vertex_to]['edge_data'].current_to = vertex_to
            # passed through the edge before and in the same direction as now
            elif G.edges[vertex_from, vertex_to]['edge_data'].current_from == vertex_from:
                A[row][edge_num] = G.edges[vertex_from, vertex_to]['edge_data'].R
            # passed through the edge before and in the opposite direction than now
            else:
                A[row][edge_num] = G.edges[vertex_from, vertex_to]['edge_data'].R * (-1)

            if vertex_from == voltage_a and vertex_to == voltage_b:
                B[row] = V
            elif vertex_from == voltage_b and vertex_to == voltage_a:
                B[row] = -V
        row += 1

    i = 0
    number_of_equations = len(cycle_basis)
    while number_of_equations < len(G.edges):
        high_degree_vertex_incident_edges = vertices[high_degree_vertices[i]]
        for edge in high_degree_vertex_incident_edges:
            # high degree vertex = vertex receiving current
            current_to = G.edges[edge[0], edge[1]]['edge_data'].current_to
            edge_num = G.edges[edge[0], edge[1]]['edge_data'].edge_num
            if high_degree_vertices[i] == current_to:
                A[row][edge_num] = 1.0
            else:
                A[row][edge_num] = -1.0
        row += 1
        number_of_equations += 1
        i += 1

    Is = np.linalg.solve(A, B)

    vertices = {}
    result = nx.DiGraph()
    for edge in G.edges(data=True):
        current = Is[edge[2]['edge_data'].edge_num]
        a = edge[2]['edge_data'].current_from
        if a == -1:
            a = edge[0]
        b = edge[2]['edge_data'].current_to
        if b == -1:
            b = edge[1]
        if current < 0:
            a, b = b, a
            current *= -1
        R = edge[2]['edge_data'].R
        result.add_edge(a, b, I=current, R=R)

        if a in vertices:
            vertices[a].append((a, b))
        else:
            vertices[a] = [(a, b)]

        if b in vertices:
            vertices[b].append((a, b))
        else:
            vertices[b] = [(a, b)]

    correct = check_currents(result, vertices, V)
    if not correct:
        raise ValueError("Error: calculations for graph were not correct!")

    return result


def check_currents(G, vertices, V):
    for vertex in vertices:
        currents_sum = 0
        for edge in vertices[vertex]:
            I = G.edges[edge[0], edge[1]]['I']
            R = G.edges[edge[0], edge[1]]['R']
            if I*R > V:
                return False

            if edge[1] == vertex:
                currents_sum += G.edges[edge[0], edge[1]]['I']
            else:
                currents_sum -= G.edges[edge[0], edge[1]]['I']
        if not math.isclose(currents_sum, 0, abs_tol=1e-5):
            return False
    return True


def plot_graph(G, file_name, title, show):
    edges, weights = zip(*nx.get_edge_attributes(G, "I").items())
    layout = nx.kamada_kawai_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'I')
    plt.title(title)
    nx.draw(G, pos=layout, node_color='Grey', edgelist=edges, edge_color=weights, with_labels=True,
                                 edge_labels=edge_labels, width=3, arrowsize=20, edge_cmap=plt.cm.get_cmap("Reds"))

    plt.savefig(file_name + ".png")
    if show == "show":
        plt.show()
