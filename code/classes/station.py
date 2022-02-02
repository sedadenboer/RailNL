# station.py
#
# Minor Programmeren
# Bèta-Programma
#
# - Contains station class to represent a station.
# - Methods and attributes: name, x and y coordinates, connections

class Station():

    def __init__(self, name, x_coord, y_coord):

        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.connections = {}

    def add_connection(self, connection, neighbour):
        """
        Adds connection to a station.
        """

        self.connections[connection] = neighbour

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """

        return self.name