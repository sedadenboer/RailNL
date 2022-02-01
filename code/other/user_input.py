import sys
import glob
import os

def region():
    """
    ask user about region for which Lijnvoering should be constructed
    """
    region = input("Select region: North- & South-Holland (return NSH) or The Netherlands (return NL): ")
    if region.upper() == "NSH":
        map_name = 'Holland'
        max_trajects = 7
        max_duration = 120
    elif region.upper() == "NL":
        map_name = 'Nationaal'
        max_trajects = 20
        max_duration = 180
    else: 
        sys.exit("Not a valid input")
    
    return map_name, max_trajects, max_duration

def algo():
    """
    ask based on which algorithm with which features he/she would like to implement
    """

    # ask user about algorithm
    algorithm = input("Select algorithm: random (return r), greedy (return g) or hillclimber (return hc): ")
    if algorithm.upper != "R" and algorithm.upper != "RANDOM" and \
        algorithm.upper != "g" and algorithm.upper != "GREEDY" and \
            algorithm.upper != "HC" and algorithm.upper != "HILLCLIMBER":
        sys.exit("Not a valid input")
    
    # ask user to apply heuristic yes or no
    prefer_unused_connection = input("Would you like to give unused connections priority? yes (return y) no return (n): ")
    if prefer_unused_connection.upper() == 'Y' or prefer_unused_connection.upper() == 'YES':
        prefer_unused_connection = True
    elif prefer_unused_connection.upper() == 'N' or prefer_unused_connection.upper() == 'NO': 
        prefer_unused_connection = False
    else:
        sys.exit("Not a valid input")
    
    # Ask user to save output 
    save_output = input("Would you like to save the output and overwrite previously saved output? yes (return y) no return (n): ")
    if save_output.upper() == 'Y' or save_output.upper() == 'YES':
        save_output = True
    elif save_output.upper() == 'N' or save_output.upper() == 'NO': 
        save_output = False
    else:
        sys.exit("Not a valid input")
    
    return algorithm, prefer_unused_connection, save_output

def random():
    """
    ask additional questions for random algorithm
    """

    runtime = '0'
    question = input("Select goal: 1 solution with all connection (return 1) or optimal solution (return 2): ")
    if question != '1' and question != '2':
        sys.exit("Not a valid input")
    
    if question == '2':
        runtime = input("Type runtime in seconds: ")
    
    return question, runtime

def greedy():
    """
    ask additional question for greedy algorithm
    """

    runtime = input("Type runtime in seconds: ")

    return runtime

def hillclimber():
    """
    ask additional question for hillclimber algorithm
    """

    iterations = input("type number of iterations: ")

    alg_choice = input("Select algorithm for initial solution: random (return r) or greedy (return g): ").upper()
    if alg_choice != "R" and alg_choice != "G":
        sys.exit("Not a valid input")
    
    remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
    if remove_traject.upper() != "K" and remove_traject.upper() != "R":
        sys.exit("Not a valid input")
    
    lin_or_exp = None
    sim_anneal = input("Would you like to apply simulated annealing? yes (return y) or no (return n): ")
    if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
        lin_or_exp = input("Would you like to apply linear (return l) or exponential (return e) formula?: ")
    elif sim_anneal.upper() != "N" and sim_anneal.upper() != "NO":
        sys.exit("Not a valid input")
    
    restart = input("Would you like to restart if state has not changed after x iterations? yes (return number of iterations) or no (return n): ")
    if restart.upper() == "N" or restart.upper() == "NO":
        restart = False
    else:
        restart = int(restart)

    return iterations, alg_choice, remove_traject, sim_anneal, lin_or_exp, restart
    
def visualise_existing():

    goal = input("Would you like to visualize distributions (return d), K over iterations (return i) or both (return b)?: ")
    if goal.upper() != "D" and goal.upper() != "I" and goal.upper() != "B":
        sys.exit("Not a valid input")
    
    return goal
    

       