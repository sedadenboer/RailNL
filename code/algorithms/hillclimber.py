from code.classes.traject import Traject
from code.algorithms import helpers as help
from code.algorithms.greedy import Greedy
from code.visualisation import visualise as vis

import random
import copy


class Hillclimber:
    """
    Hillclimber class that ..... (deletes Traject in Lijnvoering with lowest K)
    """
    def __init__(self, graph, iterations, alg_choice, remove_traject, greedy_iterations):
        self.graph = copy.deepcopy(graph)
        self.iterations = iterations
        self.remove_traject = remove_traject
        self.alg_choice = alg_choice
        self.greedy_iterations = greedy_iterations
    
    def random_start_state(self):
        """
        Generates random start solution for hillclimber by random algorithm.
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
    
    def greedy_start_state(self, graph, iterations):
        """
        Generates greedy start solution for hillclimber by greedy algorithm.
        """
        greedy_alg = Greedy(graph, iterations)
        greedy_alg.run()

        new_graph = greedy_alg.graph
        
        return new_graph

    def partial_K(self, traject):
        """
        Calculate the quality of the Traject, set T = 1
        """
        # fraction of ridden connections
        p = len(traject.connections) / len(self.graph.available_connections)

        # calculate K
        K = p * 10000 - traject.duration

        return K

    def remove_traject_random(self, graph):
        """
        Remove random traject from Lijnvoering
        """
        
        # randomly chose traject to remove from Lijnvoering
        traject_to_remove = random.choice(graph.lijnvoering.trajecten)

        # remove traject and update variables
        print(f"remove: {traject_to_remove.stations}")
        graph.lijnvoering.trajecten.remove(traject_to_remove)
        graph.update_variables()

        # update quality-goalfunction
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)

        return graph

    def remove_traject_lowest_K(self, graph):
        """
        Remove traject with lowest K from Lijnvoering
        """
        
        bad_traject = graph.lijnvoering.trajecten[0]
        lowest_K = self.partial_K(bad_traject)

        # find traject with lowest K
        for traject in graph.lijnvoering.trajecten:

            partial_K = self.partial_K(traject)

            # replace badest traject if partial_K lowest
            if partial_K < lowest_K:
                lowest_K = partial_K
                bad_traject = traject
        
        # remove traject from lijnvoering
        print(f"remove: {bad_traject.stations}")
        graph.lijnvoering.trajecten.remove(bad_traject)
        graph.update_variables()
        # update quality-goalfunction
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)

        return graph

    def add_new_traject(self, graph):
        """
        Add new traject to Lijnvoering till solution is valid
        """

        n = 0 
        while True: 

            # if previous solution was invalid, remove from Lijnvoering
            if n > 0:
                graph.lijnvoering.trajecten.pop()
                graph.update_variables()
            n += 1

            # find stations with one connection
            start_stations = help.begin_stations(graph)

            # add new traject to Lijnvoering
            help.new_traject(graph, start_stations, random.choice)
            print(f"add: {graph.lijnvoering.trajecten[-1].stations}")

            if help.visited_all_stations(graph):
                break
        
        # add quality-goalfunction
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)
        
        return graph


    def run(self):
        """
        Algorithm that implements the hillclimber algorithm:
        - It start with a valid Lijnvoering generated by the random algorithm
        - It removes a Traject from this Lijnvoering
        - It creates a new valid Trajects and adds this to the Lijnvoering
        - If K_new_Lijnvoering > K_old_Lijnvoering, the new Lijnvoering is kept
        - This algorithm is repeated a particular number of times 
        """
        print('\nloading hillclimber constructed lijnvoering...\n')
        
        # set random start state as default
        current_state = self.random_start_state()

        # retrieve random valid start state 
        if self.alg_choice == "R" or self.alg_choice == "RANDOM":
            current_state = self.random_start_state()
        # retrieve greedy start state
        elif self.alg_choice == "G" or self.alg_choice == "GREEDY":
            current_state =  self.greedy_start_state(self.graph, self.greedy_iterations)    
    	
        # for x iterations:
        i = 0
        while i < self.iterations:
            i += 1

            # copy current state
            new_graph = copy.deepcopy(current_state)

            # optional print statement
            print()
            for traject in new_graph.lijnvoering.trajecten:
                print("Traject", new_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
            print()
            print(f"current optimal K: {new_graph.K}")

            # remove traject with lowest K from Lijnvoering
            if self.remove_traject.upper() == "K":
                new_graph = self.remove_traject_lowest_K(new_graph)
            else:
                new_graph = self.remove_traject_random(new_graph)

            # optional print statement
            print()
            for traject in new_graph.lijnvoering.trajecten:
                print("Traject", new_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
            print()
            print(f"K when traject removed: {new_graph.K}")

            # add new traject till valid solution is found
            new_graph = self.add_new_traject(new_graph)
            print(f"newly added K: {new_graph.K}")

            # if K has increased, update current state
            if new_graph.K > current_state.K:
                print("current stated is changed")
                current_state = new_graph
            else:
                print("current stated is not changed")

        # Add optimal graph to Hillclimber object
        self.graph = current_state

        # write result out to csv
        help.write_output_to_csv(self.graph, 'Hillclimber')

        # create visualisation of result
        vis.visualise_solution(self.graph, 'Hillclimber')