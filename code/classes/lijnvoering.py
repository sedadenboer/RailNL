class Lijnvoering:

    def __init__(self, connections, trajecten):
        self.connections = connections
        self.trajecten = trajecten
        self.unused_connections = set(range(0, 28))
    
    def add_traject(self, traject):
        self.trajecten = self.trajecten + [traject]
    
    def add_connection(self, connection):
        self.connections = self.connections + [connection]
        self.unused_connections = set(range(0, 28)) - set(self.connections)