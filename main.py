import sys

from code.classes import graph
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.visualisation import visualise as vis

def main():

    region = input("Select North- & South-Holland (return NSH) or The Netherlands (return NL): ")
    if region == "NSH" or region == "nsh":
        question = input("Select part 1 (return 1) or part 2 (return 2): ")
        map_name = 'Holland'
        max_trajects = 7
        max_duration = 120
    elif region == "NL" or region == "nl":
        map_name = 'Nationaal'
        max_trajects = 20
        max_duration = 180
    else: 
        sys.exit("Not a valid input")

    #------------------------- Load Graph based on region ----------------------
    railway_map = graph.Graph(map_name, max_trajects, max_duration)

    #---------------------------- Visualisation Start--------------------------
    vis.visualise_start(railway_map, map_name)

    #---------------------------- Random assignment --------------------------
    random_graph = randomise.random_algorithm(railway_map)
    vis.visualise_solution(random_graph, map_name)

    #---------------------------- Random Greedy reassignment --------------------------
   

   

    # vis.visualise_result(random_lijnvoering, f"data/{map_name}/{map_name}_regions.geojson")


if __name__ == '__main__':

    main()

    

    



