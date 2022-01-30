from code.algorithms import helpers as help
from code.visualisation import visualise as vis

import copy


class Greedy:
    """
    The Greedy class that choses a valid new connection at junction in a Traject by:
        - lowest duration
        - unused connection get priority over used connection
    """
    def __init__(self, graph, prefer_unused_connection, save_output, iterations):
        self.graph = copy.deepcopy(graph)
        self.prefer_unused_connection = prefer_unused_connection
        self.iterations = iterations
        self.Nsols = int
        self.save_output = save_output
        self.all_K = []
        self.dict_K = dict()
        self.all_opt_K = dict()

    def greedy_choice(self, options):
        """
        Greedy choses next connection at junction by lowest duration
        """
        # create dictionary of all durations
        duration_dict = dict()
        for connection in options:
            duration_dict[connection] = int(connection.duration)
        
        # select option with minimum duration
        optimal_connection = min(duration_dict, key=duration_dict.get)

        return optimal_connection

    def run(self):
        """
        Algorithm that looks for combination of trajects such that short-term optimum is reached
        """
        print('\nloading greedy constructed lijnvoering...\n')

        opt_K = 0
        opt_map = self.graph
        nSolutions = 0
        all_K = []
        all_opt_K = dict()

        # find stations with one connection
        start_stations = help.begin_stations(self.graph)

        while nSolutions < self.iterations:

            # for each try, create a new graph 
            new_graph = copy.deepcopy(self.graph)
            
            # if not yet all stations and max. number of trajects reached, add new traject to lijnvoering 
            while help.reached_max_depth(new_graph) == False and help.visited_all_stations(new_graph) == False:
                help.new_traject(new_graph, start_stations, self.greedy_choice, self.prefer_unused_connection)

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

                # add the current optimal K to a dictionary with the solution number as key
                all_opt_K[nSolutions] = opt_K

        # add optimal graph and K to greedy object
        self.graph = opt_map
        self.Nsols = nSolutions
        self.all_K = all_K
        self.all_opt_K = all_opt_K

        # save results
        if self.save_output == True:
            
            # write result out to csv
            help.write_output_to_csv(opt_map, 'Greedy')

            # create visualisation of result
            vis.visualise_solution_compact(opt_map, 'Greedy')

            vis.visualise_solution(opt_map, 'Greedy')

        # create visualisation of optimal K improvement
        vis.visualise_opt_K_improvement(all_opt_K, 'Greedy')

