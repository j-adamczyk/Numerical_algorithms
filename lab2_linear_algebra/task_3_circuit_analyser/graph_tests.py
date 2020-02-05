import graph_generators
import main


def test_random_connected_graph(node_number, file_name, edge_probability):
    (a, b) = graph_generators.generate_random_connected_graph(node_number, file_name, edge_probability)
    main.calculate_currents(file_name, a, b, 100)


def test_random_cubic_graph(node_number, file_name):
    (a, b) = graph_generators.generate_random_cubic_graph(node_number, file_name)
    main.calculate_currents(file_name, a, b, 100)


def test_random_graph_with_bridge(node_number, file_name, edge_probability):
    (a, b) = graph_generators.generate_random_graph_with_bridge(node_number, file_name, edge_probability)
    main.calculate_currents(file_name, a, b, 100)


def test_random_grid_graph(node_number, file_name):
    (a, b) = graph_generators.generate_random_grid_graph(node_number, file_name)
    main.calculate_currents(file_name, a, b, 100)


# in some cases tests may not pass, e. g. because of insufficient memory or singular matrix
# the IndexError is known, but sadly there wasn't enough time to fix it

# if IndexError becomes to common, use:
# while True:
#   try:
#       graph generating code
#   except Exception:
#       pass
# and stop program after genering graph

# very large graph tests, without visualization

#test_random_connected_graph(1500, "data.txt", 0.01)
#test_random_cubic_graph(4000, "data.txt")
#test_random_graph_with_bridge(2000, "data.txt", 0.01)
#test_random_grid_graph(50, "data.txt")


# small graph tests, with visualization


# random connected graphs
#(a, b) = graph_generators.generate_random_connected_graph(15, "data.txt", 0.3)
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_connected_15", "Random connected graph, 15 nodes", "show")

#(a, b) = graph_generators.generate_random_connected_graph(40, "data.txt", 0.1)
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_connected_40", "Random connected graph, 40 nodes", "show")

#(a, b) = graph_generators.generate_random_connected_graph(75, "data.txt", 0.08)
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_connected_75", "Random connected graph, 75 nodes", "show")


# random cubic graphs
#(a, b) = graph_generators.generate_random_cubic_graph(16, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 1000)
#main.plot_graph(G, "random_cubic_16", "Random cubic graph, 16 nodes", "show")

#(a, b) = graph_generators.generate_random_cubic_graph(40, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 1000)
#main.plot_graph(G, "random_cubic_40", "Random cubic graph, 40 nodes", "show")

#(a, b) = graph_generators.generate_random_cubic_graph(76, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 1000)
#main.plot_graph(G, "random_cubic_76", "Random cubic graph, 76 nodes", "show")


# random graphs with bridges
#(a, b) = graph_generators.generate_random_graph_with_bridge(15, "data.txt", 0.3)
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_with_bridge_15", "Random connected graph with bridge, 15 nodes", "show")

#(a, b) = graph_generators.generate_random_graph_with_bridge(40, "data.txt", 0.5)
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_with_bridge_40", "Random connected graph with bridge, 40 nodes", "show")

#(a, b) = graph_generators.generate_random_graph_with_bridge(75, "data.txt", 0.1)
#G = main.calculate_currents("data.txt", a, b, 1000)
#main.plot_graph(G, "random_with_bridge_75", "Random connected graph with bridge, 75 nodes", "show")

# random grid graphs
#(a, b) = graph_generators.generate_random_grid_graph(3, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_grid_9", "Random grid graph, 9 nodes", "show")

#(a, b) = graph_generators.generate_random_grid_graph(4, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_grid_16", "Random grid graph, 16 nodes", "show")

#(a, b) = graph_generators.generate_random_grid_graph(5, "data.txt")
#G = main.calculate_currents("data.txt", a, b, 10)
#main.plot_graph(G, "random_grid_25", "Random grid graph, 25 nodes", "show")
