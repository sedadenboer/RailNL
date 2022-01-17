from code.classes import graph
from code.algorithms import randomise
from code.algorithms import greedy as gr
from code.visualisation import visualise as vis

if __name__ == '__main__':

    map_name = 'Holland'

    # Create a graph from datafile
    railway_map = graph.Graph(map_name)

    #---------------------------- Visualisation Start--------------------------
    vis.visualise_start(railway_map)

    #---------------------------- Random assignment --------------------------
    random_graph = randomise.random_algorithm(railway_map)
    vis.visualise_solution(random_graph)

    
    
    #---------------------------- Random Greedy reassignment --------------------------
   

   

    # vis.visualise_result(random_lijnvoering, f"data/{map_name}/{map_name}_regions.geojson")

    



