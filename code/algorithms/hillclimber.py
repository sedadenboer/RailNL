from code.classes.traject import Traject
from code.algorithms import helpers as help
from code.algorithms.greedy import Greedy
from decimal import Decimal
from code.algorithms.randomise import Random
from code.visualisation import visualise as vis

import random
import copy
import sys


class Hillclimber:
    """
    Hillclimber class that ..... (deletes Traject in Lijnvoering with lowest K)
    """

    def __init__(self, graph, prefer_unused_connection, save_output, alg_choice, remove_traject, iterations, start_iterations, sim_anneal, lin_or_exp):
        self.graph = copy.deepcopy(graph)
        self.iterations = iterations
        self.prefer_unused_connection = prefer_unused_connection
        self.remove_traject = remove_traject
        self.save_output = save_output
        self.alg_choice = alg_choice
        self.start_iterations = start_iterations
        self.all_K = []
        self.all_opt_K = dict()
        if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
            self.sim_anneal = True
            self.formula = lin_or_exp
        else:
            self.sim_anneal = False

    def random_start_state(self):
        """
        Generates random start solution for hillclimber by random algorithm.
        """
        random_alg = Random(self.graph, self.prefer_unused_connection, False, self.start_iterations)
        random_alg.run_opt_sol()

        new_graph = random_alg.graph
            
        return new_graph
    
    def greedy_start_state(self):
        """
        Generates greedy start solution for hillclimber by greedy algorithm.
        """
        greedy_alg = Greedy(self.graph, self.prefer_unused_connection, False, self.start_iterations)
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

        # update quality-goalfunction of Lijnvoering
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)

        return graph

    def remove_traject_lowest_K(self, graph):
        """
        Remove traject with lowest K from Lijnvoering
        """
        
        # start with first traject as worse traject
        bad_traject = graph.lijnvoering.trajecten[0]
        lowest_K = self.partial_K(bad_traject)

        # find traject with lowest K
        for traject in graph.lijnvoering.trajecten:

            # replace badest traject if partial_K lower 
            if self.partial_K(traject) < lowest_K:
                lowest_K = self.partial_K(traject)
                bad_traject = traject
        
        # remove traject from lijnvoering
        print(f"remove: {bad_traject.stations}")
        graph.lijnvoering.trajecten.remove(bad_traject)
        graph.update_variables()

        # update quality-goalfunction of Lijnvoering
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)

        return graph

    def add_new_traject(self, graph):
        """
        Add new traject to Lijnvoering till solution is valid
        """

        # create new solutions till valid one is found
        valid_solution = False
        while valid_solution == False: 

            # find stations with one connection
            start_stations = help.begin_stations(graph)

            # add new traject to Lijnvoering
            help.new_traject(graph, start_stations, random.choice, self.prefer_unused_connection)
            print(f"add: {graph.lijnvoering.trajecten[-1].stations}")

            # check whether valid Lijnvoering, if not remove newly added Traject
            if help.visited_all_stations(graph) or self.sim_anneal:
                valid_solution = True
            else:
                graph.lijnvoering.trajecten.pop()
                graph.update_variables()
        
        # add quality-goalfunction to Lijnvoering
        graph.lijnvoering_kwaliteit(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lijnvoering.trajecten)
        
        return graph

    def simulated_annealing(self, i, new_graph, old_graph):
        
        # Set temperature by chosen formula
        if self.formula.upper() == "L":
            temperature = self.iterations / 2 - 0.5 * i
        elif self.formula.upper() == "E":
            temperature = self.iterations / 2 * (0.995 ** i)
        else: 
            sys.exit("Algorithm not (yet) implemented")

        # Determine if new solution needs to be accepted
        if float(temperature) != 0.0:
            acceptation_probability = 2 ** (float(new_graph.K - old_graph.K) / float(temperature))
        else: 
            acceptation_probability = 0
        random_probability = random.random()
        if acceptation_probability > random_probability:
            return new_graph
        else:
            return old_graph


    def run(self):
        """
        Algorithm that implements the hillclimber algorithm:
        - It start with a valid Lijnvoering generated by the random or greedy algorithm
        - It removes a Traject from this Lijnvoering
        - It creates a new valid Trajects and adds this to the Lijnvoering
        - If K_new_Lijnvoering > K_old_Lijnvoering, the new Lijnvoering is kept
        - This algorithm is repeated a particular number of times 
        """
        print('\nloading hillclimber constructed lijnvoering...\n')
        
        # generate valid start state
        if self.alg_choice.upper() == "R" or self.alg_choice.upper() == "RANDOM":
            current_state = self.random_start_state()
        elif self.alg_choice.upper() == "G" or self.alg_choice.upper() == "GREEDY":
            current_state = self.greedy_start_state()

        # save all k and optimal K
        all_K = []
        all_opt_K = dict() 
    	
        # for i iterations:
        i = 0
        while i < self.iterations:
            i += 1

            # copy current state
            new_graph = copy.deepcopy(current_state)

            print("\n unused connections current solution")
            print(new_graph.unused_connections)
            print(len(new_graph.unused_connections))

            # optional print statement
            print("\nCurrent:")
            for traject in new_graph.lijnvoering.trajecten:
                print("Traject", new_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
            print()
            print(f"current optimal K: {new_graph.K}")

            # remove traject from Lijnvoering
            if self.remove_traject.upper() == "K":
                new_graph = self.remove_traject_lowest_K(new_graph)
            elif self.remove_traject.upper() == "R":
                new_graph = self.remove_traject_random(new_graph)

            print("\n update unused connections after deleting traject")
            print(new_graph.unused_connections)
            print(len(new_graph.unused_connections))

            # optional print statement
            print("\nRemoved:")
            for traject in new_graph.lijnvoering.trajecten:
                print("Traject", new_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
            print()
            print(f"K when traject removed: {new_graph.K}")

            # add new traject till valid Lijnvoering is created
            new_graph = self.add_new_traject(new_graph)

            print("\n update unused connections after adding traject")
            print(new_graph.unused_connections)
            print(len(new_graph.unused_connections))

             # optional print statement
            print("\nNew:")
            for traject in new_graph.lijnvoering.trajecten:
                print("Traject", new_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
            print()
            print(f"newly added K: {new_graph.K}")

            # Update current state, optionally by simulated annealing
            if self.sim_anneal:
                current_state = self.simulated_annealing(i, new_graph, current_state)
            else:
                if new_graph.K > current_state.K:
                    print("current stated is changed")
                    current_state = new_graph
                else:
                    print("current stated is not changed")
            
            # steekproef variables
            all_K.append(new_graph.K)

            # add the current optimal K to a dictionary with the solution number as key
            all_opt_K[i] = current_state.K

        # Add optimal graph to Hillclimber object
        self.graph = current_state
        self.all_K = all_K
        self.all_opt_K = all_opt_K

        # save results
        if self.save_output == True:

            # write result out to csv
            help.write_output_to_csv(self.graph, 'Hillclimber')
            
            # create compact visualisation of result
            vis.visualise_solution_compact(self.graph, 'Hillclimber')

            # create visualisation of optimal K improvement
            vis.visualise_opt_K_improvement(all_opt_K, 'Hillclimber', self.alg_choice, self.start_iterations, self.remove_traject)
