from code.algorithms import helpers as help
from code.visualisation import visualise as vis

import copy
import time


class Greedy:
    """
    The Greedy class that choses a valid new connection at junction in a Traject by:
        - lowest duration
        - unused connection get priority over used connection
    """
    def __init__(self, graph, prefer_unused_connection, save_output, runtime = None):
        self.graph = copy.deepcopy(graph)
        self.prefer_unused_connection = prefer_unused_connection
        self.runtime = runtime 
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
            duration_dict[connection] = int(float(connection.duration))
        
        # select option with minimum duration
        optimal_connection = min(duration_dict, key=duration_dict.get)

        return optimal_connection

    def run(self):
        """
        Algorithm that looks for combination of trajects such that short-term optimum is reached
        """
        print('\nloading greedy constructed lijnvoering...\n')

        # store variables
        opt_K = 0
        opt_map = self.graph
        all_K = []
        all_opt_K = dict()

        # start parameters
        start = time.time()
        n_runs = 0
        n_sols = 0

        # find stations with one connection
        start_stations = help.begin_stations(self.graph)

        while time.time() - start < self.runtime:
            n_runs += 1
            print(f"run: {n_runs}")

            # for each try, create a new graph 
            new_graph = copy.deepcopy(self.graph)
            
            # if not yet all stations and max. number of trajects reached, add new traject to lijnvoering 
            while help.reached_max_depth(new_graph) == False and help.visited_all_stations(new_graph) == False:
                help.new_traject(new_graph, start_stations, self.greedy_choice, self.prefer_unused_connection)

            # only valid solution if all stations are visited
            if help.visited_all_stations(new_graph):
                n_sols += 1
                print(f"solutions: {n_sols}")
            
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
                all_opt_K[n_sols] = opt_K

        # add optimal graph and K to greedy object
        self.graph = opt_map
        self.Nsols = n_sols
        self.all_K = all_K
        self.all_opt_K = all_opt_K

        # save results
        if self.save_output == True:

            # file name
            extension = ''
            if self.prefer_unused_connection:
                extension += '_prefer_unused'
            
            # write result out to csv
            help.write_output_to_csv(opt_map, 'Greedy', extension)

            # create visualisation of result
            vis.visualise_solution_compact(opt_map, 'Greedy', extension)

            # create visualisation of optimal K improvement
            vis.visualise_opt_K_improvement(all_opt_K, 'Greedy', extension)

            # write out to csv all K (for distribution) all opt K (for iterations)
            help.write_to_csv(self.graph, all_K, all_opt_K, 'Greedy', extension)

