# user_input.py
#
# Minor programmeren
# Bèta-Programma
#
# Contains all user input command lines for running and adjusting the algorithms:
#   - region
#   - algorithm choice
#   - Random / Greedy / Hillclimber (Simulated Annealing)
#   - visualization choices

import sys

MAX_TRAJECTORIES_NSH = 7
MAX_TRAJECTORIES_NL = 20
MAX_DURATION_NSH = 120
MAX_DURATION_NL = 180


def region():
    """
    Ask user about region for which lines should be constructed.
    """

    # ask user for region
    region = input("Select region: North- & South-Holland (return NSH) or The Netherlands (return NL): ")

    # check and handle user input, assign assignment constraints
    if region.upper() == "NSH":
        map_name = "Holland"
        max_trajectories = MAX_TRAJECTORIES_NSH
        max_duration = MAX_DURATION_NSH
    elif region.upper() == "NL":
        map_name = "Nationaal"
        max_trajectories = MAX_TRAJECTORIES_NL
        max_duration = MAX_DURATION_NL
    else:
        sys.exit("Not a valid input")

    return map_name, max_trajectories, max_duration


def algo():
    """
    Ask based on which algorithm what features should be implemented.
    """

    # ask user about algorithm
    algorithm = input("Select algorithm: random (return r), greedy (return g) or hillclimber (return hc): ")

    # check for Random, Greedy or Hillclimber
    if algorithm.upper() != "R" and algorithm.upper() != "RANDOM" and \
            algorithm.upper() != "G" and algorithm.upper() != "GREEDY" and \
            algorithm.upper() != "HC" and algorithm.upper() != "HILLCLIMBER":
        sys.exit("Not a valid input")

    # ask user about prioritizing unused connections (while creating trajectories)
    prefer_unused_connection = input("Would you like to give unused connections priority? yes (return y) no return (n): ")

    # handle unused connections input
    if prefer_unused_connection.upper() == 'Y' or prefer_unused_connection.upper() == 'YES':
        prefer_unused_connection = True
    elif prefer_unused_connection.upper() == 'N' or prefer_unused_connection.upper() == 'NO':
        prefer_unused_connection = False
    else:
        sys.exit("Not a valid input")

    # ask if user wants to save and overwrite output
    save_output = input(
        "Would you like to save the output and overwrite previously saved output? yes (return y) no return (n): ")

    if save_output.upper() == 'Y' or save_output.upper() == 'YES':
        save_output = True
    elif save_output.upper() == 'N' or save_output.upper() == 'NO':
        save_output = False
    else:
        sys.exit("Not a valid input")

    return algorithm, prefer_unused_connection, save_output


def random():
    """
    Ask additional questions for random algorithm.
    """

    # initialize runtime
    runtime = '0'

    # ask if user wants 1 solution including connections or optimal solution
    question = input("Select goal: 1 solution with all connections (return 1) or optimal solution (return 2): ")

    # handle invalid input
    if question != '1' and question != '2':
        sys.exit("Not a valid input")

    # ask for runtime if optimal solution is chosen
    if question == '2':
        runtime = input("Type runtime in seconds: ")

    return question, runtime


def greedy():
    """
    Ask additional question for greedy algorithm.
    """

    runtime = input("Type runtime in seconds: ")

    return runtime


def hillclimber():
    """
    Ask additional question for hillclimber algorithm.
    """

    # ask number of iterations and start state algorithm
    iterations = input("Type number of iterations: ")
    alg_choice = input("Select algorithm for initial solution: random (return r) or greedy (return g): ").upper()

    # handle invalid input
    if alg_choice != "R" and alg_choice != "G":
        sys.exit("Not a valid input")

    # ask how to remove trajectory (lowest K or random)
    remove_traject = input("Would you like to remove trajectory with lowest K (return k) or random trajectory (return r)?: ")

    # handle invalid input
    if remove_traject.upper() != "K" and remove_traject.upper() != "R":
        sys.exit("Not a valid input")

    lin_or_exp = None

    # ask if user wants to apply simulated annealing
    sim_anneal = input("Would you like to apply simulated annealing? yes (return y) or no (return n): ")

    # if chosen for simulated annealing, ask for linear or exponential variant
    if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
        lin_or_exp = input("Would you like to apply linear (return l) or exponential (return e) formula?: ")
    # handle invalid input
    elif sim_anneal.upper() != "N" and sim_anneal.upper() != "NO":
        sys.exit("Not a valid input")

    # ask for restart
    restart = input("Would you like to restart if state has not changed after x iterations? \
                    yes (return number of iterations) or no (return n): ")

    # handle restart input
    if restart.upper() == "N" or restart.upper() == "NO":
        restart = False
    else:
        restart = int(restart)

    return iterations, alg_choice, remove_traject, sim_anneal, lin_or_exp, restart


def visualise_existing():
    """
    Ask additional questions for visualising existing distributions.
    """
    # ask user which visualization to plot
    goal = input("Would you like to visualize distributions (return d), K over iterations (return i) or both (return b)?: ")

    # handle invalid input
    if goal.upper() != "D" and goal.upper() != "I" and goal.upper() != "B":
        sys.exit("Not a valid input")

    return goal
