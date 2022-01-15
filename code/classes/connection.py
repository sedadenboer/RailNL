class Connection():
    def __init__(self, id, station1, station2, duration):

        self.id = id
        self.stations = [station1, station2]
        self.duration = duration

    def __repr__(self):
        """
        Make sure that the object is printed properly if it is in a list/dict.
        """
        return str(self.id)