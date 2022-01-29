from matplotlib import pyplot as plt
import numpy as np
import os

def visualise_start(railway_map, map_name):
    """
    Visualisation code that displays the railnetwork of the selected area
    """
    print("\nLoading main visualisation...\n")
    
    # load station information
    x = []
    y = []
    z = []
    for station in railway_map.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        z.append(station.name)

    # create scatterplot of based on x- and y-coord of stations
    plt.figure(figsize=(30, 20))
    plt.scatter(y, x, c = 'black', s = 15)

    # add station name to each scatter plot point
    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))
    
    # plot all connections between stations 
    for connection in railway_map.available_connections:

        # retrieve initial information of all connections
        station1 = railway_map.stations[connection.stations[0]]
        x1 = float(station1.x_coord)
        y1 = float(station1.y_coord)
        station2 = railway_map.stations[connection.stations[1]]
        x2 = float(station2.x_coord)
        y2 = float(station2.y_coord)

        # plot connection between Stations
        plt.plot([y1, y2], [x1, x2], c = 'black', alpha = 0.25)
        
        # add duration of connection
        plt.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

    # add titles to plot of Railway Network and remove x- and y-tics
    plt.suptitle("Intercity connections North- and South-Holland", fontsize=25, y = 0.93)
    plt.title('Duration in minutes', fontsize=18, y = 1.01)
    plt.xticks([], [])
    plt.yticks([], [])

    # save figure
    plt.savefig(f"docs/Stations_{map_name}")

def visualise_solution_compact(final_graph, algorithm_name):
    """
    Visualisation code that displays the found 'lijnvoering'
    """
    print("\nLoading solution visualisation...\n")


    # select colors for trajects
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(final_graph.max_trajects):
        colors.append(cm(i/final_graph.max_trajects))

    # load station information
    x = []
    y = []
    z = []
    for station in final_graph.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        station_name = station.name.split()
        new_name = ""
        for i in range(len(station_name)):
            if i == 0:
                new_name += station_name[i]
            else:
                new_name += '-' + station_name[i][0]
        z.append(new_name)

    # create scatterplot of based on x- and y-coord of stations
    plt.figure(figsize=(20, 25))
    plt.scatter(y, x, c = 'black', s = 15)

    # add station name to each scatter plot point
    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))
    
    # plot all connections between stations 
    for connection in final_graph.available_connections:

        # retrieve initial information of all connections
        station1 = final_graph.stations[connection.stations[0]]
        x1 = float(station1.x_coord)
        y1 = float(station1.y_coord)
        station2 = final_graph.stations[connection.stations[1]]
        x2 = float(station2.x_coord)
        y2 = float(station2.y_coord)

        # plot connection between Stations
        plt.plot([y1, y2], [x1, x2], c = 'black', alpha = 1, linestyle=':')
        
        # # add duration of connection
        plt.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

    connection_visited = dict()
    # for each traject, plot all connections
    n = 0
    for traject in final_graph.lijnvoering.trajecten:
        n += 1
        c = 0
        for connection in traject.connections:
            c += 1
            connection_visited[connection.id] = connection_visited.get(connection.id,0) + 1
            times_visited = connection_visited[connection.id]

            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)

            # print(f"draw connection {connection} which is visited {times_visited} times")
            plt.plot([y1 - 0.005 * (times_visited-1), y2 - 0.005 * (times_visited-1)], [x1 + 0.002 * (times_visited-1), x2 + 0.002 * (times_visited-1)], c = colors[n - 2], alpha = 0.5, linewidth=4.0, label=f"Traject {n}" if c == 1 else "")
        
    # add titles to plot of Railway Network and remove x- and y-tics
    plt.suptitle(f"Railnetwork generated by {algorithm_name} Algorithm (K = {str(round(final_graph.K, 2))}, p = {str(round(len(set(final_graph.used_connections))/len(final_graph.available_connections), 2))})", fontsize = 20, y = 0.9)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.axis('scaled')
    plt.legend()

    # create filename based on region and algorithm
    if final_graph.max_trajects == 7:
        file = 'results/' + str(algorithm_name) + '/Holland/visualisation_compact'
    else:
        file = 'results/' + str(algorithm_name) + '/Nationaal/visualisation_compact'

    # save figure
    plt.savefig(file)


def visualise_solution(final_graph, algorithm_name):
    """
    Visualisation code that displays the found 'lijnvoering'
    """
    print("\nLoading solution visualisation...\n")


    # select colors for trajects
    colors = []
    cm = plt.get_cmap('gist_rainbow')
    for i in range(final_graph.max_trajects):
        colors.append(cm(i/final_graph.max_trajects))

    # load station information
    x = []
    y = []
    z = []
    for station in final_graph.stations.values():
        x.append(float(station.x_coord))
        y.append(float(station.y_coord))
        z.append(station.name)

    # determine height of figure based on number of trajects
    if len(final_graph.lijnvoering.trajecten) > 6:
        fig = plt.figure(figsize=(70, 70))
    else:
        fig = plt.figure(figsize=(70, 40))

    # create subplot for each traject
    n_trajects = 1
    fig.subplots_adjust(hspace=0.4, wspace=0.2)

    for traject in final_graph.lijnvoering.trajecten:
        
        # determine dimensions of figure based on number of trajects
        if len(final_graph.lijnvoering.trajecten) > 9:
            ax = fig.add_subplot(5, 4, n_trajects)
        elif len(final_graph.lijnvoering.trajecten) > 6 and len(final_graph.lijnvoering.trajecten) < 10:
            ax = fig.add_subplot(3, 3, n_trajects)
        else:
            ax = fig.add_subplot(2, 3, n_trajects)

        # update total number of trajects and set title to subplot
        n_trajects += 1
        ax.set_title(f'Traject {n_trajects - 1}: {traject.stations[0]} --> {traject.stations[-1]} ({traject.duration} min.)', fontsize=25)

        # create main rail network with station names 
        ax.scatter(y, x, c = 'black', s = 15)
        for i, txt in enumerate(z):
            ax.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

        # plot all connections between stations including the duration
        for connection in set(final_graph.available_connections):
            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)
            ax.plot([y1, y2], [x1, x2], c = 'black', alpha = 0.20)
            ax.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

        # plot all connections in the traject 
        for connection in traject.connections:
            station1 = final_graph.stations[connection.stations[0]]
            x1 = float(station1.x_coord)
            y1 = float(station1.y_coord)
            station2 = final_graph.stations[connection.stations[1]]
            x2 = float(station2.x_coord)
            y2 = float(station2.y_coord)
            ax.plot([y1, y2], [x1, x2], c = colors[n_trajects - 2], alpha = 0.25, linewidth=4.0)
            ax.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

        # remove x and y -tics
        ax.set_xticks([])
        ax.set_yticks([])

    # add title 
    fig.suptitle(f"Railnetwork generated by Random Algorithm (K = {final_graph.K})", fontsize=45, y = 0.93)

    # create filename based on region and algorithm
    if final_graph.max_trajects == 7:
        file = 'results/' + str(algorithm_name) + '/Holland/visualisation'
    else:
        file = 'results/' + str(algorithm_name) + '/Nationaal/visualisation'

    # save figure
    fig.savefig(file)


# def visualise_solution_compact(final_graph, algorithm_name):
#     """
#     Visualisation code that displays the found 'lijnvoering'
#     """

#     # select colors for trajects
#     colors = []
#     cm = plt.get_cmap('gist_rainbow')
#     for i in range(final_graph.max_trajects):
#         colors.append(cm(i/final_graph.max_trajects))

#     # load station information
#     x = []
#     y = []
#     z = []
#     for station in final_graph.stations.values():
#         x.append(float(station.x_coord))
#         y.append(float(station.y_coord))
#         z.append(station.name)

#     fig = plt.figure(figsize=(30, 20))
#     ax = fig.add_subplot(111)

#     # create subplot for each traject
#     n_trajects = 1

#     for traject in final_graph.lijnvoering.trajecten:

#         # update total number of trajects and set title to subplot
#         n_trajects += 1

#         # create main rail network with station names 
#         ax.scatter(y, x, c = 'black', s = 15)
#         for i, txt in enumerate(z):
#             ax.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

#         # plot all connections between stations including the duration
#         for connection in set(final_graph.available_connections):
#             station1 = final_graph.stations[connection.stations[0]]
#             x1 = float(station1.x_coord)
#             y1 = float(station1.y_coord)
#             station2 = final_graph.stations[connection.stations[1]]
#             x2 = float(station2.x_coord)
#             y2 = float(station2.y_coord)
#             ax.plot([y1, y2], [x1, x2], c = 'black', alpha = 0.20)
#             ax.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

#         # plot all connections in the traject 
#         for connection in traject.connections:
#             station1 = final_graph.stations[connection.stations[0]]
#             x1 = float(station1.x_coord)
#             y1 = float(station1.y_coord)
#             station2 = final_graph.stations[connection.stations[1]]
#             x2 = float(station2.x_coord)
#             y2 = float(station2.y_coord)
#             # TODO: fix overlap of trajectories !
#             # https://stackoverflow.com/questions/61993940/how-to-fix-the-overlapping-lines-in-matplotlib-plot
#             ax.plot([y1, y2], [x1, x2], c = colors[n_trajects - 2], alpha = 0.3, linewidth=5)
#             ax.annotate(connection.duration, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

#         # remove x and y -tics
#         ax.set_xticks([])
#         ax.set_yticks([])

#     # add title 
#     fig.suptitle(f"Railnetwork generated by Random Algorithm (K = {final_graph.K}, #trajectories = {n_trajects})", fontsize=30, y = 0.93)

#     # create filename based on region and algorithm
#     if final_graph.max_trajects == 7:
#         file = 'results/' + str(algorithm_name) + '/Holland/visualisation_compact'
#     else:
#         file = 'results/' + str(algorithm_name) + '/Nationaal/visualisation_compact'

#     # save figure
#     fig.savefig(file)

def visualise_steekproef(all_K):
    """
    Visualisation code that displays the found 'lijnvoering'
    """
    fig = plt.figure(figsize=(20,20))
    plt.hist(all_K, bins = 250, color = 'grey', density = False)
    plt.xlabel('K', fontsize = 20)
    plt.ylabel('frequency', fontsize=20)
    plt.xticks(fontsize= 10)
    fig.suptitle(f"Frequency Histogram of K generated by Random Algorithm \n (n= {len(all_K)}, mean = {round(np.mean(all_K),2)}, var = {round(np.var(all_K),2)})", fontsize=25, y = 0.93)
    fig.savefig(f"plots/steekproef")

def visualise_steekproef_by_trajects(dict_K):
    """
    Visualisation code that displays the found 'lijnvoering'
    """

    # select colors for number of trajects
    
    colors = ['red', 'green', 'blue', 'purple']

    fig = plt.figure(figsize=(20,20))
    i = 0
    tot_obs = 0
    for key in dict_K.keys():
        plt.hist(dict_K[key], bins = 250, color = colors[i], density = False, label=f"{key} (mean = {round(np.mean(dict_K[key]),2)}, var = {round(np.var(dict_K[key]),2)})")
        i += 1
        tot_obs += len(dict_K[key])
    plt.xlabel('K', fontsize = 20)
    plt.ylabel('frequency', fontsize=20)
    plt.xticks(fontsize= 10)
    plt.legend(title = "Number of trajects")
    
    fig.suptitle(f"Frequency Histogram of K generated by Random Algorithm \n (n= {tot_obs})", fontsize=25, y = 0.93)
    fig.savefig(f"plots/steekproef_pro_trajects")

   
def visualise_opt_K_improvement(all_opt_K, algorithm_name, start_alg = None, start_it = None, random_or_K = None):
    """
    Visualize how the K value improves during the iterations
    """

    fig = plt.figure(figsize=(20,20))
    plt.plot(all_opt_K.keys(), all_opt_K.values())
    plt.xlabel('iterations', fontsize = 20)
    plt.ylabel('K', fontsize = 20)
    
    if algorithm_name == 'Hillclimber':
        if start_alg.upper() == "R":
            start_alg = "Random"
        else:
            start_alg = "Greedy"
        
        if random_or_K.upper() == "R":
            random_or_K = "Random Traject"
        else:
            random_or_K = "Traject with lowest K"
        fig.suptitle(f"Improvement of K after {len(all_opt_K.keys())} iterations using {algorithm_name} algorithm \n \
        start state generated by {start_alg} (n = {start_it}) and {random_or_K} removed", fontsize = 25, y = 0.93)
    else:
        fig.suptitle(f"Improvement of K after {len(all_opt_K.keys())} iterations using {algorithm_name} algorithm", fontsize = 25, y = 0.93)
    
    fig.savefig(f"plots/Opt_K_Improvement_{algorithm_name}")


def visualise_opt_K_all_algorithms(opt_K_random, opt_K_greedy, opt_K_hillclimber, prefer_unused_connections, start_alg, start_it, random_or_K):
    """
    Visualize how the optimal K compares for all algorithms after n iterations
    """
    
    fig = plt.figure(figsize=(20,20))
    plt.plot(opt_K_random.keys(), opt_K_random.values(), color = 'blue', label = 'random')
    plt.plot(opt_K_greedy.keys(), opt_K_greedy.values(), color = 'green', label = 'greedy')
    if start_alg.upper() == "R":
        start_alg = "Random"
    else:
        start_alg = "Greedy"
    if random_or_K.upper() == "R":
        random_or_K = "Random Traject"
    else:
        random_or_K = "Traject with lowest K"
    plt.plot(opt_K_hillclimber.keys(), opt_K_hillclimber.values(), color = 'red', label = f'hillclimber ({start_alg} start (n = {start_it}), {random_or_K} removed)')
    plt.xlabel('iterations', fontsize = 20)
    plt.ylabel('K', fontsize = 20)
    plt.legend(title = 'Algorithm')

    if prefer_unused_connections:
        heuristic = ''
    else:
        heuristic = ' not'

    fig.suptitle(f"Improvement of K after {len(opt_K_random.keys())} iterations, unused connections{heuristic} preferred", fontsize = 25, y = 0.93)
    fig.savefig("plots/All_K_Improvement")

def visualise_K_distribution_comparison(all_K_random, all_K_greedy, all_K_hillclimber, prefer_unused_connections, start_alg, start_it, random_or_K, sim_anneal, lin_or_exp):
    """
    Visualize the distribution of K in a histogram for all algorithms.
    """
    fig = plt.figure(figsize=(20,20))
    plt.hist(all_K_random, bins = 250, color = 'blue', label = 'random', alpha = 0.5)
    plt.hist(all_K_greedy, bins = 250, color = 'green', label = 'greedy', alpha = 0.5)

    alg_choice_name = ""
    traject_choice_name = ""
    hc_sa_filename = "hillclimber"
    hillclimber_or_sim_annealing = "hillclimber"

    if start_alg.upper() == "R":
        alg_choice_name = "Random"
    else:
        alg_choice_name = "Greedy"
    if random_or_K.upper() == "R":
        traject_choice_name = "Random Traject"
    else:
        traject_choice_name = "Traject with lowest K"

    if sim_anneal.upper() == "Y" or sim_anneal.upper() == "YES":
        if lin_or_exp.upper() == "L":
            hillclimber_or_sim_annealing = "simulated annealing, linear"
            hc_sa_filename = "sim_anneal_lin"
        elif lin_or_exp.upper() == "E":
            hillclimber_or_sim_annealing = "simulated annealing, exponential"
            hc_sa_filename = "sim_anneal_exp"

    if prefer_unused_connections:
        heuristic = ''
    else:
        heuristic = ' not'
    
    plt.hist(all_K_hillclimber, bins = 250, color = 'red', label = f'{hillclimber_or_sim_annealing} ({alg_choice_name} start (n = {start_it}), {traject_choice_name} removed)', alpha = 0.5)
    plt.xlabel('K', fontsize = 20)
    plt.ylabel('frequency', fontsize=20)
    plt.xticks(fontsize= 10)
    plt.legend(title = 'Algorithm')
    fig.suptitle(f"Frequency Histogram of K for all algorithms \n (n= {len(all_K_random)}), unused connections{heuristic} preferred", fontsize=25, y = 0.93)
    
    # save a new image if variables are changed
    fig.savefig(f"plots/steekproef_all_{hc_sa_filename}_{start_alg}_start_{random_or_K}_traject")
    if os.path.exists(f"plots/steekproef_all_{hc_sa_filename}_{start_alg}_start_{random_or_K}_traject"):
        fig.savefig(f"plots/steekproef_all_{hc_sa_filename}_{start_alg}_start_{random_or_K}_traject")

