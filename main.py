# main.py
#
# Minor programmeren
# Bèta-Programma
#
# - Lets you create a RailNL line solution through the command-line.
# - All files in /code are required for this file to work.

import sys

from code.classes import graph
from code.visualisation import visualise as vis
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import helpers
from code.other import user_input


def main():

    goal = input("Would you like to create new Lines (return 1) or visualize existing Lines (return 2)?: ")

    # option 1: create new lines
    if goal == '1':
        # ------------------------------ Ask user for region and create graph + start visualisation ---------------------------------
        map_name, max_trajects, max_duration = user_input.region()
        railway_map = graph.Graph(map_name, max_trajects, max_duration)
        vis.visualise_start(railway_map, map_name)

        # ------------------------------------ Ask user which algorithm and what features ------------------------------------------
        algorithm, prefer_unused_connection, save_output = user_input.algo()

        # --------------------------------------- Implement algorithm ----------------------------------------
        if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
            # ask additional questions
            question, runtime = user_input.random()

            # create one valid line solution with Random
            if question == '1':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output)
                random.run_one_sol()
                final_graph = random.graph
                helpers.print_statement_main(final_graph)

            # create optimal line solution with Random
            elif question == '2':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output, int(runtime))
                random.run_opt_sol()
                final_graph = random.graph
                helpers.print_statement_main(final_graph)

        elif algorithm.upper() == "G" or algorithm.upper() == "Greedy":
            # ask runtime for Greedy
            runtime = user_input.greedy()

            # create optimal line solution with Greedy
            greedy = gr.Greedy(railway_map, prefer_unused_connection, save_output, int(runtime))
            greedy.run()
            final_graph = greedy.graph
            helpers.print_statement_main(final_graph)

        elif algorithm.upper() == "HC" or algorithm.upper() == "HILLCLIMBER":
            # parameter input for Hillclimber
            iterations, alg_choice, remove_traject, sim_anneal, lin_or_exp, restart = user_input.hillclimber()

            # create optimal line solution with Hillclimber
            hillclimber = hc.Hillclimber(railway_map, prefer_unused_connection, save_output, alg_choice,
                                         remove_traject, int(iterations), sim_anneal, lin_or_exp, restart)
            hillclimber.run()
            final_graph = hillclimber.graph
            helpers.print_statement_main(final_graph)

    # option 2: visualize existing Lines
    elif goal == '2':
        goal = user_input.visualise_existing()
        vis.start_comparing(goal)

    else:
        # handle invalid input
        sys.exit("Not a valid input")


if __name__ == '__main__':

    main()