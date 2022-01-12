
# GOAL: lijnvoering intercity treinen, zet aantal trajecten uit o.b.v. tijdsframe
#       lijnvoering = trajecten waarover de treinen gedurende de dag heen en weer rijden
#       traject     = route van sporen en stations waarover treinen heen en weer rijden, mag niet langer zijn dan tijdsframe
#           ex. traject = [Castricum , Zaandam , Hoorn , Alkmaar] is 59min, past binnen tijdsframe 60min

############################################ DEEL 1 (noord/zuid-holland) ############################################ 

# 1. Maak een lijnvoering voor Noord- en Zuid-Holland met maximaal zeven trajecten binnen een tijdsframe van twee uur, 
#    waarbij alle verbindingen bereden worden.

#    Kwaliteitsfunctie:    K = p*10000 - (T*100 + Min)
#    p   = fractie van de bereden verbindingen (dus tussen 0 en 1)
#    T   = aantal trajecten
#    Min = aantal minuten in alle trajecten samen

# 2. Maak wederom een lijnvoering voor Noord- en Zuid-Holland met maximaal zeven trajecten binnen een tijdsframe van twee uur, 
#    en probeer nu K zo hoog mogelijk te krijgen.


import pandas as pd
import matplotlib.pyplot as plt

class Station:

  def __init__(self, connections, x_coord, y_coord):

    # dict formatted as connections['connected station'] = duration
    self.connections = connections

    # x- and y-coordinates of station as floats
    self.x_coord = x_coord
    self.y_coord = y_coord


def main():

    ###################################### 1. Import Data ######################################
    # import data into pandas dataframe
    df_connections = pd.read_csv("Data_Holland/ConnectiesHolland.csv")
    df_stations = pd.read_csv("Data_Holland/StationsHolland.csv")
    
    ################################ 2. Create Station Objects ##################################
    # dict formatted as stations['name station'] = Station object
    stations = {}

    # loop over all North- and South-Holland intercity stations
    for i_1 in df_stations.index:

        # retrieve initial station information
        name = df_stations['station'][i_1]
        x_coord = df_stations['x'][i_1]
        y_coord = df_stations['y'][i_1]

        # create dict of connections formatted as connections['connected station'] = duration
        connections = {}
        for i_2 in df_connections.index:
            if df_connections['station1'][i_2] == name:
                connections[df_connections['station2'][i_2]] = df_connections['distance'][i_2]
            elif df_connections['station2'][i_2] == name:
                connections[df_connections['station1'][i_2]] = df_connections['distance'][i_2]

        # create Station object and add to main dict
        station_object = Station(connections, x_coord, y_coord)
        stations[name] = station_object
    
    ############################## 3. Visualization Railway Network ################################
    # retrieve initial information of intercity stations
    x = df_stations['x']
    y = df_stations['y']
    z = df_stations['station']

    # create scatterplot of based on x- and y-coord of stations
    plt.figure(figsize=(30, 20))
    plt.scatter(y, x, c = 'black', s = 15)

    # add station name to each scatter plot point
    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]), textcoords="offset points", xytext=(0, 10))

    # plot all connections between stations 
    for i in df_connections.index:

        # retrieve initial information of all connections
        station1 = df_connections['station1'][i]
        station2 = df_connections['station2'][i]
        duration = df_connections['distance'][i]

        # retrieve related Station objects of two stations
        station1_object = stations[station1]
        station2_object = stations[station2]
        
        # plot connection between Stations
        plt.plot([station1_object.y_coord, station2_object.y_coord], [station1_object.x_coord, station2_object.x_coord], 
                 c = 'black', alpha = 0.25)
        
        # add duration of connection
        plt.annotate(duration, ((station1_object.y_coord + station2_object.y_coord)/2,(station1_object.x_coord + station2_object.x_coord)/2), 
                    textcoords="offset points", xytext=(0,10), ha='center')

    # add titles to plot of Railway Network and remove x- and y-tics
    plt.suptitle("Intercity connections North- and South-Holland", fontsize=25, y = 0.93)
    plt.title('Duration in minutes', fontsize=18, y = 1.01)
    plt.xticks([], [])
    plt.yticks([], [])

    # save figure
    plt.savefig('Stations_Holland')

if __name__ == "__main__":
    main()

