class Traject:

    def __init__(self, stations, duration, connections):
        self.stations = stations
        self.duration = duration
        self.connections = connections
    
    def update_traject(self, new_station, extra_time):
        if self.duration + extra_time < 120:
            self.stations = self.stations + [new_station]
            self.duration = self.duration + extra_time
            return True
        else:
            return False

    def add_connection(self, connection):
        self.connections = self.connections + [connection]