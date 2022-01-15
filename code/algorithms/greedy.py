import copy

class Greedy:
    def __init__(self, graph, transmitters):
        self.graph = copy.deepcopy(graph)
        self.transmitters = transmitters
    
    ## zodat jein de main algorhtme.run kan doen; genereert zo oplossing
    def run(self):
        nodes = list(self.graph.nodes.values())

        node_possibilities = self.transmitters

        # Repeat until no more possible solution or we've assigned all nodes
        while nodes or not node_possibilities:
            # NOTE: implement method
            node = self.get_next_node()

            node_possibilities = node.get_possibilities