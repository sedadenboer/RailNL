from matplotlib import pyplot as plt

def visualise_start(railway_map, map_name):
    """
    Visualisation code that displays the railnetwork of the selected area
    """
    print("Loading main visualisation...")
    print()
    
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


def visualise_solution(final_graph, map_name):
    """
    Visualisation code that displays the found 'lijnvoering'
    """
    print("Loading solution visualisation...")
    print()

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
    if len(final_graph.lijnvoering) > 6:
        fig = plt.figure(figsize=(70, 70))
    else:
        fig = plt.figure(figsize=(70, 40))

    # create subplot for each traject
    n_trajects = 1
    fig.subplots_adjust(hspace=0.4, wspace=0.2)

    for traject in final_graph.lijnvoering:
        
        # determine dimensions of figure based on number of trajects
        if len(final_graph.lijnvoering) > 9:
            ax = fig.add_subplot(5, 4, n_trajects)
        elif len(final_graph.lijnvoering) > 6 and len(final_graph.lijnvoering) < 10:
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

    # add title and save figure
    fig.suptitle("Railnetwork generated by Random Algorithm", fontsize=45, y = 0.93)
    fig.savefig(f"docs/Stations_{map_name}_Random_Solution")