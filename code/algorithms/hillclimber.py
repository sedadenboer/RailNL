from code.classes.traject import Traject
from code.algorithms import helpers as help
from code.visualisation import visualise as vis

import random
import copy


class Hillclimber:
    """
    Hillclimber class that ..... (deletes Traject in Lijnvoering with lowest K)
    """
    def __init__(self, graph, iterations):
        self.graph = copy.deepcopy(graph)
        self.iterations = iterations
    
    def random_start_state(self):
        """
        Generates random start solution for hillclimber by random algorithm
        """
        # find stations with one connection
        start_stations = help.begin_stations(self.graph)

        while True:

            # for each try, create a new graph 
            new_graph = copy.deepcopy(self.graph)
            
            # if not yet all stations and max. number of trajects reached, add new traject to lijnvoering 
            while help.reached_max_depth(new_graph) == False and help.visited_all_stations(new_graph) == False:
                help.new_traject(new_graph, start_stations, random.choice)

            # only valid solution if all stations are visited
            if help.visited_all_stations(new_graph):
                new_graph.lijnvoering_kwaliteit(new_graph.used_connections, \
                                            new_graph.available_connections, \
                                            new_graph.lijnvoering.trajecten)
                
                break
            
        return new_graph

    def run(self):
        """
        Algorithm that looks for ....
        """
        print('\nloading hillclimber constructed lijnvoering...\n')

        # retrieve random valid state 
        random_start_state =  self.random_start_state()
    	
        # for x iterations:
        i = 0
        while i < self.iterations:
            i += 1

            # copy current state
            new_graph = random_start_state

        #     #TODO: muteer de kopie
        #     #TODO: als de staat is verbeterd (K is hoger):
        #         # TODO: vervang de oude staat door de nieuwe
        
        # Add optimal graph to Hillclimber object
        self.graph = new_graph

        # write result out to csv
        help.write_output_to_csv(new_graph, 'Hillclimber')

        # create visualisation of result
        vis.visualise_solution(new_graph, 'Hillclimber')