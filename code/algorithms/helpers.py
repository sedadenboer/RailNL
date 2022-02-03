# helpers.py
#
# Minor Programmeren
# Bèta-Programma
#
# Contains functions that have to be used frequently.

import csv
import random
from code.classes.trajectory import Trajectory

MAX_TRAJECTORIES_NSH = 7


def begin_stations(graph):
    """
    Find stations in railway network which have one connection.
    """

    start_stations = []

    for station in graph.stations.values():
        if len(station.connections) == 1:
            start_stations.append(station)

    return start_stations


def visited_all_stations(graph):
    """
    Check whether all stations in railway network are in lines.
    """

    return len(graph.visited_stations) == len(graph.stations)


def reached_max_depth(graph):
    """
    Check whether max. number of trajectories are in lines.
    """

    return len(graph.lines.trajectories) == graph.max_trajectories


def start_new_trajectory(graph, station1, station2, duration, chosen_connection):
    """
    Create new trajectory based on start connection.
    """

    new_trajectory = Trajectory([station1, station2], int(float(duration)), [chosen_connection])
    graph.add_connection(chosen_connection)
    cur_station = graph.stations[station2]

    return new_trajectory, cur_station


def first_connection(chosen_connection, station_obj=None):
    """
    Find connection variables based on chosen connection.
    """

    if station_obj is not None:
        station1 = station_obj.name
        station2 = list(station_obj.connections.values())[0]
        duration = chosen_connection.duration
    else:
        [station1, station2] = chosen_connection.stations
        duration = chosen_connection.duration

    return station1, station2, duration


def new_connection(algorithm, options, cur_station):
    """
    Find new connection by algoritm and options.
    """

    chosen_connection = algorithm(options)
    duration = chosen_connection.duration
    new_station = cur_station.connections[chosen_connection]

    return chosen_connection, duration, new_station


def unused_connections(cur_station, graph):
    """
    At junction, check if connection not yet in lines is possible.
    """

    unused_cur_station = set(cur_station.connections.keys()).intersection(graph.unused_connections)

    return list(unused_cur_station)


def unique_station_at_trajectory(cur_station, stations_at_trajectory):
    """
    Check whether connection with station not yet at trajectory is possible.
    """

    con_stations = list(cur_station.connections.values())

    return not all(item in stations_at_trajectory for item in con_stations)


def new_trajectory(graph, start_stations, algorithm, prefer_unused_connection):
    """
    Create new trajectory and add to lines.
    """

    # if possible, set single-connection station as start station
    if len(graph.lines.trajectories) < len(start_stations):
        station_obj = start_stations[len(graph.lines.trajectories)]
        chosen_connection = list(station_obj.connections.keys())[0]
        chosen_connection = graph.available_connections[int(chosen_connection.id) - 1]
        [station1, station2, duration] = first_connection(chosen_connection, station_obj)
    # else, randomly select start station ..
    else:
        # .. from unused connections @ lines
        if prefer_unused_connection and len(graph.unused_connections) != 0:
            chosen_connection = random.choice(list(graph.unused_connections))
        # .. from all connections available
        else:
            chosen_connection = random.choice(list(graph.available_connections))
        [station1, station2, duration] = first_connection(chosen_connection)

    # start new trajectory
    [new_trajectory, cur_station] = start_new_trajectory(graph, station1, station2, duration, chosen_connection)

    # add new connections to trajectory
    extend_trajectory = True

    while extend_trajectory:
        # choose new connection from unused or all connections
        if prefer_unused_connection and unused_connections(cur_station, graph):
            options = unused_connections(cur_station, graph)
        else:
            options = list(cur_station.connections.keys())

        # select next part of trajectory by algorithm
        chosen_connection, duration, new_station = new_connection(algorithm, options, cur_station)

        # if selected station is already in trajectory..
        if unique_station_at_trajectory(cur_station, new_trajectory.stations):
            # .. find new connection from all connections
            if not prefer_unused_connection:
                options = list(cur_station.connections.keys())
                while (new_station in new_trajectory.stations):
                    options.remove(chosen_connection)
                    chosen_connection, duration, new_station = new_connection(algorithm, options, cur_station)
            # .. first try to find new connection from unused connections
            else:
                options = unused_connections(cur_station, graph)

                while (new_station in new_trajectory.stations) and len(options) > 1:
                    options.remove(chosen_connection)
                    chosen_connection, duration, new_station = new_connection(algorithm, options, cur_station)

                options = list(cur_station.connections.keys())

                while (new_station in new_trajectory.stations):
                    options.remove(chosen_connection)
                    chosen_connection, duration, new_station = new_connection(algorithm, options, cur_station)

            # add valid connection to trajectory if within time constraint
            if new_trajectory.update_trajectory(new_station, int(float(duration)), chosen_connection, graph.max_duration):
                cur_station = graph.stations[new_station]
                graph.add_connection(chosen_connection)
            # if impossible to add connection within time constraint, end trajectory
            else:
                extend_trajectory = False

        # if impossible to select station not yet in trajectory, end trajectory
        else:
            extend_trajectory = False

    # if trajectory is finished, add trajectory to lines
    graph.lines.add_trajectory(new_trajectory)


def write_output_to_csv(final_graph, algorithm_name, extension):

    # create filename based on region and algorithm
    if final_graph.max_trajectories == MAX_TRAJECTORIES_NSH:
        file = 'results/' + str(algorithm_name) + '/Holland/output' + str(extension) + '.csv'
    else:
        file = 'results/' + str(algorithm_name) + '/Nationaal/output' + str(extension) + '.csv'

    # create csv file
    with open(file, 'w', encoding='UTF8') as f:

        writer = csv.writer(f)

        # write the header
        writer.writerow(['train', 'stations'])

        # write the data
        for trajectory in final_graph.lines.trajectories:
            writer.writerow([f'train_{final_graph.lines.trajectories.index(trajectory)+1}',
                            str(trajectory.stations).translate({39: None})])

        # write the footer
        writer.writerow(['score', final_graph.K])


def write_to_csv(final_graph, all_K, all_opt_K, algorithm_name, extension):

    # create filename based on region and algorithm
    if final_graph.max_trajectories == MAX_TRAJECTORIES_NSH:
        file_all_K = 'data/' + str(algorithm_name) + '_Holland_all_K' + str(extension) + '.csv'
        file_opt_K = 'data/' + str(algorithm_name) + '_Holland_opt_K' + str(extension) + '.csv'
    else:
        file_all_K = 'data/' + str(algorithm_name) + '_Nationaal_all_K' + str(extension) + '.csv'
        file_opt_K = 'data/' + str(algorithm_name) + '_Nationaal_opt_K' + str(extension) + '.csv'

    # create csv file for all_K (List)
    with open(file_all_K, 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(all_K)

    # create csv file for opt_K (Dictionary)
    with open(file_opt_K, 'w', encoding='UTF8') as f:
        for key in all_opt_K.keys():
            f.write("%s,%s\n" % (key, all_opt_K[key]))


def print_statement_main(final_graph):
    """
    Print statement when final lines solution is found.
    """

    print("\nFound optimal K of:", final_graph.K)
    print("\n")

    for trajectory in final_graph.lines.trajectories:
        print("Trajectory", final_graph.lines.trajectories.index(trajectory), "\n", ", ".join(trajectory.stations))
