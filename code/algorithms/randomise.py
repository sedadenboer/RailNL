from code.algorithms import helpers as help
from code.visualisation import visualise as vis

import random
import copy


class Random:
    """
    The Random class that choses a valid random new connection in each Traject
    """
    def __init__(self, graph, prefer_unused_connection, save_output, iterations = None):
        self.graph = copy.deepcopy(graph)
        self.iterations = iterations
        self.prefer_unused_connection = prefer_unused_connection
        self.Nsols = int
        self.all_K = []
        self.dict_K = dict()
        self.save_output = save_output
        self.all_opt_K = dict()
            

    def run_one_sol(self):
        """
        Algorithm that looks for combination of trajects such that all connections are used
        """
        print('\nloading randomly constructed lijnvoering...\n')

        solution = False
        nTry = 0 

        while solution == False:

            # for each try, create a new graph 
            nTry += 1
            new_graph = copy.deepcopy(self.graph)
            
            # find stations with one connection
            start_stations = help.begin_stations(self.graph)

            # if not yet max. trajects and solution not found, add new traject to lijnvoering 
            while len(new_graph.unused_connections) != 0 and help.reached_max_depth(new_graph) == False:
                help.new_traject(new_graph, start_stations, random.choice, self.prefer_unused_connection)

            # if all connections used, print solution and stop loop
            if len(new_graph.unused_connections) == 0:
                solution = True

                # add quality-goalfunction
                new_graph.lijnvoering_kwaliteit(new_graph.used_connections, \
                                                new_graph.available_connections, \
                                                new_graph.lijnvoering.trajecten)
                
                print('Found the following correct lijnvoering at try number:', nTry)
                for i, traject in enumerate(new_graph.lijnvoering.trajecten):
                    print('traject', i + 1,':', traject.stations)
                    print('duration:', traject.duration)
                    print('connections', traject.connections)
        
        # add graph of solution to Random object
        self.graph = new_graph

        # save output
        if self.save_output == True:
            
            # write result out to csv
            help.write_output_to_csv(new_graph, 'Random/One_Solution')

            # create visualisation of result
            vis.visualise_solution_new(new_graph, 'Random/One_Solution')


    def run_opt_sol(self):
        """
        Algorithm that looks for combination of trajects such that quality goal-fucntion is optimized
        """
        print('\nloading randomly constructed lijnvoering...\n')

        opt_K = 0
        opt_map = self.graph
        nSolutions = 0

        all_K = []
        dict_K = dict()
        all_opt_K = dict()

        # find stations with one connection
        start_stations = help.begin_stations(self.graph)

        while nSolutions < self.iterations:

            # for each try, create a new graph 
            new_graph = copy.deepcopy(self.graph)
            
            # if not yet all stations and max. number of trajects reached, add new traject to lijnvoering 
            while help.reached_max_depth(new_graph) == False and help.visited_all_stations(new_graph) == False:
                help.new_traject(new_graph, start_stations, random.choice, self.prefer_unused_connection)

            # only valid solution if all stations are visited
            if help.visited_all_stations(new_graph):
                nSolutions += 1
            
                # add quality-goalfunction
                new_graph.lijnvoering_kwaliteit(new_graph.used_connections, \
                                                new_graph.available_connections, \
                                                new_graph.lijnvoering.trajecten)
                
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

                # add the current optimal K to a dictionary with the solution number as key
                all_opt_K[nSolutions] = opt_K
                
         # add optimal graph and K to Random object
        self.graph = opt_map
        self.Nsols = nSolutions
        self.all_K = all_K
        self.dict_K = dict_K
        self.all_opt_K = all_opt_K

        # save output
        if self.save_output == True:

            # write result out to csv
            help.write_output_to_csv(opt_map, 'Random/Opt_Solution')

            # create visualisation of result
            vis.visualise_solution(opt_map, 'Random/Opt_Solution')

        # create visualisation of optimal K improvement
        vis.visualise_opt_K_improvement(all_opt_K, 'Random')






# def random_traject(graph):
#     """
#     Create new traject based on the following algorithm:
#     - 1st connection of traject is chosen from unused connections @ lijnvoering 
#     - at each junction, new connection is chosen from unused connections @ lijnvoering 
#       if not possible, non-unique connection is chosen
#     - at each junction, new connection is chosen with station that is not yet @ traject
#       if not possible, connection with non-unique station is chosen
#     """
#     # create new traject with first connection selected from unused connections @ lijnvoering
#     chosen_connection = random.choice(list(graph.unused_connections))
#     [station1, station2] = chosen_connection.stations
#     duration = chosen_connection.duration
#     new_traject = Traject([station1, station2], int(float(duration)), [chosen_connection])
#     graph.add_connection(chosen_connection)
#     cur_station = graph.stations[station2]

#     # add new connections to traject as long as time constraint permits
#     traject_not_finished = True
#     while traject_not_finished:
        
#         # chose new part of traject from connections not yet @ lijnvoering
#         unused_connections_cur_station = set(cur_station.connections.keys()).intersection(graph.unused_connections)
#         if len(unused_connections_cur_station) != 0: 
#             connection = random.choice(list(unused_connections_cur_station))
#             duration = connection.duration
#             connected_station = cur_station.connections[connection]
#         # if not possible, chose non-unique connection
#         else:
#             connection = random.choice(list(cur_station.connections.keys()))
#             duration = connection.duration
#             connected_station = cur_station.connections[connection]

#         permitted_connection = True
#         ########################### ONLY 1x STATION @ TRAJECT #########################
#         con_stations = list(cur_station.connections.values())
#         # if selected station is in current traject, select new station if possible
#         if all(item in new_traject.stations for item in con_stations) == False:
#             while (connected_station in new_traject.stations):
#                 connection = random.choice(list(cur_station.connections.keys()))
#                 duration = connection.duration
#                 connected_station = cur_station.connections[connection]
#         # if not possible, end traject as 2x the same station in 1 traject is not possible
#         else: 
#             traject_not_finished = False
#             permitted_connection = False
                
#         # add connections to traject if within time constraint
#         if permitted_connection == True:
#             cur_station = graph.stations[connected_station]
#             if new_traject.update_traject(connected_station, int(float(duration)), connection, graph.max_duration) == True:
#                 graph.add_connection(connection)
#             else:
#                 traject_not_finished = False
    
#     # if finished, add traject to lijnvoering 
#     graph.lijnvoering.add_traject(new_traject)


    # def run_unique(self):
    #     """
    #     Algorithm that checks for number of unique Lijnvoeringen in state space
    #     """
    #     print('\nchecking for unique solutions...\n')

    #     nTry = 0 
    #     nSolutions = 0
    #     nUnique = 0
    #     nonUnique = 0
    #     same_k = 0
    #     yes = 0

    #     lijnvoeringen_by_K = dict()
    #     K_counter = dict()

    #     while nTry < 2000000:

    #         # for each try, create a new graph 
    #         nTry += 1
    #         new_graph = copy.deepcopy(self.graph)
            
    #         # if not yet max. trajects and not yet all stations visited, add new traject to lijnvoering
    #         while len(new_graph.visited_stations) != len(new_graph.stations) and len(new_graph.lijnvoering.trajecten) < new_graph.max_trajects:
    #             help.new_traject(new_graph, random.choice)
            
    #         # if all stations are visited, solution is found
    #         if len(new_graph.visited_stations) == len(new_graph.stations):
    #             nSolutions += 1
                
    #             # add K
    #             new_graph.lijnvoering_kwaliteit(new_graph.used_connections, new_graph.available_connections, new_graph.lijnvoering.trajecten)

    #             # if found non-unique K
    #             if new_graph.K in lijnvoeringen_by_K.keys():
    #                 same_k += 1
    #                 # check for duplicate, if there is only one lijnvoeringen with same K
    #                 if type(lijnvoeringen_by_K[new_graph.K]) != list:
    #                     yes += 1
    #                     # if new lijnvoering turns out to be unique, create list of 2 solutions
    #                     if lijnvoeringen_by_K[new_graph.K] != new_graph.lijnvoering:
    #                         lijnvoeringen_by_K[new_graph.K] = [lijnvoeringen_by_K[new_graph.K], new_graph.lijnvoering]
    #                         K_counter[new_graph.K] += 1
    #                         nUnique += 1
    #                     else:
    #                         nonUnique += 1
    #                 # check for duplicate, if there are more unique lijnvoeringen with same K
    #                 else:
    #                     Unique = True
    #                     for lijnvoering in lijnvoeringen_by_K[new_graph.K]:
    #                         if lijnvoering == new_graph.lijnvoering:
    #                             nonUnique += 1
    #                             Unique = False
    #                             break
    #                     # if new lijnvoering turns out to be unique
    #                     if Unique == True:
    #                         lijnvoeringen_by_K[new_graph.K] = lijnvoeringen_by_K[new_graph.K] + [new_graph.lijnvoering]
    #                         K_counter[new_graph.K] += 1
    #                         nUnique += 1
    #             # if found unique K
    #             else:
    #                 nUnique += 1
    #                 lijnvoeringen_by_K[new_graph.K] = new_graph.lijnvoering
    #                 K_counter[new_graph.K] = 1
            
    #         print(f"n: {nTry}")
    #         print(f"Solutions: {nSolutions}")
    #         print(f"nUnique: {nUnique}")
    #         print(f"nNon-unique: {nonUnique}")
    #         print(f"list works: {yes}")
    #         print(f"lijnvoeringen with same_k: {same_k}\n")

    #     return new_graph