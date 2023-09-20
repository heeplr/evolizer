#!/usr/bin/env python3

from evolizer import Individual, Evolver


class KnapSack(Individual):
    MAX_WEIGHT = 50
    # all possible items and their values
    PARAM_CHOICES = {
        1: [ { 'weight': 10, 'value': 60 }, {} ],
        2: [ { 'weight': 20, 'value': 100 }, {} ],
        3: [ { 'weight': 30, 'value': 120 }, {} ]
    }

    def fitness(self, score=None):
        """grade sack"""
        total_weight = sum([
            item['weight'] if 'weight' in item else 0 for item in self.params.values()
        ])
        total_value = sum([
            item['value'] if 'value' in item else 0 for item in self.params.values()
        ])
        # too heavy?
        if total_weight > KnapSack.MAX_WEIGHT:
            return 0
        # value is our score
        return total_value


if __name__ == '__main__':
    generations = 200  # Number of times to evole/breed the population.
    population = 10  # Number of individuals in each generation.

    # create initial population
    individuals = []
    for i in range(population):
        individuals += [ KnapSack() ]
    # create evolver
    evolver = Evolver(retain=0.4, lucky_chance=0.1, mutate_chance=0.5)

    # run evolver
    individuals = evolver.optimize(individuals, generations)
