
from code.classes.traject import Traject

import random
import copy
    

# N_try = 0
# solution = False
# while solution == False: 

# # create empty lijnvoering
# lijnvoering_NZNL = Lijnvoering([], [])

# while len(lijnvoering_NZNL.trajecten) < 7:
    
#     # randomly chose first part of traject from unused connections
#     chosen_connection = random.choice(list(lijnvoering_NZNL.unused_connections))
    
#     # retrieve stations and duration of this connection
#     station_1 = df_connections['station1'][chosen_connection]
#     station_2 = df_connections['station2'][chosen_connection]
#     duration = df_connections['distance'][chosen_connection]
    
#     # create new traject, add connection to lijnvoering and initialize current station
#     new_traject = Traject([station_1, station_2], duration, [chosen_connection])
#     lijnvoering_NZNL.add_connection(chosen_connection)
#     cur_station = stations[station_2]

#     # as long as traject is not finished
#     while True:
#         # print("current trajectory:", new_traject.stations)
#         # print("current duration of trajectory (min):", new_traject.duration)
#         # print("bereden verbindingen (lijnvoering):", set(lijnvoering_NL.verbindingen))

#         # first, try to chose (randomly) new part of traject from connections not yet in lijnvoering
#         unused_connections_cur_station = set(cur_station.connections.keys()).intersection(lijnvoering_NZNL.unused_connections)
#         if len(unused_connections_cur_station) != 0: 
#             connection_number = random.choice(list(unused_connections_cur_station))
#             connected_station, duration = cur_station.connections[connection_number]
#         # else, chose from connections already in lijnvoering
#         else:
#             connection_number = random.choice(list(cur_station.connections.keys()))
#             connected_station, duration = cur_station.connections[connection_number]

#         # if connection with station that is not in current traject is possible & selected station is in current traject, try to find new station
#         con_stations = [s[0] for s in list(cur_station.connections.values())]
#         if all(item in new_traject.stations for item in con_stations) == False:
#             while (connected_station in new_traject.stations):
#                 connection_number = random.choice(list(cur_station.connections.keys()))
#                 connected_station, duration = cur_station.connections[connection_number]

#         # update current station, if possible to add connections within time constraint, do so and add connection 
#         cur_station = stations[connected_station]
#         if new_traject.update_traject(connected_station, duration) == True:
#             lijnvoering_NZNL.add_connection(connection_number)
#             new_traject.add_connection(connection_number)
#         # else, finish traject
#         else:
#             break
    
#     # add traject to lijnvoering, if all connections are yet included, stop lijnvoering
#     lijnvoering_NZNL.add_traject(new_traject)
#     if len(lijnvoering_NZNL.unused_connections) == 0:
#         break

# # if all connections are included, a solution is found
# if len(lijnvoering_NZNL.unused_connections) == 0:
#     solution = True
#     print('Found the following correct lijnvoering:')
# # else, search again for a solution
# else: 
#     N_try = N_try + 1
#     print('did not find a correct lijnvoering/solution at try:', N_try, ', missed:', 28-len(set(lijnvoering_NZNL.connections)))

# for i, traject in enumerate(lijnvoering_NZNL.trajecten):
# print('traject',i,':', traject.stations)
# print('duration:', traject.duration)
# print('connections', traject.connections)



def random_traject(graph):
    """
    Randomly .......
    """
    # randomly chose first part of traject from unused connections
    chosen_connection = random.choice(list(graph.unused_connections))
    [station1, station2] = chosen_connection.stations
    duration = chosen_connection.duration

    # create new traject, add connection to lijnvoering and initialize current station
    new_traject = Traject([station1, station2], int(duration), [chosen_connection])
    graph.add_connection(chosen_connection)
    cur_station = graph.stations[station2]

    traject_not_finished = True

    while traject_not_finished:
        
        # first, try to chose (randomly) new part of traject from connections not yet in lijnvoering
        unused_connections_cur_station = set(cur_station.connections.keys()).intersection(graph.unused_connections)
        if len(unused_connections_cur_station) != 0: 
            connection = random.choice(list(unused_connections_cur_station))
            duration = connection.duration
            connected_station = cur_station.connections[connection]
        else:
            connection = random.choice(list(cur_station.connections.keys()))
            duration = connection.duration
            connected_station = cur_station.connections[connection]

        # if connection with station that is not in current traject is possible 
        # and selected station is in current traject, try to find new station
        con_stations = list(cur_station.connections.values())
        if all(item in new_traject.stations for item in con_stations) == False:
            while (connected_station in new_traject.stations):
                connection = random.choice(list(cur_station.connections.keys()))
                duration = connection.duration
                connected_station = cur_station.connections[connection]
                
        # update current station, if possible to add connections within time constraint, do so and add connection 
        cur_station = graph.stations[connected_station]
        if new_traject.update_traject(connected_station, int(duration)) == True:
            graph.add_connection(connection)
            new_traject.add_connection(connection)
        else:
            traject_not_finished = False
    
    # add traject to lijnvoering 
    graph.add_traject(new_traject)
    

def random_algorithm(graph):
    """
    Algorithm that looks for combination of trajects (max. 7 trajects of < 120min)
    such that all connections are used/
    """
    print('loading randomly constructed lijnvoering...')
    print()

    solution = False
    nTry = 0 

    while solution == False:

        nTry = nTry + 1

        new_graph = copy.deepcopy(graph)
        # Randomly add new traject until all connections there
        while len(new_graph.unused_connections) != 0 and len(new_graph.lijnvoering) < 7:
            random_traject(new_graph)


        # check whether correct solution
        if len(new_graph.unused_connections) == 0:
            solution = True
            print('Found the following correct lijnvoering at try number:', nTry)
        
            for i, traject in enumerate(new_graph.lijnvoering):
                print('traject',i,':', traject.stations)
                print('duration:', traject.duration)
                print('connections', traject.connections)
    
    return new_graph



