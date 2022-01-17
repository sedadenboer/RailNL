class Traject:

    def __init__(self, stations, duration, connections):
        self.stations = stations
        self.duration = duration
        self.connections = connections
    
    def update_traject(self, new_station, extra_time, connection, max_duration):
        """
        Add connection to traject if possible within time constraint.
        Return boolean to indicate whether succeeded or not.
        """
        if self.duration + extra_time < max_duration:
            self.stations = self.stations + [new_station]
            self.duration = self.duration + extra_time
            self.connections = self.connections + [connection]
            return True
        else:
            return False
