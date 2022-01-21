from code.classes.traject import Traject
from code.classes.lijnvoering import Lijnvoering

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

        permitted_connection = True
        ########################### ONLY 1x STATION @ TRAJECT #########################
        con_stations = list(cur_station.connections.values())
        # if selected station is in current traject, select new station if possible
        if all(item in new_traject.stations for item in con_stations) == False:
            while (connected_station in new_traject.stations):
                connection = random.choice(list(cur_station.connections.keys()))
                duration = connection.duration
                connected_station = cur_station.connections[connection]
        # if not possible, end traject as 2x the same station in 1 traject is not possible
        else: 
            traject_not_finished = False
            permitted_connection = False
                
        # add connections to traject if within time constraint
        if permitted_connection == True:
            cur_station = graph.stations[connected_station]
            if new_traject.update_traject(connected_station, int(float(duration)), connection, graph.max_duration) == True:
                graph.add_connection(connection)
            else:
                traject_not_finished = False
    
    # if finished, add traject to lijnvoering 
    graph.lijnvoering.add_traject(new_traject)

def random_algorithm_unique_sols(graph):
    """
    ...
    """
    print('\nloading randomly constructed lijnvoering...\n')

    ######################### check that comparison lijnvoering works ###############################
    # # traject 1
    # [station1, station2] = graph.available_connections[1].stations
    # duration = graph.available_connections[1].duration
    # traject1 = Traject([station1, station2, 'maastricht'], int(float(duration)), [graph.available_connections[1], graph.available_connections[2]])

    # # traject 2
    # [station1, station2] = graph.available_connections[15].stations
    # duration = graph.available_connections[15].duration
    # traject2 = Traject([station1, station2, 'maastricht'], int(float(duration)), [graph.available_connections[15], graph.available_connections[2]])

    # # traject 3
    # [station1, station2] = graph.available_connections[15].stations
    # duration = graph.available_connections[15].duration
    # traject3 = Traject(['maastricht', station2, station1], int(float(duration)), [graph.available_connections[2], graph.available_connections[15]])

   
    # # lijnvoering 1
    # lijnvoering1 = Lijnvoering()
    # lijnvoering1.add_traject(traject1)
    # lijnvoering1.add_traject(traject2)

    # # lijnvoering 2
    # lijnvoering2 = Lijnvoering()
    # lijnvoering2.add_traject(traject3)
    # lijnvoering2.add_traject(traject1)

    # print(lijnvoering1 == lijnvoering2)


    nTry = 0 
    nSolutions = 0
    nUnique = 0
    nonUnique = 0
    same_k = 0

    lijnvoeringen_by_K = dict()
    K_counter = dict()

    while nTry < 100000:

        # for each try, create a new graph 
        nTry += 1
        new_graph = copy.deepcopy(graph)
        
        # if not yet max. trajects and solution not found, add new traject to lijnvoering 
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering.trajecten) < new_graph.max_trajects:
            random_traject(new_graph)

        nSolutions += 1
        new_graph.lijnvoering_kwaliteit(set(new_graph.used_connections), new_graph.available_connections, new_graph.lijnvoering.trajecten)

        # if found non-unique K
        if new_graph.K in lijnvoeringen_by_K.keys():
            same_k += 1
            # check if duplicate if there is only one lijnvoeringen with same K
            if type(lijnvoeringen_by_K[new_graph.K]) != list:
                # if new lijnvoering turn out to be unique
                if lijnvoeringen_by_K[new_graph.K] != new_graph.lijnvoering:
                    lijnvoeringen_by_K[new_graph.K] = [lijnvoeringen_by_K[new_graph.K], new_graph.lijnvoering]
                    K_counter[new_graph.K] += 1
                    nUnique += 1
                else:
                    nonUnique += 1
            # check if duplicate if there are already more unique lijnvoeringen with same K
            else:
                Unique = True
                for lijnvoering in lijnvoeringen_by_K[new_graph.K]:
                    if lijnvoering == new_graph.lijnvoering:
                        nonUnique += 1
                        Unique = False
                # if new lijnvoering turn out to be unique
                if Unique == True:
                    lijnvoeringen_by_K[new_graph.K] = lijnvoeringen_by_K[new_graph.K] + [new_graph.lijnvoering]
                    K_counter[new_graph.K] += 1
                    nUnique += 1
        # if found unique K
        else:
            nUnique += 1
            lijnvoeringen_by_K[new_graph.K] = new_graph.lijnvoering
            K_counter[new_graph.K] = 1


        print(f"n: {nTry}")
        print(f"Solutions: {nSolutions}")
        print(f"nUnique: {nUnique}")
        print(f"nNon-unique: {nonUnique}\n")
        print(f"lijnvoeringen with same_k: {same_k}")


    return new_graph
        
 

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
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering.trajecten) < new_graph.max_trajects:
            random_traject(new_graph)

        # if all connections used, print solution and stop loop
        if len(new_graph.unused_connections) == 0:
            solution = True
            
            print('Found the following correct lijnvoering at try number:', nTry)
            for i, traject in enumerate(new_graph.lijnvoering.trajecten):
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
    nSolutions = 0

    all_K = []
    dict_K = dict()

    while nSolutions < 1000:

        # for each try, create a new graph 
        new_graph = copy.deepcopy(graph)
        
        # if not yet max. trajects and solution not found, add new traject to lijnvoering 
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering.trajecten) < new_graph.max_trajects:
            random_traject(new_graph)

        # only valid solution if all stations are visited
        visited_stations = set()
        for traject in new_graph.lijnvoering.trajecten:
            for station in traject.stations:
                visited_stations.add(station)
        
        if len(visited_stations) == 22:

            nSolutions += 1
        
            # add quality-goalfunction
            new_graph.lijnvoering_kwaliteit(set(new_graph.used_connections), new_graph.available_connections, new_graph.lijnvoering.trajecten)
            
            # if quality higher then optimal, replace optimal results
            if new_graph.K > opt_K:
                opt_K = new_graph.K
                opt_map = new_graph
            
            # steekproef variables
            all_K.append(new_graph.K)
            if len(new_graph.lijnvoering.trajecten) in dict_K.keys():
                dict_K[len(new_graph.lijnvoering.trajecten)].append(new_graph.K)
            else:
                dict_K[len(new_graph.lijnvoering.trajecten)] = [new_graph.K]
            
    return opt_map, opt_K, all_K, dict_K



