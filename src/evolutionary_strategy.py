"""
Module that implements the evolutionary strategy.
"""

import random


class Candidate:
    """
    A candidate that is used in the evolutionary strategy.
    
    In the context of the current implementation of the strategy, a candidate has an array of weights, each of which is
    in the range of [0.0, 1.0]. Each weight represents an offset to be added to the middle racing line (the line at the
    exact mid point of the left and right track limits). A value of 0.0 represents moving the vertex toward the left
    track limit, while a value of 1.0 represents moving it toward the right track limit and 0.5 has the vertex staying
    at the center.
    """
    
    def __init__(self, weights=None):
        """
        Method to initialize the candidate.

        Args:
            weights(list): List of weights, each of which is in the range [0, 1]. Defaults to None.

        """
        self.weights = weights if weights else []


class EvolutionaryStrategy:
    """
    The module implementing the evolutionary strategy.
    """
    
    def __init__(self, left_limit, right_limit, population_size=50, iterations=5):
        """
        Method to initialize the evolutionary strategy.

        Args:
            left_limit(RacingLine): Left side track limit.
            right_limit(RacingLine): Right side track limit.
            population_size(int): Size of the population to be used. Defaults to 50.
            iterations(int): Number of iterations to run the algorithm for. Defaults to 5.

        """
        self.right_limit = right_limit
        self.left_limit = left_limit
        self.population_size = population_size
        self.iterations = iterations
        self.population = []

    def generate_population(self):
        """
        Method to generate the population for the solution set.
        """
        population = []
        for _ in range(len(self.population_size)):
            weights = [random.uniform(0.0, 1.0) for _ in self.left_limit.vertices]
            population.append(Candidate(weights))
        
        self.population = population
