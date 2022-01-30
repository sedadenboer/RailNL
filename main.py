import sys
import time
import pickle

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

    #----------------------------------- Load Graph based on region  ------------------------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #----------------------------------- Calculate statespace ------------------------------------
    # state_space = css.state_space_cal(railway_map)

    #--------------------------------------- Visualisation Start----------------------------------------
    vis.visualise_start(railway_map, map_name)

    # Ask user to run all algorithms or one
    K_comparison = input("Would you like to compare K improvement and distribution for all algorithms (return all) or run just one (return one)? ")
    
    # If user wants to run all algorithms
    if K_comparison.upper() == "ALL":
        # Ask user for total iterations
        iterations = input("Type number of iterations: ")
        
        # Ask user to apply heuristic
        prefer_unused_connection = input("Would you like to give unused connections priority? yes (return y) no return (n): ")
        if prefer_unused_connection.upper() == 'Y' or prefer_unused_connection.upper() == 'YES':
            prefer_unused_connection = True
        elif prefer_unused_connection.upper() == 'N' or prefer_unused_connection.upper() == 'NO': 
            prefer_unused_connection = False
        else:
            sys.exit("Not a valid input")
        
        # Don't overwrite current railway maps
        save_output = False

        # Run random algorithm
        random = randomise.Random(railway_map, prefer_unused_connection, save_output, int(iterations))
        random.run_opt_sol()

        # Run greedy algorithm
        greedy = gr.Greedy(railway_map, prefer_unused_connection, save_output, int(iterations))
        greedy.run()
        
        # Ask user for hillclimber variables
        alg_choice = input("Select algorithm for initial solution: random (return r) or greedy (return g): ").upper()
        start_iterations = input("Type number of random/greedy iterations to generate start state: ")
        remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
        sim_anneal = input("Would you like to apply simulated annealing? yes (return y) or no (return n): ")
        if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
            lin_or_exp = input("Would you like to apply linear (return l) or exponential (return e) formula?: ")
        else:
            lin_or_exp = None
        
        # Run hillcimber algorithm with given input
        hillclimber = hc.Hillclimber(railway_map, prefer_unused_connection, save_output, alg_choice, remove_traject, int(iterations), int(start_iterations), sim_anneal, lin_or_exp)
        hillclimber.run()

        # Visualize K improvement of all algorithms in one graph
        vis.visualise_opt_K_all_algorithms(random.all_opt_K, greedy.all_opt_K, hillclimber.all_opt_K, prefer_unused_connection, alg_choice, start_iterations, remove_traject)

        # Visualize K distribution of a sample of N iterations for all algorithms
        vis.visualise_K_distribution_comparison(random.all_K, greedy.all_K, hillclimber.all_K, prefer_unused_connection, alg_choice, start_iterations, remove_traject, sim_anneal, lin_or_exp)

    # If user wants to run just one algorithm
    else:
        # Ask user for algorithm to apply
        algorithm = input("Select algorithm: random (return r), greedy (return g) or hillclimber (return hc): ")
        
        if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":
            question = input("Select goal: 1 solution (all connection, return 1) or optimal solution (return 2): ")

        if ((algorithm.upper() == "R" or algorithm.upper() == "RANDOM") and question == '2') or (algorithm.upper() != "R"):
            iterations = input("Type number of iterations: ")
        
        # Ask user to apply heuristic yes or no
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

        #--------------------------------------- Implement Algorithms ----------------------------------------
        tic = time.perf_counter()

        if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":

            # Question 1.1
            if question == '1':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output)
                random.run_one_sol()
                final_graph = random.graph

            # Question 1.2 / 2.1 met Random 
            elif question == '2':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output, int(iterations))
                random.run_opt_sol()
                final_graph = random.graph
                
                # print solution
                print("Found optimal K of:", random.graph.K)
                for traject in final_graph.lijnvoering.trajecten:
                    print("Traject", final_graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
        
        # Question 1.2 / 2.1 met Greedy
        elif algorithm.upper() == "G" or algorithm.upper() == "Greedy":
            greedy = gr.Greedy(railway_map, prefer_unused_connection, save_output, int(iterations))
            greedy.run()
            final_graph = greedy.graph
            
            # print solution
            print("Found optimal K of:", greedy.graph.K)
            for traject in greedy.graph.lijnvoering.trajecten:
                print("Traject", greedy.graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))

        elif algorithm.upper() == "HC" or algorithm.upper() == "HILLCLIMBER":
            alg_choice = input("Select algorithm for initial solution: random (return r) or greedy (return g): ").upper()
            start_iterations = input("Type number of random/greedy iterations to generate start state: ")
            remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
            sim_anneal = input("Would you like to apply simulated annealing? yes (return y) or no (return n): ")
            if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
                lin_or_exp = input("Would you like to apply linear (return l) or exponential (return e) formula?: ")
            else:
                lin_or_exp = None
            restart = input("Would you like to restart if state has not changed after x iterations? yes (return number of iterations) or no (return no): ")
            if restart.upper() == "NO":
                restart = False
            else:
                restart = int(restart)

            hillclimber = hc.Hillclimber(railway_map, prefer_unused_connection, save_output, alg_choice, remove_traject, int(iterations), int(start_iterations), sim_anneal, lin_or_exp, restart)
            hillclimber.run()
            final_graph = hillclimber.graph

            # print solution
            print("Found optimal K of:", hillclimber.graph.K)
            for traject in hillclimber.graph.lijnvoering.trajecten:
                print("Traject", hillclimber.graph.lijnvoering.trajecten.index(traject), "\n", ", ".join(traject.stations))
    
        else: 
            sys.exit("Algorithm not (yet) implemented")

        toc = time.perf_counter()

        print(f"Algorithm runned for {toc - tic:0.4f} seconds / {(toc - tic)/60:0.4f} minutes")

        ## optional pickle dumping
        # pickle.dump(final_graph, open( "save.p", "wb" ) )
        # favorite_color = pickle.load( open( "save.p", "rb" ) )

if __name__ == '__main__':

    main()

    

    



