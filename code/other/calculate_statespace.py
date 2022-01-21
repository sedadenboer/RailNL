
import itertools
import math

def check_possible(seq, railway_map):

    duration = 0
    for connection in seq:
        duration += connection.duration 
    
    if duration > railway_map.max_duration:
        return False
    
    all_permutations = []
    for p in itertools.permutations(seq):
        if p[0] <= p[-1]:
            print('yes')

def state_space_cal(railway_map):

    # create dict with key = connection_id, value = duration
    connection_overview = dict()
    for connection in railway_map.available_connections:
        connection_overview[connection] = int(connection.duration)


    # find all combinations of connections which:
    # - sum is smaller than duration allowed at traject
    # - len is larger than 2 connections
    trajects = [seq for i in range(len(connection_overview), 0, -1)
               for seq in itertools.combinations(list(connection_overview.values()), i)
               if len(seq) > 2 and sum(seq) < railway_map.max_duration]

    ######################## to big to calculate #######################
    # # find all possible unique lijnvoeringen
    # # apply [n!/r!(n-r)!] as order = 0, repitition = 0 with n = len(trajects) and r = max_trajects
    # Nlijnvoeringen = math.factorial(len(trajects)) / \
    #                 (math.factorial(railway_map.max_trajects) * math.factorial(len(trajects) - railway_map.max_trajects))
    Nlijnvoeringen = 1

    return Nlijnvoeringen