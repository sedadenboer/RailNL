from code.classes.traject import Traject

import random
import copy

def greedy_choice(options):

    # create dictionary of all durations
    duration_dict = dict()
    for connection in options:
        duration_dict[connection] = connection.duration
    
    # select option with minimum duration
    optimal_connection = min(duration_dict, key=duration_dict.get)

    return optimal_connection

def greedy_traject(graph, start_stations):

    # set single-connection station as start station if possible 
    if len(graph.lijnvoering.trajecten) < len(start_stations):
        station_obj = start_stations[len(graph.lijnvoering.trajecten)]
        station1 = station_obj.name
        station2 = list(station_obj.connections.values())[0]
        chosen_connection = list(station_obj.connections.keys())[0]
        duration = chosen_connection.duration
    # else, create new traject with first connection selected from unused connections @ lijnvoering
    else:
        chosen_connection = random.choice(list(graph.unused_connections))
        [station1, station2] = chosen_connection.stations
        duration = chosen_connection.duration
    
    # start new traject
    new_traject = Traject([station1, station2], int(float(duration)), [chosen_connection])
    graph.add_connection(chosen_connection)
    cur_station = graph.stations[station2]

    # add new connections to traject as long as time constraint permits
    CONTINUE = True
    while CONTINUE:

        # chose new part of traject from connections not yet @ lijnvoering
        unused_connections_cur_station = set(cur_station.connections.keys()).intersection(graph.unused_connections)
        if len(unused_connections_cur_station) != 0: 
            connection = greedy_choice(list(unused_connections_cur_station))
            duration = connection.duration
            connected_station = cur_station.connections[connection]
        else:
            connection = greedy_choice(list(cur_station.connections.keys()))
            duration = connection.duration
            connected_station = cur_station.connections[connection]

        # if selected station is in current traject, select new station if possible
        # if not possible, end traject as 2x the same station in 1 traject is not allowed
        permitted_connection = True
        con_stations = list(cur_station.connections.values())
        if all(item in new_traject.stations for item in con_stations) == False:
            while (connected_station in new_traject.stations):
                connection = random.choice(list(cur_station.connections.keys()))
                duration = connection.duration
                connected_station = cur_station.connections[connection]
        else: 
            CONTINUE = False
            permitted_connection = False
                
        # add valid connections to traject if within time constraint
        if permitted_connection == True:
            cur_station = graph.stations[connected_station]
            if new_traject.update_traject(connected_station, int(float(duration)), connection, graph.max_duration) == True:
                graph.add_connection(connection)
            else:
                CONTINUE = False
    
    # if finished, add traject to lijnvoering 
    graph.lijnvoering.add_traject(new_traject)


def greedy_start(graph, iterations):
    """
    Algorithm that looks for combination of trajects such that short-term optimum is reached
    """
    print('\nloading greedy constructed lijnvoering...\n')

    opt_K = 0
    opt_map = graph
    nSolutions = 0

    # find stations with one connection
    start_stations = []
    for station in graph.stations.values():
        if len(station.connections) == 1:
            start_stations.append(station)

    while nSolutions < iterations:

        # for each try, create a new graph 
        new_graph = copy.deepcopy(graph)
        
        # if not yet all stations and max. number of trajects reached, add new traject to lijnvoering 
        while len(new_graph.visited_stations) != len(new_graph.stations) and len(new_graph.lijnvoering.trajecten) < new_graph.max_trajects:
            greedy_traject(new_graph, start_stations)

        # only valid solution if all stations are visited
        if len(new_graph.visited_stations) == len(new_graph.stations):
            nSolutions += 1
        
            # add quality-goalfunction
            new_graph.lijnvoering_kwaliteit(new_graph.used_connections, new_graph.available_connections, new_graph.lijnvoering.trajecten)
            
            # if quality higher then optimal, replace optimal results
            if new_graph.K > opt_K:
                opt_K = new_graph.K
                opt_map = new_graph
            
    return opt_map, opt_K
