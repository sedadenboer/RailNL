# graph.py
#
# Minor Programmeren
# Bèta-Programma
#
# - Contains graph class to represent a line solution graph.
# - Loads all stations and connections and their properties.
# - Methods and attributes: stations (+ properties), connections (+ properties), calculation of K

import csv
from .station import Station
from .connection import Connection
from .lines import Lines


class Graph():

    def __init__(self, source_map, max_trajectories, max_duration):

        # upload stations and connections
        self.stations = self.load_stations(source_map)
        self.available_connections = []
        self.load_connections(source_map)
        # upload case-specific information
        self.max_trajectories = max_trajectories
        self.max_duration = max_duration
        # keep track of used connections and visited stations
        self.used_connections = set()
        self.unused_connections = set(self.available_connections) - set(self.used_connections)
        self.visited_stations = set()
        # save result
        self.lines = Lines()
        self.K = 0

    def load_stations(self, source_map):
        """
        Load all the stations into the graph.
        """

        stations = {}
        source_file = f"data/{source_map}/Stations{source_map}.csv"

        # read source file
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                # load stations
                stations[row['station']] = Station(row['station'], row['x'], row['y'])

        return stations

    def load_connections(self, source_map):
        """
        Load all the connections into the loaded stations.
        """

        source_file = f"data/{source_map}/Connecties{source_map}.csv"
        id = 0

        # read source file
        with open(source_file, 'r') as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                # update id, load connections and update properties
                id += 1
                connection = Connection(id, row['station1'], row['station2'], row['distance'])
                self.available_connections.append(connection)
                self.stations[row['station1']].add_connection(connection, row['station2'])
                self.stations[row['station2']].add_connection(connection, row['station1'])

    def update_variables(self):
        """
        Update connections used and not-used and visited stations based on added connection.
        """

        stations = []
        connections = []

        # create lists with all stations and connections
        for trajectory in self.lines.trajectories:
            stations += trajectory.stations
            connections += trajectory.connections

        # update variables and transform to set
        self.used_connections = set(connections)
        self.unused_connections = set(self.available_connections) - self.used_connections
        self.visited_stations = set(stations)

    def add_connection(self, connection):
        """
        Update connections used and not-used and visited stations based on added connection.
        """

        self.used_connections.add(connection)
        self.unused_connections = set(self.available_connections) - self.used_connections
        [station1, station2] = connection.stations
        self.visited_stations.add(station1)
        self.visited_stations.add(station2)

    def lines_quality(self, used_connections, all_connections, lines):
        """
        Calculate the quality of the lines.
        """

        # fraction of ridden connections
        p = len(used_connections) / len(all_connections)
        # number of trajectories
        T = len(lines)
        # number of minutes of all trajectories together
        Min = 0
        for trajectory in lines:
            Min += trajectory.duration

        # calculate K
        self.K = p * 10000 - (T * 100 + Min)
