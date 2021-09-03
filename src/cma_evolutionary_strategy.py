"""
Module that implements the CMA evolutionary strategy.
"""

import numpy as np

from evolutionary_strategy import EvolutionaryStrategy


class CMAEvolutionaryStrategy(EvolutionaryStrategy):
    """
    The module implementing the CMA evolutionary strategy.
    References: https://en.wikipedia.org/wiki/CMA-ES, https://arxiv.org/pdf/1604.00772.pdf
    """

    def __init__(self, left_limit, right_limit, car, starting_velocity=0.0, weight_group_size=20, smoothing_length=9,
                 smoothing_order=1, population_size=50, iterations=5, standard_deviation=0.3):
        """
        Method to initialize the CMA evolutionary strategy.

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
            standard_deviation(float): Standard deviation to use when constructing the path vector. Defaults to 0.3.

        """
        super(CMAEvolutionaryStrategy, self).__init__(
            left_limit=left_limit, right_limit=right_limit, car=car, starting_velocity=starting_velocity,
            weight_group_size=weight_group_size, smoothing_length=smoothing_length, smoothing_order=smoothing_order,
            population_size=population_size, iterations=iterations, standard_deviation=standard_deviation)

        self.population_matrix = np.array()
        self.means = np.array()
        self.covariance_matrix = np.array()
        self.num_parents = self.population_size / 2

    def generate_population(self):
        """
        Method to generate the population for the solution set.

        Returns:
            population(list): List of Candidates in the population.

        """
        super(CMAEvolutionaryStrategy, self).generate_population()
        self.population_matrix = np.array([candidate.weights for candidate in self.population])
        self.means = self.population_matrix.sums(axis=0) / float(self.population_size)
        self.covariance_matrix = self._generate_covariance_matrix()
        return self.population

    def run(self):
        """
        Method to run the strategy.

        Returns:
            best_candidate(Candidate): Candidate with the best fitness (least lap time) in the final population.

        """
        pass

    def _generate_empirical_covariance_matrix(self):
        """
        Method to generate the empirical covariance matrix for a population.

        Returns:
            covariance_matrix(np.array): Covariance matrix for the population.

        """
        cols = len(self.population_matrix[0])
        covariance_matrix = np.array([[0.0] * cols] * cols)
        column_sums = self.population_matrix.sum(axis=0)
        column_sums = np.reshape(column_sums, (-1, 1)).transpose()

        for row in self.population_matrix:
            mat_row = np.reshape(row, (-1, 1)).transpose()
            bracket = mat_row - (1.0 / self.population_size) * column_sums
            bracket = bracket.transpose()
            covariance_matrix = covariance_matrix + (bracket.dot(bracket.transpose()))

        self.covariance_matrix = 1.0 / (self.population_size - 1) * covariance_matrix
        return self.covariance_matrix
