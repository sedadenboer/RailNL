# lines.py
#
# Minor Programmeren
# Bèta-Programma
#
# - Contains lines class to represent a line solution.
# - Methods and attributes: trajectories

class Lines():

    def __init__(self):
        self.trajectories = []

    def add_trajectory(self, trajectory):
        """
        Adds trajectory to line solution.
        """

        self.trajectories = self.trajectories + [trajectory]

    def __eq__(self, other):
        """
        Checks equiality of two line solutions.
        """

        # two line solutions are equal if they contain the same trajectories, order does not matter
        check_1 = all(item in self.trajectories for item in other.trajectories)
        check_2 = all(item in other.trajectories for item in self.trajectories)

        if check_1 and check_2:
            return True
        else:
            return False
