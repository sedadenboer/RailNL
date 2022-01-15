class Station():
    def __init__(self, name, x_coord, y_coord):

        self.name = name
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.connections = {}

    def add_connection(self, connection, neighbour):
        self.connections[connection] = neighbour

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return self.name