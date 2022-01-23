import sys
import csv 

from code.classes import graph
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.visualisation import visualise as vis
from code.other import calculate_statespace as css


def main():

    #------------------------------ Request & Implement user input -------------------------------
    # Ask user for region
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

    # Ask user for algorithm to apply
    algorithm = input("Select algorithm: random (return r) or greedy (return g): ")
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
        question = input("Select goal: one solution (return 1) or optimal solution (return 2): ")

    if (algorithm.upper() == "R" and question == '2') or (algorithm.upper() != "R"):
        iterations = input("Type number of iterations: ")
    #----------------------------------- Load Graph based on region ------------------------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #----------------------------------- Calculate statespace/unique solutions ------------------------------------
    # state_space = css.state_space_cal(railway_map)

    # #--------------------------------------- Visualisation Start----------------------------------------
    # vis.visualise_start(railway_map, map_name)

    # #--------------------------------------- Implement Algorithms ----------------------------------------
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
        if question == '1':
            random = randomise.Random(railway_map)
            random.run_one_sol()
            final_graph = random.graph
        elif question == '2':
            random = randomise.Random(railway_map, int(iterations))
            random.run_opt_sol()
            final_graph = random.graph
            
            # print solution
            print("Found optimal K of:", random.graph.K)
            for traject in final_graph.lijnvoering.trajecten:
                print("Traject", final_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
    
    elif algorithm.upper() == "G" or algorithm.upper() == "GREEDY":
        greedy = gr.Greedy(railway_map, int(iterations))
        greedy.run()
        final_graph = greedy.graph
        
        # print solution
        print("Found optimal K of:", greedy.graph.K)
        for traject in greedy.graph.lijnvoering.trajecten:
            print("Traject", greedy.graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))

    else: 
        sys.exit("Algorithm not yet implemented")

    #-------------------------------------- Visualisation Result -----------------------------------------
    # vis.visualise_solution(final_graph, map_name)

    # #-------------------------------------- Final Output to csv-----------------------------------------
    # with open('output.csv', 'w', encoding='UTF8') as f:
        
    #     writer = csv.writer(f)

    #     # write the header
    #     writer.writerow(['train', 'stations'])

    #     # write the data
    #     for traject in final_graph.lijnvoering.trajecten:
    #         writer.writerow([f'train_{final_graph.lijnvoering.trajecten.index(traject)+1}', str(traject.stations).translate({39: None})])
        
    #     # write the footer
    #     writer.writerow(['score', final_graph.K])

if __name__ == '__main__':

    main()

    

    



