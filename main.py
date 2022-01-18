import sys

from code.classes import graph
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.visualisation import visualise as vis

def main():

    #------------------------------ Request & Implement user input -------------------------------
    region = input("Select region: North- & South-Holland (return NSH) or The Netherlands (return NL): ")
    algorithm = input("Select algorithm: random (return r) or greedy (return g): ")
    if region.upper() == "NSH":
        question = input("Select goal: one solution (return 1) or optimal solution (return 2): ")
        map_name = 'Holland'
        max_trajects = 7
        max_duration = 120
    elif region.upper() == "NL":
        map_name = 'Nationaal'
        max_trajects = 20
        max_duration = 180
    else: 
        sys.exit("Not a valid input")

    #------------------------------ Load Graph based on region ------------------------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #---------------------------------- Visualisation Start----------------------------------------
    vis.visualise_start(railway_map, map_name)

    #------------------------------------ Start algorithm ----------------------------------------
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
        if map_name == 'HOLLAND' and question == 1:
            random_graph = randomise.random_algorithm_one_sol(railway_map)
        else:
            random_graph = randomise.random_algorithm_opt_sol(railway_map)
    else: 
        sys.exit("Algorithm not yet implemented")

    #---------------------------- Display visualisation results ------------------------------------
    vis.visualise_solution(random_graph, map_name)


if __name__ == '__main__':

    main()

    

    



