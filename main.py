import sys
import csv 

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

    #----------------------------------- Load Graph based on region ------------------------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #--------------------------------------- Visualisation Start----------------------------------------
    vis.visualise_start(railway_map, map_name)

    #--------------------------------------- Implement Algorithm ----------------------------------------
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
        if map_name == 'HOLLAND' and question == 1:
            final_graph = randomise.random_algorithm_one_sol(railway_map)
        else:
            final_graph, K = randomise.random_algorithm_opt_sol(railway_map)
            print("Found optimal K of:", K)
            for traject in final_graph.lijnvoering:
                print("Traject", final_graph.lijnvoering.index(traject), "\n", ", ".join(traject.stations))

    else: 
        sys.exit("Algorithm not yet implemented")

    #-------------------------------------- Visualisation Result -----------------------------------------
    vis.visualise_solution(final_graph, map_name)

    #-------------------------------------- Final Output to csv-----------------------------------------
    with open('output.csv', 'w', encoding='UTF8') as f:
        
        writer = csv.writer(f)

        # write the header
        writer.writerow(['train', 'stations'])

        # write the data
        for traject in final_graph.lijnvoering:
            writer.writerow([f'train_{final_graph.lijnvoering.index(traject)+1}', str(traject.stations).translate({39: None})])
        
        # write the footer
        writer.writerow(['score', final_graph.K])

if __name__ == '__main__':

    main()

    

    



