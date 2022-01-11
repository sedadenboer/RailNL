
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

    # connections['connected station'] = duration
    self.connections = connections
    # x/y-coordinates of station
    self.x_coord = x_coord
    self.y_coord = y_coord

def main():

    # import data 
    df_connections = pd.read_csv("Data_Holland/ConnectiesHolland.csv")
    df_stations = pd.read_csv("Data_Holland/StationsHolland.csv")

    # create plot of train network N/S-holland 
    x = df_stations['x']
    y = df_stations['y']
    z = df_stations['station']
    plt.figure(figsize=(30, 20))
    plt.scatter(y, x, c = ['black'], s = 15)

    for i, txt in enumerate(z):
        plt.annotate(txt, (y[i], x[i]))

    plt.title("Intercity connections North/South Holland", fontsize=25)
    plt.savefig('Stations_Holland')
    
    # list with objects of all stations of N/Z-holland
    stations = list()
    
    for i_1 in df_stations.index:
        # retrieve initial station information
        name = df_stations['station'][i_1]
        x_coord = df_stations['x'][i_1]
        y_coord = df_stations['y'][i_1]

        # find connections of station
        connections = {}
        for i_2 in df_connections.index:
            if df_connections['station1'][i_2] == name:
                connections[df_connections['station2'][i_2]] = df_connections['distance'][i_2]
            elif df_connections['station2'][i_2] == name:
                connections[df_connections['station1'][i_2]] = df_connections['distance'][i_2]

        # create station object and add to list
        name = Station(connections, x_coord, y_coord)
        stations.append(name)

if __name__ == "__main__":
    main()

