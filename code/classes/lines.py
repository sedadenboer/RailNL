import collections

class Lijnvoering():
    
    def __init__(self):
        self.trajecten = []

    def add_traject(self, traject):
        self.trajecten = self.trajecten + [traject]
    
    def __eq__(self, other):

        # two lijnvoeringen are equal if they contain the same trajecten, order does not matter
        check_1 = all(item in self.trajecten for item in other.trajecten)
        check_2 = all(item in other.trajecten for item in self.trajecten)

        if check_1 and check_2:
            return True
        else:
            return False
       