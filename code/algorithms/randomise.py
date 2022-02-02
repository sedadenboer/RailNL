# randomise.py
#
# Minor Programmeren
# Bèta-Programma
#
# - Random class which creates random algorithm line solution.
# - Creates a graph with one line solution or an optimal line solution.
# - Results (plots) can be saved optionally.

from code.algorithms import helpers as help
from code.visualisation import visualise as vis
import random
import copy
import time


class Random:
    """
    The Random class that chooses a valid random new connection in each Trajectory.
    """

    def __init__(self, graph, prefer_unused_connection, save_output, runtime=None):

        self.graph = copy.deepcopy(graph)
        self.runtime = runtime
        self.prefer_unused_connection = prefer_unused_connection
        self.Nsols = int
        self.all_K = []
        self.dict_K = dict()
        self.save_output = save_output
        self.all_opt_K = dict()

    def run_one_sol(self):
        """
        Algorithm that looks for combination of trajectories such that all connections are used.
        """

        print('\nloading randomly constructed lines...\n')

        solution = False
        nTry = 0

        while solution == False:
            # for each try, create a new graph
            nTry += 1
            new_graph = copy.deepcopy(self.graph)

            # find stations with one connection
            start_stations = help.begin_stations(self.graph)

            # if not yet max. trajectories and solution not found, add new trajectory to lines
            while len(new_graph.unused_connections) != 0 and help.reached_max_depth(new_graph) == False:
                help.new_trajectory(new_graph, start_stations, random.choice, self.prefer_unused_connection)

            # if all connections used, print solution and stop loop
            if len(new_graph.unused_connections) == 0:
                solution = True

                # add quality-goalfunction
                new_graph.lines_quality(new_graph.used_connections,
                                        new_graph.available_connections,
                                        new_graph.lines.trajectories)

                # print output while rendering a solution
                print('Found the following correct lines at try number:', nTry)
                for i, trajectory in enumerate(new_graph.lines.trajectories):
                    print('trajectory', i + 1, ':', trajectory.stations)
                    print('duration:', trajectory.duration)
                    print('connections', trajectory.connections)

        # add graph of solution to Random object
        self.graph = new_graph

        # save output
        if self.save_output:
            # write result out to csv
            help.write_output_to_csv(new_graph, 'Random/One_Solution')

            # create visualisation of result
            vis.visualise_solution_compact(new_graph, 'Random/One_Solution')

    def run_opt_sol(self):
        """
        Algorithm that looks for combination of trajectories such that quality goal-fucntion is optimized.
        """

        print('\nloading randomly constructed lines...\n')

        # store variables
        opt_K = 0
        opt_map = self.graph
        all_K = []
        dict_K = dict()
        all_opt_K = dict()

        # start variables
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

            # if not yet all stations and max. number of trajectories reached, add new trajectory to lines
            while help.reached_max_depth(new_graph) == False and help.visited_all_stations(new_graph) == False:
                help.new_trajectory(new_graph, start_stations, random.choice, self.prefer_unused_connection)

            # only valid solution if all stations are visited
            if help.visited_all_stations(new_graph):
                n_sols += 1
                print(f"solutions: {n_sols}")

                # add quality-goalfunction
                new_graph.lines_quality(new_graph.used_connections,
                                        new_graph.available_connections,
                                        new_graph.lines.trajectories)

                # if quality higher than optimal, replace optimal results
                if new_graph.K > opt_K:
                    opt_K = new_graph.K
                    opt_map = new_graph

                # sample variables
                all_K.append(new_graph.K)
                if len(new_graph.lines.trajectories) in dict_K.keys():
                    dict_K[len(new_graph.lines.trajectories)].append(new_graph.K)
                else:
                    dict_K[len(new_graph.lines.trajectories)] = [new_graph.K]

                # add the current optimal K to a dictionary with the solution number as key
                all_opt_K[n_sols] = opt_K

        # add optimal graph and K to Random object
        self.graph = opt_map
        self.Nsols = n_sols
        self.all_K = all_K
        self.dict_K = dict_K
        self.all_opt_K = all_opt_K

        # save output
        if self.save_output:

            # file name
            extension = ''
            if self.prefer_unused_connection:
                extension += '_prefer_unused'

            # write result out to csv
            help.write_output_to_csv(opt_map, 'Random/Opt_Solution/', extension)

            # create compact visualisation of result
            vis.visualise_solution_compact(opt_map, 'Random', extension, 'Opt_Solution')

            # create visualisation of optimal K improvement
            vis.visualise_opt_K_improvement(all_opt_K, 'Random', extension)

            # write all K (for distribution) and all opt K (for iterations) out to csv
            help.write_to_csv(self.graph, all_K, all_opt_K, 'Random', extension)
