class Trajectory:

    def __init__(self, stations, duration, connections):
        self.stations = stations
        self.duration = duration
        self.connections = connections
    
    def update_trajectory(self, new_station, extra_time, connection, max_duration):
        """
        Add connection to trajectory if possible within time constraint.
        Return boolean to indicate whether succeeded or not.
        """
        if self.duration + extra_time < max_duration:
            self.stations = self.stations + [new_station]
            self.duration = self.duration + extra_time
            self.connections = self.connections + [connection]
            return True
        else:
            return False
    
    def __eq__(self, other):

        # two trajectories are equal if they contain connections in the same order
        if self.connections == other.connections:
            return True
        # or if one trajectory is the reverse of the other trajectory
        elif list(reversed(self.connections)) == other.connections:
            return True
        else:
            return False
