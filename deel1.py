
# GOAL: lijnvoering intercity treinen, zet aantal trajecten uit o.b.v. tijdsframe
#       lijnvoering = trajecten waarover de treinen gedurende de dag heen en weer rijden
#       traject     = route van sporen en stations waarover treinen heen en weer rijden, mag niet langer zijn dan tijdsframe
#           ex. traject = [Castricum , Zaandam , Hoorn , Alkmaar] is 59min, past binnen tijdsframe 60min

############################################ DEEL 1 (noord/zuid-holland) ############################################ 

# 1. Maak een lijnvoering voor Noord- en Zuid-Holland met maximaal zeven trajecten binnen een tijdsframe van twee uur, 
#    waarbij alle verbindingen bereden worden.

#    Kwaliteitsfunctie:    K = p*10000 - (T*100 + Min)
#    p   = fractie van de bereden verbindingen (dus tussen 0 en 1)
#    T   = aantal trajecten
#    Min = aantal minuten in alle trajecten samen

# 2. Maak wederom een lijnvoering voor Noord- en Zuid-Holland met maximaal zeven trajecten binnen een tijdsframe van twee uur, 
#    en probeer nu K zo hoog mogelijk te krijgen.





# def main():


   
    

#     ############################## 4. Exercise 1.1 ################################
    
#     N_try = 0
#     solution = False
#     while solution == False: 
        
#         # create empty lijnvoering
#         lijnvoering_NZNL = Lijnvoering([], [])

#         while len(lijnvoering_NZNL.trajecten) < 7:
            
#             # randomly chose first part of traject from unused connections
#             chosen_connection = random.choice(list(lijnvoering_NZNL.unused_connections))
           
#             # retrieve stations and duration of this connection
#             station_1 = df_connections['station1'][chosen_connection]
#             station_2 = df_connections['station2'][chosen_connection]
#             duration = df_connections['distance'][chosen_connection]
            
#             # create new traject, add connection to lijnvoering and initialize current station
#             new_traject = Traject([station_1, station_2], duration, [chosen_connection])
#             lijnvoering_NZNL.add_connection(chosen_connection)
#             cur_station = stations[station_2]

#             # as long as traject is not finished
#             while True:
#                 # print("current trajectory:", new_traject.stations)
#                 # print("current duration of trajectory (min):", new_traject.duration)
#                 # print("bereden verbindingen (lijnvoering):", set(lijnvoering_NL.verbindingen))

#                 # first, try to chose (randomly) new part of traject from connections not yet in lijnvoering
#                 unused_connections_cur_station = set(cur_station.connections.keys()).intersection(lijnvoering_NZNL.unused_connections)
#                 if len(unused_connections_cur_station) != 0: 
#                     connection_number = random.choice(list(unused_connections_cur_station))
#                     connected_station, duration = cur_station.connections[connection_number]
#                 # else, chose from connections already in lijnvoering
#                 else:
#                     connection_number = random.choice(list(cur_station.connections.keys()))
#                     connected_station, duration = cur_station.connections[connection_number]

#                 # if connection with station that is not in current traject is possible & selected station is in current traject, try to find new station
#                 con_stations = [s[0] for s in list(cur_station.connections.values())]
#                 if all(item in new_traject.stations for item in con_stations) == False:
#                     while (connected_station in new_traject.stations):
#                         connection_number = random.choice(list(cur_station.connections.keys()))
#                         connected_station, duration = cur_station.connections[connection_number]

#                 # update current station, if possible to add connections within time constraint, do so and add connection 
#                 cur_station = stations[connected_station]
#                 if new_traject.update_traject(connected_station, duration) == True:
#                     lijnvoering_NZNL.add_connection(connection_number)
#                     new_traject.add_connection(connection_number)
#                 # else, finish traject
#                 else:
#                     break
            
#             # add traject to lijnvoering, if all connections are yet included, stop lijnvoering
#             lijnvoering_NZNL.add_traject(new_traject)
#             if len(lijnvoering_NZNL.unused_connections) == 0:
#                 break
        
#         # if all connections are included, a solution is found
#         if len(lijnvoering_NZNL.unused_connections) == 0:
#             solution = True
#             print('Found the following correct lijnvoering:')
#         # else, search again for a solution
#         else: 
#             N_try = N_try + 1
#             print('did not find a correct lijnvoering/solution at try:', N_try, ', missed:', 28-len(set(lijnvoering_NZNL.connections)))

#     for i, traject in enumerate(lijnvoering_NZNL.trajecten):
#         print('traject',i,':', traject.stations)
#         print('duration:', traject.duration)
#         print('connections', traject.connections)
    
#     ############################## 4. Exercise 1.1 (all options) ################################
    
#     # correct solutions
#     N_solutions = 0 
#     N_unique_solutions = 0
#     solutions = dict()

#     N = 0 
#     while N < 100000: 
#         print(N)

#         # create empty lijnvoering
#         lijnvoering_NZNL = Lijnvoering([], [])

#         while len(lijnvoering_NZNL.trajecten) < 7:
            
#             # randomly chose first part of traject from unused connections
#             chosen_connection = random.choice(list(lijnvoering_NZNL.unused_connections))
           
#             # retrieve stations and duration of this connection
#             station_1 = df_connections['station1'][chosen_connection]
#             station_2 = df_connections['station2'][chosen_connection]
#             duration = df_connections['distance'][chosen_connection]
            
#             # create new traject, add connection to lijnvoering and initialize current station
#             new_traject = Traject([station_1, station_2], duration, [chosen_connection])
#             lijnvoering_NZNL.add_connection(chosen_connection)
#             cur_station = stations[station_2]

#             # as long as traject is not finished
#             while True:
#                 # print("current trajectory:", new_traject.stations)
#                 # print("current duration of trajectory (min):", new_traject.duration)
#                 # print("bereden verbindingen (lijnvoering):", set(lijnvoering_NL.verbindingen))

#                 # first, try to chose (randomly) new part of traject from connections not yet in lijnvoering
#                 unused_connections_cur_station = set(cur_station.connections.keys()).intersection(lijnvoering_NZNL.unused_connections)
#                 if len(unused_connections_cur_station) != 0: 
#                     connection_number = random.choice(list(unused_connections_cur_station))
#                     connected_station, duration = cur_station.connections[connection_number]
#                 # else, chose from connections already in lijnvoering
#                 else:
#                     connection_number = random.choice(list(cur_station.connections.keys()))
#                     connected_station, duration = cur_station.connections[connection_number]

#                 # if connection with station that is not in current traject is possible & selected station is in current traject, try to find new station
#                 con_stations = [s[0] for s in list(cur_station.connections.values())]
#                 if all(item in new_traject.stations for item in con_stations) == False:
#                     while (connected_station in new_traject.stations):
#                         connection_number = random.choice(list(cur_station.connections.keys()))
#                         connected_station, duration = cur_station.connections[connection_number]

#                 # update current station, if possible to add connections within time constraint, do so and add connection 
#                 cur_station = stations[connected_station]
#                 if new_traject.update_traject(connected_station, duration) == True:
#                     lijnvoering_NZNL.add_connection(connection_number)
#                     new_traject.add_connection(connection_number)
#                 # else, finish traject
#                 else:
#                     break
            
#             # add traject to lijnvoering, if all connections are yet included, stop lijnvoering
#             lijnvoering_NZNL.add_traject(new_traject)
#             if len(lijnvoering_NZNL.unused_connections) == 0:
#                 break
        
#         N = N + 1 

#         # if all connections are included, a solution is found
#         if len(lijnvoering_NZNL.unused_connections) == 0:
#             N_solutions = N_solutions + 1
#             new_solution = list()
#             for traject in lijnvoering_NZNL.trajecten:
#                 new_solution.append(traject.connections)

#             not_unique = False
#             for i in list(solutions.values()):
#                 if all(item in new_solution for item in i) and all(item in i for item in new_solution):
#                     not_unique = True
            
#             if not_unique == False:
#                 N_unique_solutions = N_unique_solutions + 1 
#                 solutions['solution' + str(N_unique_solutions)] = new_solution

#     print("Number of tries:", N)
#     print("number solutions:", N_solutions)
#     print("number unique solutions:", N_unique_solutions)




# if __name__ == "__main__":
#     main()

