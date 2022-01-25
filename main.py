import sys

from code.classes import graph
from code.visualisation import visualise as vis
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
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
    algorithm = input("Select algorithm: random (return r), greedy (return g) or hillclimber (return hc): ")
    
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
        question = input("Select goal: 1 solution (all connection, return 1) or optimal solution (return 2): ")

    if ((algorithm.upper() == "R" or algorithm.upper() == "RANDOM") and question == '2') or (algorithm.upper() != "R"):
        iterations = input("Type number of iterations: ")

    #----------------------------------- Load Graph based on region  ------------------------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #----------------------------------- Calculate statespace ------------------------------------
    # state_space = css.state_space_cal(railway_map)

    #--------------------------------------- Visualisation Start----------------------------------------
    vis.visualise_start(railway_map, map_name)

    #--------------------------------------- Implement Algorithms ----------------------------------------
    if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":

        # Question 1.1
        if question == '1':
            random = randomise.Random(railway_map)
            random.run_one_sol()
            final_graph = random.graph

        # Question 1.2 / 2.1 met Random 
        elif question == '2':
            random = randomise.Random(railway_map, int(iterations))
            random.run_opt_sol()
            final_graph = random.graph
            
            # print solution
            print("Found optimal K of:", random.graph.K)
            for traject in final_graph.lijnvoering.trajecten:
                print("Traject", final_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
    
    # Question 1.2 / 2.1 met Greedy
    elif algorithm.upper() == "G" or algorithm.upper() == "Greedy":
        greedy = gr.Greedy(railway_map, int(iterations))
        greedy.run()
        final_graph = greedy.graph
        
        # print solution
        print("Found optimal K of:", greedy.graph.K)
        for traject in greedy.graph.lijnvoering.trajecten:
            print("Traject", greedy.graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))

    elif algorithm.upper() == "HC" or algorithm.upper() == "HILLCLIMBER":
        alg_choice = input("Select algorithm for initial solution: random (return R) or greedy (return G): ").upper()

        if alg_choice == "R" or alg_choice == "RANDOM":
            remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
            hillclimber = hc.Hillclimber(railway_map, int(iterations), alg_choice, remove_traject, None)
        elif alg_choice == "G" or alg_choice == "GREEDY":
            greedy_iterations = input("Type number of greedy iterations: ")
            remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
            hillclimber = hc.Hillclimber(railway_map, int(iterations), alg_choice, remove_traject, int(greedy_iterations))
        
        hillclimber.run()
        final_graph = hillclimber.graph

        # print solution
        print("Found optimal K of:", hillclimber.graph.K)
        for traject in hillclimber.graph.lijnvoering.trajecten:
            print("Traject", hillclimber.graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
   
    else: 
        sys.exit("Algorithm not yet implemented")


if __name__ == '__main__':

    main()

    

    



