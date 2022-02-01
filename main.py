import sys

from code.classes import graph
from code.visualisation import visualise as vis
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import helpers
from code.other import user_input



def main():

    goal = input("Would you like to create new Lijnvoerig (return 1) or visualize existing Lijnvoeringen (return 2)?: ")
    
    if goal == '1':

        #------------------------------ Ask user for region and create graph + start visualisation ---------------------------------
        map_name, max_trajects, max_duration = user_input.region()
        railway_map = graph.Graph(map_name, max_trajects, max_duration)
        vis.visualise_start(railway_map, map_name)

        #------------------------------------ Ask user which algorithm with which featurs ------------------------------------------
        algorithm, prefer_unused_connection, save_output = user_input.algo()

        #--------------------------------------- Implement algorithm ----------------------------------------
        if algorithm.upper() == "R" or algorithm.upper() == "RANDOM":

            # ask additional questions
            question, runtime = user_input.random()

            # Question 1.1
            if question == '1':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output)
                random.run_one_sol()
                final_graph = random.graph
                helpers.print_statement_main(final_graph)

            # Question 1.2 / 2.1 met Random 
            elif question == '2':
                random = randomise.Random(railway_map, prefer_unused_connection, save_output, int(runtime))
                random.run_opt_sol()
                final_graph = random.graph
                helpers.print_statement_main(final_graph)
                
        elif algorithm.upper() == "G" or algorithm.upper() == "Greedy":

            # ask additional question
            runtime = user_input.greedy()

            # Question 1.2 / 2.1 met Greedy
            greedy = gr.Greedy(railway_map, prefer_unused_connection, save_output, int(runtime))
            greedy.run()
            final_graph = greedy.graph
            helpers.print_statement_main(final_graph)

        elif algorithm.upper() == "HC" or algorithm.upper() == "HILLCLIMBER":

            # additional questions
            iterations, alg_choice, remove_traject, sim_anneal, lin_or_exp, restart = user_input.hillclimber()

            # Question 1.2 / 2.1 met Hillclimber
            hillclimber = hc.Hillclimber(railway_map, prefer_unused_connection, save_output, alg_choice, remove_traject, int(iterations), sim_anneal, lin_or_exp, restart)
            hillclimber.run()
            final_graph = hillclimber.graph
            helpers.print_statement_main(final_graph)
    
    elif goal == '2':
        
        goal = user_input.visualise_existing()
        vis.start_comparing(goal)

    else: 
        sys.exit("Not a valid input")

    # #--------------------------------- Run algoritms simultaneously----------------------------------------
    # # Ask user to run all algorithms or one
    # K_comparison = input("Would you like to compare K improvement and distribution for all algorithms (return all) or run just one (return one)? ")
    
    # # If user wants to run all algorithms
    # if K_comparison.upper() == "ALL":
    #     # Ask user for total iterations
    #     runtime = input("Type runtime in minutes: ")
        
    #     # Ask user to apply heuristic
    #     prefer_unused_connection = input("Would you like to give unused connections priority? yes (return y) no return (n): ")
    #     if prefer_unused_connection.upper() == 'Y' or prefer_unused_connection.upper() == 'YES':
    #         prefer_unused_connection = True
    #     elif prefer_unused_connection.upper() == 'N' or prefer_unused_connection.upper() == 'NO': 
    #         prefer_unused_connection = False
    #     else:
    #         sys.exit("Not a valid input")
        
    #     # Don't overwrite current railway maps
    #     save_output = False

    #     # Run random algorithm
    #     random = randomise.Random(railway_map, prefer_unused_connection, save_output, int(runtime))
    #     random.run_opt_sol()

    #     # Run greedy algorithm
    #     greedy = gr.Greedy(railway_map, prefer_unused_connection, save_output, int(runtime))
    #     greedy.run()
        
    #     # Ask user for hillclimber variables
    #     alg_choice = input("Select algorithm for initial solution: random (return r) or greedy (return g): ").upper()
    #     start_iterations = input("Type number of random/greedy iterations to generate start state: ")
    #     remove_traject = input("Would you like to remove traject with lowest K (return k) or random traject (return r)?: ")
    #     sim_anneal = input("Would you like to apply simulated annealing? yes (return y) or no (return n): ")
    #     if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
    #         lin_or_exp = input("Would you like to apply linear (return l) or exponential (return e) formula?: ")
    #     else:
    #         lin_or_exp = None
        
    #     # Run hillcimber algorithm with given input
    #     hillclimber = hc.Hillclimber(railway_map, prefer_unused_connection, save_output, alg_choice, remove_traject, int(runtime), int(start_iterations), sim_anneal, lin_or_exp)
    #     hillclimber.run()

    #     # Visualize K improvement of all algorithms in one graph
    #     vis.visualise_opt_K_all_algorithms(random.all_opt_K, greedy.all_opt_K, hillclimber.all_opt_K, prefer_unused_connection, alg_choice, start_iterations, remove_traject)

    #     # Visualize K distribution of a sample of N iterations for all algorithms
    #     vis.visualise_K_distribution_comparison(random.all_K, greedy.all_K, hillclimber.all_K, prefer_unused_connection, alg_choice, start_iterations, remove_traject, sim_anneal, lin_or_exp)

    # #--------------------------------------- Implement single algorithm ----------------------------------------
    # else:
        
 

        
 


if __name__ == '__main__':

    main()

    

    



