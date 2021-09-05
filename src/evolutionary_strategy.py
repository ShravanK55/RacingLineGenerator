"""
Module that implements the evolutionary strategy.
"""

import random

import numpy as np
from scipy.signal import savgol_filter

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
        self.lap_time = None

    @property
    def fitness(self):
        """
        Gets the fitness of the Candidate.
        NOTE: The fitness is equal to the lap time of the candidate. The lower the fitness, the better the solution.

        Returns:
            lap_time(float): Lap time of the car in seconds.

        """
        return self.lap_time


class EvolutionaryStrategy:
    """
    The module implementing the evolutionary strategy.
    """

    def __init__(self, left_limit, right_limit, car, starting_velocity=0.0, weight_group_size=20, smoothing_length=9,
                 smoothing_order=1, population_size=50, iterations=5, num_offspring=50, mutation_factor=0.5,
                 standard_deviation=0.3):
        """
        Method to initialize the evolutionary strategy.

        Args:
            left_limit(RacingLine): Left side track limit.
            right_limit(RacingLine): Right side track limit.
            car(Car): Car to evaluate the racing line for.
            starting_velocity(float): Starting velocity of the car in m/s. Defaults to 0.0 m/s.
            weight_group_size(int): Number of weights to group together. Defaults to 20.
            smoothing_length(int): Length of weights to smoothen at the ends of each weight group. Defaults to 9.
            smoothing_order(int): Order of interpolation to use for smoothing. Defaults to 1 (Linear).
            population_size(int): Size of the population to be used. Defaults to 50.
            iterations(int): Number of iterations to run the algorithm for. Defaults to 5.
            num_offspring(int): Number of offspring to generate each generation. Defaults to 50.
            mutation_factor(float): Factor by which the offspring are to be mutated. Defaults to 0.5.
            standard_deviation(float): Standard deviation to use when constructing the path vector. Defaults to 0.3.

        """
        self.right_limit = right_limit
        self.left_limit = left_limit
        self.car = car
        self.starting_velocity = starting_velocity
        self.weight_group_size = weight_group_size
        self.smoothing_length = smoothing_length
        self.smoothing_order = smoothing_order
        self.population_size = population_size
        self.iterations = iterations
        self.population = []
        self.num_offspring = num_offspring
        self.mutation_factor = mutation_factor
        self.standard_deviation = standard_deviation
        self.candidate_length = len(self.left_limit.vertices)

    def generate_population(self):
        """
        Method to generate the population for the solution set.

        Returns:
            population(list): List of Candidates in the population.

        """
        population = []
        for _ in range(self.population_size):
            # Creating weights in groups.
            weights = []
            for _ in range(0, len(self.left_limit.vertices), self.weight_group_size):
                weights.extend([random.uniform(0.0, 1.0)] * self.weight_group_size)

            # Smoothening weights using the Savitzsky-Golay filter (cubic).
            if self.smoothing_length > 0:
                weights = list(savgol_filter(weights, self.smoothing_length, self.smoothing_order))

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

        for _ in range(self.num_offspring):
            idx = np.random.randint(0, self.population_size)
            parent = self.population[idx]
            path_vector = []

            # Generating the path vector from normally distributed values for every weight group.
            for _ in range(0, len(parent.weights), self.weight_group_size):
                delta_weights = list(np.random.normal(0.0, self.standard_deviation, 1)) * self.weight_group_size
                path_vector.extend(delta_weights)

            mutated_vector = [weight * self.mutation_factor for weight in path_vector]
            offspring_weights = []

            for w_idx in range(len(parent.weights)):
                offspring_weight = clamp(parent.weights[w_idx] + mutated_vector[w_idx], 0.0, 1.0)
                offspring_weights.append(offspring_weight)

            # Smoothening weights using the Savitzsky-Golay filter (cubic).
            if self.smoothing_length > 0:
                offspring_weights = list(savgol_filter(offspring_weights, self.smoothing_length, self.smoothing_order))

            new_candidate = Candidate(offspring_weights)
            offspring.append(new_candidate)

        self.population.extend(offspring)
        return offspring

    def calculate_fitness(self, candidate):
        """
        Method to evaluate the fitness of a candidate. In this case, the lower the fitness, the better it is.

        Args:
            candidate(Candidate): Candidate to evaluate the fitness for.

        Returns:
            fitness(float): Fitness of the candidate.

        """
        if (candidate.fitness):
            return candidate.fitness

        line = RacingLine.generate_from_weights(candidate.weights, self.left_limit, self.right_limit)
        lap_time_calculator = LapTimeCalculator()
        candidate.lap_time = lap_time_calculator.calculate_lap_time(line, self.car, self.starting_velocity)
        return candidate.fitness

    def perform_selection(self):
        """
        Method to perform selection of Candidates in the population. The selection method is the Roulette-Wheel
        selection.

        Returns:
            population(list): List of Candidates after performing selection.

        """
        for candidate in self.population:
            self.calculate_fitness(candidate)

        population_fitness = sum([candidate.fitness for candidate in self.population])
        probabilities = [candidate.fitness / population_fitness for candidate in self.population]

        # Taking the complement of the probabilities as we have to minimize the lap time.
        probabilities = 1 - np.array(probabilities)
        probabilities = probabilities / probabilities.sum()

        print("Best (Min) Fitness: {}".format(min([candidate.fitness for candidate in self.population])))
        print("Average Fitness: {}".format(population_fitness / len(self.population)))

        self.population = list(np.random.choice(self.population, size=self.population_size, replace=False,
                                                p=probabilities))
        return self.population

    def run(self):
        """
        Method to run the strategy.

        Returns:
            best_candidate(Candidate): Candidate with the best fitness (least lap time) in the final population.

        """
        self.generate_population()

        for generation in range(self.iterations):
            print("Generation {}".format(generation))
            self.generate_offspring()
            self.perform_selection()
            print("")

        best_candidate = self.population[0]
        for idx in range(1, self.population_size):
            # Select the candidate with the least lap time.
            if (self.population[idx].fitness < best_candidate.fitness):
                best_candidate = self.population[idx]

        print("Best fitness after running the algorithm: {}".format(best_candidate.fitness))
        return best_candidate
