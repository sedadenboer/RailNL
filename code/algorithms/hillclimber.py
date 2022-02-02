# hillclimber.py
#
# Minor Programmeren
# Bèta-Programma
#
# - Hillclimber class which creates hillclimber algorithm line solution.
# - Also has the option to add Simulated Annealing.
# - Creates a graph with an optimal line solution.
# - Results (plots) can be saved optionally.

from code.classes.trajectory import Trajectory
from code.algorithms import helpers as help
from code.algorithms.greedy import Greedy
from decimal import Decimal
from code.algorithms.randomise import Random
from code.visualisation import visualise as vis
import random
import copy
import sys
import time


class Hillclimber:
    """
    Hillclimber class that aims to optimize K by small mutations.
    """

    def __init__(self, graph, prefer_unused_connection, save_output, alg_choice, remove_trajectory, iterations, sim_anneal, lin_or_exp, restart):

        self.graph = copy.deepcopy(graph)
        self.prefer_unused_connection = prefer_unused_connection
        self.remove_trajectory = remove_trajectory
        self.save_output = save_output
        self.iterations = iterations
        self.alg_choice = alg_choice
        self.restart = restart
        self.all_K = []
        self.all_opt_K = dict()

        # check for simulated annealing
        if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
            self.sim_anneal = True
            self.formula = lin_or_exp
        else:
            self.sim_anneal = False

    def random_start_state(self):
        """
        Generates random start solution for hillclimber by random algorithm.
        """

        random_alg = Random(self.graph, self.prefer_unused_connection, False, 1)
        random_alg.run_opt_sol()

        new_graph = random_alg.graph
            
        return new_graph
    
    def greedy_start_state(self):
        """
        Generates greedy start solution for hillclimber by greedy algorithm.
        """

        greedy_alg = Greedy(self.graph, self.prefer_unused_connection, False, 1)
        greedy_alg.run()

        new_graph = greedy_alg.graph
        
        return new_graph

    def partial_K(self, trajectory):
        """
        Calculate the quality of the Traject, set T = 1
        """

        # fraction of ridden connections
        p = len(trajectory.connections) / len(self.graph.available_connections)

        # calculate K
        K = p * 10000 - trajectory.duration

        return K

    def remove_trajectory_random(self, graph):
        """
        Remove random trajectory from Lines
        """
        
        # randomly chose trajectory to remove from Lines
        trajectory_to_remove = random.choice(graph.lines.trajectories)

        # remove trajectory and update variables
        graph.lines.trajectories.remove(trajectory_to_remove)
        graph.update_variables()

        # update quality-goalfunction of Lines
        graph.lines_quality(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lines.trajectories)

        return graph

    def remove_trajectory_lowest_K(self, graph):
        """
        Remove trajectory with lowest K from Lines
        """
        
        # start with first trajectory as worse trajectory
        bad_trajectory = graph.lines.trajectories[0]
        lowest_K = self.partial_K(bad_trajectory)

        # find trajectory with lowest K
        for trajectory in graph.lines.trajectories:

            # replace badest trajectory if partial_K lower 
            if self.partial_K(trajectory) < lowest_K:
                lowest_K = self.partial_K(trajectory)
                bad_trajectory = trajectory
        
        # remove trajectory from lines
        graph.lines.trajectories.remove(bad_trajectory)
        graph.update_variables()

        # update quality-goalfunction of Lines
        graph.lines_quality(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lines.trajectoryories)

        return graph

    def add_new_trajectory(self, graph):
        """
        Add new trajectory to Lines till solution is valid
        """

        # create new solutions till valid one is found
        valid_solution = False
        while valid_solution == False: 

            # find stations with one connection
            start_stations = help.begin_stations(graph)

            # add new trajectory to Lines
            help.new_trajectory(graph, start_stations, random.choice, self.prefer_unused_connection)

            # check whether valid Lines, if not remove newly added Traject
            if help.visited_all_stations(graph) or self.sim_anneal:
                valid_solution = True
            else:
                graph.lines.trajectories.pop()
                graph.update_variables()
        
        # add quality-goalfunction to Lines
        graph.lines_quality(graph.used_connections, \
                                        graph.available_connections, \
                                        graph.lines.trajectories)
        
        return graph

    def simulated_annealing(self, i, new_graph, old_graph):
        """
        Applies simulated annealing to hillclimber algorithm.
        Does this by looking at the acceptation probability, and 
        calculates this with the help of a linear or exponetial function.
        """

        # set temperature by chosen formula
        if self.formula.upper() == "L":
            temperature = self.iterations / 2 - 0.5 * i
        elif self.formula.upper() == "E":
            temperature = self.iterations / 2 * (0.995 ** i)
        else: 
            sys.exit("Algorithm not (yet) implemented")

        # calculate acceptation probability
        if float(temperature) > 0.0001:
            acceptation_probability = Decimal(2 ** (Decimal(new_graph.K - old_graph.K) / Decimal(temperature)))
        else: 
            acceptation_probability = 0
        random_probability = random.random()

        # determine if new solution needs to be accepted
        if acceptation_probability > random_probability:
            return new_graph
        else:
            return old_graph

    def run(self):
        """
        Algorithm that implements the hillclimber algorithm:
        - It start with a valid Lines generated by the random or greedy algorithm
        - It removes a Traject from this Lines
        - It creates a new valid Trajectories and adds this to the Lines
        - If K_new_Lijnvoering > K_old_Lijnvoering, the new Lines is kept
        - This algorithm is repeated a particular number of times 
        """

        print('\nloading hillclimber constructed lines...\n')

        # store variables
        all_K = []
        all_opt_K = dict() 
        all_restart_K = dict()

        # generate valid start state
        if self.alg_choice.upper() == "R" or self.alg_choice.upper() == "RANDOM":
            current_state = self.random_start_state()
        elif self.alg_choice.upper() == "G" or self.alg_choice.upper() == "GREEDY":
            current_state = self.greedy_start_state()
    	
        # start parameters
        start = time.time()
        n_runs = 0
        n_sols = 0
        n_repeat = 0

        while n_runs < self.iterations:
            n_runs += 1
            print(f"run: {n_runs}")

            # copy current state
            new_graph = copy.deepcopy(current_state)

            # remove trajectory from Lines
            if self.remove_trajectory.upper() == "K":
                new_graph = self.remove_trajectory_lowest_K(new_graph)
            elif self.remove_trajectory.upper() == "R":
                new_graph = self.remove_trajectory_random(new_graph)

            # add new trajectory till valid Lines is created
            new_graph = self.add_new_trajectory(new_graph)
            
            # Update current state, optionally by simulated annealing
            if self.sim_anneal:
                current_state = self.simulated_annealing(n_runs, new_graph, current_state)
            elif new_graph.K > current_state.K:
                current_state = new_graph
            
            # save K values
            all_K.append(new_graph.K)
            all_opt_K[n_runs] = current_state.K
            
            # check whether current state has changed
            if current_state.lines != new_graph.lines:
                n_repeat += 1
            else:
                n_sols += 1
                print(f"solutions: {n_sols}")
            
            # at restart, save current state and generate new start state
            if self.restart != False and n_repeat > self.restart:
                all_restart_K[current_state.K] = current_state
                if self.alg_choice.upper() == "R" or self.alg_choice.upper() == "RANDOM":
                    current_state = self.random_start_state()
                elif self.alg_choice.upper() == "G" or self.alg_choice.upper() == "GREEDY":
                    current_state = self.greedy_start_state()
                n_repeat = 0

        # if restart applied, save graph with highest K
        if self.restart != False:
            max_key = max(all_restart_K, key=int)
            self.graph = all_restart_K[max_key]

        # else, save current graph
        else:
            self.graph = current_state

        self.all_K = all_K
        self.all_opt_K = all_opt_K

        # print time
        print(f"\n time passed: {time.time() - start}")

        # save results
        if self.save_output == True:

            # file name
            extension = ''
            if self.prefer_unused_connection:
                extension += '_prefer_unused'
            if self.alg_choice.upper() == "R" or self.alg_choice.upper() == "RANDOM":
                extension += '_random_start'
            else:
                extension += '_greedy_start'
            if self.remove_trajectory.upper() == "K":
                extension += '_remove_K'
            else:
                extension += '_remove_random'
            if self.sim_anneal:
                extension += '_sim_anneal'
            if self.restart != False:
                extension += '_restart'
            
            # write result out to csv
            help.write_output_to_csv(self.graph, 'Hillclimber', extension)
            
            # create compact visualisation of result
            vis.visualise_solution_compact(self.graph, 'Hillclimber', extension)

            # create visualisation of optimal K improvement
            vis.visualise_opt_K_improvement(all_opt_K, 'Hillclimber', extension)

            # write out to csv all K (for distribution) all opt K (for iterations)
            help.write_to_csv(self.graph, all_K, all_opt_K, 'Hillclimber', extension)