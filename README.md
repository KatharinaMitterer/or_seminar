#Urban Ridesharing Problem with Stochastic Travel Times: Simheuristic Approach

This repository contains an implementation of a simheuristic approach for solving the urban ridesharing problem with stochastic travel times, as described in the paper "Solving an urban ridesharing problem with stochastic travel times: A simheuristic approach" by Leandro do C. Martins, Angel A. Juan, Maria Torres, Elena Perez-Bernabeu, Canan G. Corlu, and Javier Faulin, presented at the Winter Simulation Conference 2021.

#Overview

The urban ridesharing problem involves finding optimal routes for a set of riders who wish to travel from their origin to their destination using a shared vehicle. This problem is complicated by the stochastic nature of travel times in urban environments, which can be affected by traffic congestion, accidents, and other factors.

The simheuristic approach used in this implementation combines simulation and metaheuristics to generate near-optimal solutions for the urban ridesharing problem. The approach includes a set of heuristics for generating initial solutions, as well as a simulated annealing algorithm for optimizing those solutions.


#Results

This study aimed to solve the urban ridesharing problem with stochastic travel times using a simheuristic approach and compare the results with those of Martins et al. (2021). Twenty problem instances were generated, ten of which had six vehicles, two destinations, and 64 pick-up points. The remaining ten problem instances had 12 vehicles, four destinations, and 200 pick-up points or 24 vehicles, eight destinations, and 500 pick-up points. The simheuristic approach involved solving the deterministic version of the problem, then testing the solution through 100 simulations with stochastic travel times, using a multi-start approach. The results showed an improvement in average reward of 3.19%, 4.17%, and 5.64% for the problem instances with six, twelve, and 24 vehicles, respectively, compared to the deterministic approach. In contrast, the deterministic approach was more reliable for the problem instances with six vehicles. The comparison with Martins et al. (2021) showed a lower improvement in average reward for the problem instances with six vehicles in this study.

#Acknowledgments

This implementation was developed as part of my seminar thesis for the Institute of Discrete Optimization and Logistics at KIT. The implementation is based on the simheuristic approach described in the paper "Solving an urban ridesharing problem with stochastic travel times: A simheuristic approach" by Leandro do C. Martins, Angel A. Juan, Maria Torres, Elena Perez-Bernabeu, Canan G. Corlu, and Javier Faulin, presented at the Winter Simulation Conference 2021.


