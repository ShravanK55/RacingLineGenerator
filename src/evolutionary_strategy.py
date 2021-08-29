"""
Module that implements the evolutionary strategy.
"""

import numpy
import random

from constants import REFERENCE_FITNESS
from lap_time_calculator import LapTimeCalculator
from racing_line import RacingLine
from utils import clamp


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
        self.lap_time = -1

    @property
    def fitness(self):
        """
        Method to get the fitness of a candidate.
        """

        if (self.lap_time):
            return REFERENCE_FITNESS - self.lap_time

        lap_time_calculator = LapTimeCalculator()
        lap_time_calculator.calculate_lap_time(RacingLine.generate_from_weights(self.weights))


class EvolutionaryStrategy:
    """
    The module implementing the evolutionary strategy.
    """

    def __init__(self, left_limit, right_limit, weight_group_size=20, population_size=50, iterations=5,
                 num_offspring=50, mutation_factor=0.5, standard_deviation=0.3):
        """
        Method to initialize the evolutionary strategy.

        Args:
            left_limit(RacingLine): Left side track limit.
            right_limit(RacingLine): Right side track limit.
            weight_group_size(int): Number of weights to group together. Defaults to 20.
            population_size(int): Size of the population to be used. Defaults to 50.
            iterations(int): Number of iterations to run the algorithm for. Defaults to 5.
            num_offspring(int): Number of offspring to generate each generation. Defaults to 50.
            mutation_factor(float): Factor by which the offspring are to be mutated. Defaults to 0.5.
            standard_deviation(float): Standard deviation to use when constructing the path vector. Defaults to 0.3.

        """
        self.right_limit = right_limit
        self.left_limit = left_limit
        self.weight_group_size = weight_group_size
        self.population_size = population_size
        self.iterations = iterations
        self.population = []
        self.num_offspring = num_offspring
        self.mutation_factor = mutation_factor
        self.standard_deviation = standard_deviation

    def generate_population(self):
        """
        Method to generate the population for the solution set.

        Returns:
            population(list): List of Candidates in the population.

        """
        population = []
        for _ in range(self.population_size):
            weights = [random.uniform(0.0, 1.0) for _ in self.left_limit.vertices]
            population.append(Candidate(weights))

        self.population = population
        return population

    def generate_offspring(self):
        """
        Method to generate the offspring for the population.

        Returns:
            offspring(list): List of offspring Candidates that were generated by mutating the parents.

        """
        offspring = []

        for _ in range(len(self.num_offspring)):
            idx = numpy.random(0, len(self.population))
            parent = self.population[idx]
            path_vector = numpy.random.normal(0.0, self.standard_deviation, len(parent.weights))
            mutated_vector = [weight * self.mutation_factor for weight in path_vector]
            offspring_weights = []

            for w_idx in range(len(parent.weights)):
                offspring_weight = clamp(parent.weights[w_idx] + mutated_vector[w_idx], 0.0, 1.0)
                offspring_weights.append(offspring_weight)

            new_candidate = Candidate(offspring_weights)
            offspring.append(new_candidate)

        self.population.extend(offspring)
        return offspring

    def perform_selection(self):
        """
        Method to perform selection of candidates in the population.
        """
        pass

