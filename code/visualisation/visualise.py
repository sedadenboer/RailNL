# visualise.py
#
# Minor Programmeren
# Bèta-Programma
#
# Contains functions to visualise the line solution results.

from matplotlib import pyplot as plt
import os
import sys
from csv import reader


def start_comparing(goal):
    """
    Creates a comparison between different data as given by the user.
    """

    all_files = os.listdir("./data/")
    compare_all_K = []
    compare_opt_K = []

    # select all files to compare
    for file in all_files:

        # based on answer, add file to list
        if (('all_K' in file) and (goal.upper() == "D" or goal.upper() == "B")) \
                or (('opt_K' in file) and (goal.upper() == "I" or goal.upper() == "B")):
            add = input(f"Would you like to add {file} to comparison? yes (return y), no return (n): ")

            if add.upper() != "Y" and add.upper() != "N":
                sys.exit("No valid input")

            if ('all_K' in file) and (goal.upper() == "D" or goal.upper() == "B") and add.upper() == "Y":
                compare_all_K.append(file)
            elif ('opt_K' in file) and (goal.upper() == "I" or goal.upper() == "B") and add.upper() == "Y":
                compare_opt_K.append(file)

    # start visualisation
    if len(compare_all_K) != 0:
        visualise_K_distribution_comparison(compare_all_K)
    if len(compare_opt_K) != 0:
        visualise_opt_K_all_algorithms(compare_opt_K)


def visualise_start(railway_map, map_name):
    """
    Visualisation code that displays the railnetwork of the selected area.
    """

    print("\nLoading main visualisation...\n")

    # load station information
    x = []
    y = []
    z = []
    for station in railway_map.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        z.append(station.name)

    # create scatterplot of based on x- and y-coordinates of stations
    plt.figure(figsize=(30, 20))
    plt.scatter(y, x, c='black', s=15)

    # add station name to each scatter plot point
    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

    # plot all connections between stations
    for connection in railway_map.available_connections:

        # retrieve initial information of all connections
        station1 = railway_map.stations[connection.stations[0]]
        x1 = float(station1.x_coord)
        y1 = float(station1.y_coord)
        station2 = railway_map.stations[connection.stations[1]]
        x2 = float(station2.x_coord)
        y2 = float(station2.y_coord)

        # plot connection between Stations
        plt.plot([y1, y2], [x1, x2], c='black', alpha=0.25)

        # add duration of connection
        plt.annotate(connection.duration, ((y1 + y2) / 2, (x1 + x2) / 2), textcoords="offset points", xytext=(0, 10),
                     ha='center')

    # add titles to plot of Railway Network and remove x- and y-tics
    plt.suptitle("Intercity connections North- and South-Holland", fontsize=25, y=0.93)
    plt.title('Duration in minutes', fontsize=18, y=1.01)
    plt.xticks([], [])
    plt.yticks([], [])

    # save figure
    plt.savefig(f"docs/Stations_{map_name}")


def visualise_solution_compact(final_graph, algorithm_name, extension, q=''):
    """
    Visualisation code that displays the found 'lines'.
    """

    print("\nLoading compact Lines visualisation...\n")

    # select colors for trajectories
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(final_graph.max_trajectories):
        colors.append(cm(i/final_graph.max_trajectories))

    # load station information
    x = []
    y = []
    z = []
    for station in final_graph.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        station_name = station.name.split()
        new_name = ""
        for i in range(len(station_name)):
            if i == 0:
                new_name += station_name[i]
            else:
                new_name += '-' + station_name[i][0]
        z.append(new_name)

    # create scatterplot of based on x- and y-coord of stations
    plt.figure(figsize=(20, 25))
    plt.scatter(y, x, c='black', s=15)

    # add station name to each scatter plot point
    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

    # plot all connections between stations
    for connection in final_graph.available_connections:

        # retrieve initial information of all connections
        station1 = final_graph.stations[connection.stations[0]]
        x1 = float(station1.x_coord)
        y1 = float(station1.y_coord)
        station2 = final_graph.stations[connection.stations[1]]
        x2 = float(station2.x_coord)
        y2 = float(station2.y_coord)

        # plot connection between stations
        plt.plot([y1, y2], [x1, x2], c='black', alpha=1, linestyle=':')

        # add duration of connection
        plt.annotate(connection.duration, ((y1 + y2) / 2, (x1 + x2) / 2), textcoords="offset points", xytext=(0, 10),
                     ha='center')

    connection_visited = dict()
    # for each trajectory, plot all connections
    n = 0
    for trajectory in final_graph.lines.trajectories:
        n += 1
        c = 0
        for connection in trajectory.connections:
            c += 1
            connection_visited[connection.id] = connection_visited.get(connection.id, 0) + 1
            times_visited = connection_visited[connection.id]

            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)

            plt.plot([y1 - 0.005 * (times_visited - 1), y2 - 0.005 * (times_visited-1)],
                     [x1 + 0.002 * (times_visited - 1), x2 + 0.002 * (times_visited - 1)], c=colors[n - 2],
                     alpha=0.5, linewidth=4.0, label=f"Trajectory {n}" if c == 1 else "")

    # add titles to plot of Railway Network and remove x- and y-tics
    plt.suptitle(f"Railnetwork generated by {algorithm_name} Algorithm (K = {str(round(final_graph.K, 2))}, \
                 p = {str(round(len(set(final_graph.used_connections))/len(final_graph.available_connections), 2))})",
                 fontsize=20, y=0.9)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.axis('scaled')
    plt.legend()

    # create filename based on region and algorithm
    if final_graph.max_trajectories == 7:
        file = 'results/' + str(algorithm_name) + '/' + q + '/Holland/visualisation_compact' + extension
    else:
        file = 'results/' + str(algorithm_name) + '/' + q + '/Nationaal/visualisation_compact' + extension

    # save figure
    plt.savefig(file)


def visualise_solution(final_graph, algorithm_name):
    """
    Visualisation code that displays the found 'lines'
    """

    print("\nLoading solution visualisation...\n")

    # select colors for trajectories
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(final_graph.max_trajectories):
        colors.append(cm(i/final_graph.max_trajectories))

    # load station information
    x = []
    y = []
    z = []
    for station in final_graph.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        z.append(station.name)

    # determine height of figure based on number of trajectories
    if len(final_graph.lines.trajectories) > 6:
        fig = plt.figure(figsize=(70, 70))
    else:
        fig = plt.figure(figsize=(70, 40))

    # create subplot for each trajectory
    n_trajectories = 1
    fig.subplots_adjust(hspace=0.4, wspace=0.2)

    for trajectory in final_graph.lines.trajectories:

        # determine dimensions of figure based on number of trajectories
        if len(final_graph.lines.trajectories) > 9:
            ax = fig.add_subplot(5, 4, n_trajectories)
        elif len(final_graph.lines.trajectories) > 6 and len(final_graph.lines.trajectories) < 10:
            ax = fig.add_subplot(3, 3, n_trajectories)
        else:
            ax = fig.add_subplot(2, 3, n_trajectories)

        # update total number of trajectories and set title to subplot
        n_trajectories += 1
        ax.set_title(f'Trajectory {n_trajectories - 1}: {trajectory.stations[0]} --> \
                     {trajectory.stations[-1]} ({trajectory.duration} min.)', fontsize=25)

        # create main rail network with station names
        ax.scatter(y, x, c='black', s=15)
        for i, txt in enumerate(z):
            ax.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

        # plot all connections between stations including the duration
        for connection in set(final_graph.available_connections):
            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)
            ax.plot([y1, y2], [x1, x2], c='black', alpha=0.20)
            ax.annotate(connection.duration, ((y1 + y2) / 2, (x1 + x2) / 2),
                        textcoords="offset points", xytext=(0, 10), ha='center')

        # plot all connections in the trajectory
        for connection in trajectory.connections:
            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)
            ax.plot([y1, y2], [x1, x2], c=colors[n_trajectories - 2], alpha=0.25, linewidth=4.0)
            ax.annotate(connection.duration, ((y1 + y2) / 2, (x1 + x2) / 2),
                        textcoords="offset points", xytext=(0, 10), ha='center')

        # remove x- and y-tics
        ax.set_xticks([])
        ax.set_yticks([])

    # add title
    fig.suptitle(f"Railnetwork generated by Random Algorithm (K = {final_graph.K})", fontsize=45, y=0.93)

    # create filename
    if final_graph.max_trajectories == 7:
        file = 'results/' + str(algorithm_name) + '/Holland/visualisation'
    else:
        file = 'results/' + str(algorithm_name) + '/Nationaal/visualisation'
    if final_graph.prefer_unused_connection:
        file += '_prefer_unused'

    # save figure
    fig.savefig(file)


def visualise_opt_K_improvement(all_opt_K, algorithm_name, extension):
    """
    Visualize how the K value improves during the iterations.
    """

    print("\nLoading visualisation of improvement K over iterations ...\n")

    # plot the optimal K value after each iteration
    fig = plt.figure(figsize=(20, 20))
    plt.plot(all_opt_K.keys(), all_opt_K.values(), color='black')
    plt.xlabel('iterations', fontsize=20, labelpad=25)
    plt.ylabel('K', fontsize=20, labelpad=25)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # add title
    plt.title(f"Improvement of K after {len(all_opt_K.keys())} iterations using {algorithm_name} Algorithm", fontsize=25,
              pad=25)

    # create file name
    file = f"plots/Opt_K_Improvement_{algorithm_name}{extension}"

    fig.savefig(file)


def retrieve_name(file):
    """
    Retrieves algorithm name and chosen options from filename.
    """

    name = ''

    if 'Random' in file:
        name = 'Random'
    elif 'Greedy' in file:
        name = 'Greedy'
    elif 'Hillclimber' in file:
        name = 'Hillclimber'

        if 'remove_K' in file:
            name += ' / remove K'
        else:
            name += ' / remove random'
        if 'random_start' in file:
            name += ' / random start'
        else:
            name += ' / greedy start'
        if 'sim_anneal' in file:
            name += ' / sim anneal'
        if 'restart' in file:
            name += ' / restart'

    if 'prefer_unused' in file:
        name += ' / prefer unused'
    
    return name
            
def visualise_opt_K_all_algorithms(compare_opt_K):
    """
    Visualize how the optimal K compares for all algorithms after a number of iterations.
    """

    print("\nLoading visualisation of optimal K all algorithms ...\n")

    fig = plt.figure(figsize=(20, 20))

    # select colors for all distributions
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(len(compare_opt_K)):
        colors.append(cm(i/len(compare_opt_K)))

    # loop over all solutions
    all_values = []
    all_names = []
    for file in compare_opt_K:
        # retrieve name from file_name
        retrieve_name(file)
        all_names.append(name)

        # add values
        with open('data/' + file, 'r') as read_obj:
            values = []
            for row in reader(read_obj):
                values.append(float(row[1]))

        all_values.append(values)

    # create plot
    min_iterations = min(map(len, all_values))
    counter = 0
    for i in range(len(all_values)):
        plt.plot(list(range(min_iterations)), all_values[i][:min_iterations], color=colors[counter], label=all_names[i])
        counter += 1

    # add titles etc.
    plt.xlabel('iterations', fontsize=20)
    plt.ylabel('K', fontsize=20)
    plt.legend(title='Algorithm')
    fig.suptitle("Improvement K over iterations", fontsize=25, y=0.93)

    # save a new image if variables are changed
    fig.savefig("plots/compare_distributions_K")


def visualise_K_distribution_comparison(compare_all_K):
    """
    Visualize the distribution of K in a histogram for all algorithms.
    """

    print("\nLoading visualisation of distribution of K ...\n")

    fig = plt.figure(figsize=(20, 20))

    # select colors for all distributions
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(len(compare_all_K)):
        colors.append(cm(i/len(compare_all_K)))

    # loop over all solutions
    all_names = []
    all_values = []
    for file in compare_all_K:
        # retrieve name from file_name
        retrieve_name(file)
        all_names.append(name)

        with open('data/' + file, 'r') as read_obj:
            # csv => list => histogram
            all_K = list(reader(read_obj))[0]
            all_K = [float(item) for item in all_K]
            all_values.append(all_K)

    # create plot
    min_iterations = min(map(len, all_values))
    counter = 0
    for i in range(len(all_values)):
        plt.hist(all_values[i][:min_iterations], bins=250, color=colors[counter], label=all_names[i], alpha=0.5)
        counter += 1

    # add titles, legenda and ticks to figure
    plt.xlabel('K', fontsize=20)
    plt.ylabel('frequency', fontsize=20)
    plt.xticks(fontsize=10)
    plt.legend(title='Algorithm')
    fig.suptitle("Frequency Histogram of K", fontsize=25, y=0.93)

    # save a new image if variables are changed
    fig.savefig("plots/compare_distributions_K")
