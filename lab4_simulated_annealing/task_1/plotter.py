import matplotlib.pyplot as plt


def plot_data(first_path, best_path, distances_plot_data, temperatures_plot_data):
    first_path_xs = []
    first_path_ys = []
    for city in first_path:
        first_path_xs.append(city[0])
        first_path_ys.append(city[1])

    first_path_xs.append(first_path_xs[0])
    first_path_ys.append(first_path_ys[0])

    best_path_xs = []
    best_path_ys = []
    for city in best_path:
        best_path_xs.append(city[0])
        best_path_ys.append(city[1])

    best_path_xs.append(best_path_xs[0])
    best_path_ys.append(best_path_ys[0])

    temperatures_xs = temperatures_plot_data[0]
    temperatures_ys = temperatures_plot_data[1]

    distances_xs = distances_plot_data[0]
    distances_ys = distances_plot_data[1]

    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].plot(first_path_xs, first_path_ys, marker="o", markerfacecolor="red")
    axarr[0, 0].set_title("Before annealing")
    axarr[0, 1].plot(best_path_xs, best_path_ys, marker="o", markerfacecolor="red")
    axarr[0, 1].set_title("After annealing")
    axarr[1, 0].plot(temperatures_xs, temperatures_ys)
    axarr[1, 0].set_title("Temperature")
    axarr[1, 1].plot(distances_xs, distances_ys)
    axarr[1, 1].set_title("Distance")

    plt.show()


def plot_iterations_and_distances(iterations, distances):
    plt.plot(iterations, distances)
    plt.show()
