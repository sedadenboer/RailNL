from code.classes.traject import Traject

import random
import copy
    

def random_traject(graph):
    """
    Create new traject based on the following algorithm:
    - 1st connection of traject is chosen from unused connections @ lijnvoering 
    - at each junction, new connection is chosen from unused connections @ lijnvoering 
      if not possible, non-unique connection is chosen
    - at each junction, new connection is chosen with station that is not yet @ traject
      if not possible, connection with non-unique station is chosen
    """
    # create new traject with first connection selected from unused connections @ lijnvoering
    chosen_connection = random.choice(list(graph.unused_connections))
    [station1, station2] = chosen_connection.stations
    duration = chosen_connection.duration
    new_traject = Traject([station1, station2], int(float(duration)), [chosen_connection])
    graph.add_connection(chosen_connection)
    cur_station = graph.stations[station2]

    # add new connections to traject as long as time constraint permits
    traject_not_finished = True
    while traject_not_finished:
        
        # chose new part of traject from connections not yet @ lijnvoering
        unused_connections_cur_station = set(cur_station.connections.keys()).intersection(graph.unused_connections)
        if len(unused_connections_cur_station) != 0: 
            connection = random.choice(list(unused_connections_cur_station))
            duration = connection.duration
            connected_station = cur_station.connections[connection]
        # if not possible, chose non-unique connection
        else:
            connection = random.choice(list(cur_station.connections.keys()))
            duration = connection.duration
            connected_station = cur_station.connections[connection]

        # if selected station is in current traject, select new station if possible
        con_stations = list(cur_station.connections.values())
        if all(item in new_traject.stations for item in con_stations) == False:
            while (connected_station in new_traject.stations):
                connection = random.choice(list(cur_station.connections.keys()))
                duration = connection.duration
                connected_station = cur_station.connections[connection]
                
        # add connections to traject if within time constraint
        cur_station = graph.stations[connected_station]
        if new_traject.update_traject(connected_station, int(float(duration)), connection, graph.max_duration) == True:
            graph.add_connection(connection)
        else:
            traject_not_finished = False
    
    # if finished, add traject to lijnvoering 
    graph.add_traject(new_traject)
    

def random_algorithm_one_sol(graph):
    """
    Algorithm that looks for combination of trajects such that all connections are used
    """
    print('\nloading randomly constructed lijnvoering...\n')

    solution = False
    nTry = 0 

    while solution == False:

        # for each try, create a new graph 
        nTry += 1
        new_graph = copy.deepcopy(graph)
        
        # if not yet max. trajects and solution not found, add new traject to lijnvoering 
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering) < new_graph.max_trajects:
            random_traject(new_graph)

        # if all connections used, print solution and stop loop
        if len(new_graph.unused_connections) == 0:
            solution = True
            
            print('Found the following correct lijnvoering at try number:', nTry)
            for i, traject in enumerate(new_graph.lijnvoering):
                print('traject', i + 1,':', traject.stations)
                print('duration:', traject.duration)
                print('connections', traject.connections)

    
    return new_graph


def random_algorithm_opt_sol(graph):
    """
    Algorithm that looks for combination of trajects such that quality goal-fucntion is optimized
    """
    print('\nloading randomly constructed lijnvoering...\n')

    opt_K = 0
    opt_map = graph
    nTry = 0

    all_K = []
    dict_K = dict()

    while nTry < 10000:

        # for each try, create a new graph 
        nTry += 1
        new_graph = copy.deepcopy(graph)
        
        # if not yet max. trajects and solution not found, add new traject to lijnvoering 
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering) < new_graph.max_trajects:
            random_traject(new_graph)

        # add quality-goalfunction
        new_graph.lijnvoering_kwaliteit(set(new_graph.used_connections), new_graph.available_connections, new_graph.lijnvoering)
        
        # if quality higher then optimal, replace optimal results
        if new_graph.K > opt_K:
            opt_K = new_graph.K
            opt_map = new_graph
        
        # steekproef variables
        all_K.append(new_graph.K)
        if len(new_graph.lijnvoering) in dict_K.keys():
            dict_K[len(new_graph.lijnvoering)].append(new_graph.K)
        else:
            dict_K[len(new_graph.lijnvoering)] = [new_graph.K]
            
    return opt_map, opt_K, all_K, dict_K



