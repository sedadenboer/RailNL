# RailNL
This project is part of the 'Programmeertheorie' course of the programming minor of the University of Amsterdam.

## Description
The organization of a trainnetwork is a very complex problem and can be solved with the help of AI-techniques. The goal of this project is to search for optimal line management solutions for the trainnetwork in the Dutch provinces North- and South-Holland and eventually the complete trainnetwork of The Netherlands. The focus here lays on the trajectories of intercity trains use during the day. This implies that there have to be created a couple of trajectories within a certain timeframe. In this case a trajectory is a route of tracks and stations on which trains can travel back and forth. Eventually the algorithm has to produce the most efficient line management solution as possible.

The former can be done with the help of the following equation:

`K = p * 1000 = (T * 100 + Min)`

`K` = quality of the line management

`p` = fraction of the ridden connections (number between 0 and 1)

`T` = the number of trajectories

`Min` = the number of minutes of all the trajectories taken together


## North- and South-Holland
For this assignment a line management solution has to be found for North- and South-Holland with max. 7 trajectories within a timeframe of 2 hours, and all connections have to be ridden. After this is done, this has to be done again but with the goal to optimize `K` for it to be as high as possible. In this case not all connections have to be ridden.

### State space
The state space of a problem is equal to the number of unique solutions. The following formula is used to calculate the state space: `(n!)/(r!(n-r)!)`, where in this problem r equals to the number of trajectories allowed and n equals to the number of unique trajectories. For the North- and South-Holland case, `r` = 7 and `n` = 10835519. Entering in these values into the formula, will give a state space in the order of 10^10^8.16. Because of the enormous size of the state space, the following restrictions are set to decrease this number:
- Teleportations are not allowed; a train has to continue from the last destination.
- A trajectory can't go over a connection or station more than once.
- A trajectory has to start at a connection that has not been used before in the line.
- A trajectory has to consist of at least 2 connections.
- All stations need to be visited in a line.

### Algorithm
Different algorithms will be used to find the optimal solution with the highest `K` value. 
A random algorithm has been implemented with the restrictions set above. This algorithm only takes these restrictions into account, all other choices are random. This algorithm is run 100.000 times and the solution with the highest `K` value from these runs is saved in a figure. From an experiment testing for uniqueness, it is known that these 100.000 solutions are almost guaranteed to be unique solutions. 
A greedy and hill climber algorithm will also be implemented and are currently being worked on.

## The Netherlands

### Algorithm

## Authors
* [@sedadenboer](https://www.github.com/sedadenboer)
* [@evapots](https://github.com/evapots)
* [@Thijmen1411](https://github.com/Thijmen1411)
