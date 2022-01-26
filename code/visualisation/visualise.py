from matplotlib import pyplot as plt
import numpy as np

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

def visualise_solution_new(final_graph, algorithm_name):
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
    plt.figure(figsize=(20, 30))
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
        plt.annotate(connection.id, ((y1 + y2) / 2,(x1 + x2) / 2), textcoords="offset points", xytext=(0,10), ha='center')

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
    plt.suptitle(f"Railnetwork generated by Random Algorithm (K = {str(round(final_graph.K, 2))}, p = {str(round(len(set(final_graph.used_connections))/len(final_graph.available_connections), 2))}) \n {final_graph.used_connections}", fontsize=25)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.axis('scaled')
    plt.legend()

    # create filename based on region and algorithm
    if final_graph.max_trajects == 7:
        file = 'results/' + str(algorithm_name) + '/Holland/visualisation'
    else:
        file = 'results/' + str(algorithm_name) + '/Nationaal/visualisation'

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

   
def visualise_opt_K_improvement(all_opt_K, algorithm_name):
    """
    Visualize how the K value improves during the iterations
    """

    fig = plt.figure(figsize=(20,20))
    plt.plot(all_opt_K.keys(), all_opt_K.values())
    plt.xlabel('iterations', fontsize = 20)
    plt.ylabel('K', fontsize = 20)

    fig.suptitle(f"Improvement of K after {len(all_opt_K.keys())} iterations using {algorithm_name} algorithm", fontsize = 25, y = 0.93)
    fig.savefig(f"plots/Opt_K_Improvement_{algorithm_name}")