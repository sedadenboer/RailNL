import csv

from .station import Station
from .connection import Connection
from .traject import Traject
from .lijnvoering import Lijnvoering


class Graph():
    def __init__(self, source_map, max_trajects, max_duration):
        self.stations = self.load_stations(source_map)
        self.available_connections = []
        self.load_connections(source_map)
        self.max_trajects = max_trajects
        self.max_duration = max_duration
        self.used_connections = []
        self.unused_connections = set(self.available_connections) - set(self.used_connections)
        self.lijnvoering = Lijnvoering()
        self.K = 0
    

    def __eq__(self, other):
        return self.age == other.age

    def load_stations(self, source_map):
        """
        Load all the stations into the graph.
        """
        stations = {}
        source_file = f"data/{source_map}/Stations{source_map}.csv"
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                stations[row['station']] = Station(row['station'], row['x'], row['y'])

        return stations

    def load_connections(self, source_map):
        """
        Load all the connections into the loaded stations.
        """
        source_file = f"data/{source_map}/Connecties{source_map}.csv"
        id = 0
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                id += 1
                connection = Connection(id, row['station1'], row['station2'], row['distance'])
                self.available_connections.append(connection)
                self.stations[row['station1']].add_connection(connection, row['station2'])
                self.stations[row['station2']].add_connection(connection, row['station1'])

    def add_connection(self, connection):
        """
        Update connections used and not-used based on added connection.
        """
        self.used_connections = self.used_connections + [connection]
        self.unused_connections = set(self.available_connections) - set(self.used_connections)
    
    def lijnvoering_kwaliteit(self, used_connections, all_connections, lijnvoering):
        """
        Calculate the quality of the lijnvoering.
        """
        # fraction of ridden connections
        p = len(used_connections) / len(all_connections)
        # number of trajectories
        T = len(lijnvoering)
        # number of minutes of all trajectories together
        Min = 0
        for traject in lijnvoering:
            Min += traject.duration

        # calculate K
        self.K = p * 10000 - (T * 100 + Min)
