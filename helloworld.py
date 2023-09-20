#!/usr/bin/env python3

from evolizer import Individual, Evolver


class HelloGreeter(Individual):
    PARAM_CHOICES = {
        '0': "abcdefghijklmnopqrstuvwxyz",
        '1': "abcdefghijklmnopqrstuvwxyz",
        '2': "abcdefghijklmnopqrstuvwxyz",
        '3': "abcdefghijklmnopqrstuvwxyz",
        '4' : "abcdefghijklmnopqrstuvwxyz",
        '5' : "abcdefghijklmnopqrstuvwxyz",
        '6' : "abcdefghijklmnopqrstuvwxyz",
        '7' : "abcdefghijklmnopqrstuvwxyz",
        '8' : "abcdefghijklmnopqrstuvwxyz",
        '9' : "abcdefghijklmnopqrstuvwxyz",
    }

    def __repr__(self):
        return "<HelloGreeter(fitness={}, msg=\"{}\")>".format(
            self.fitness(),
            self.params['0'] +
            self.params['1'] +
            self.params['2'] +
            self.params['3'] +
            self.params['4'] +
            self.params['5'] +
            self.params['6'] +
            self.params['7'] +
            self.params['8'] +
            self.params['9']
        )

    def fitness(self, score=None):
        neg_fitness = 0
        # calculate deviation from goal
        params = [
            self.params['0'],
            self.params['1'],
            self.params['2'],
            self.params['3'],
            self.params['4'],
            self.params['5'],
            self.params['6'],
            self.params['7'],
            self.params['8'],
            self.params['9']
        ]
        for a, b in zip("helloworld", params):
            neg_fitness += abs(ord(a) - ord(b))

        fitness = -neg_fitness

        # additional score for correct position
        if self.params['0'] == 'h': fitness += 2
        if self.params['1'] == 'e': fitness += 2
        if self.params['2'] == 'l': fitness += 2
        if self.params['3'] == 'l': fitness += 2
        if self.params['4'] == 'o': fitness += 2
        if self.params['5'] == 'w': fitness += 2
        if self.params['6'] == 'o': fitness += 2
        if self.params['7'] == 'r': fitness += 2
        if self.params['8'] == 'l': fitness += 2
        if self.params['9'] == 'd': fitness += 2

        return fitness

    def finished(self):
        """return true if we got perfect result"""
        return bool(all([
            self.params['0'] == 'h',
            self.params['1'] == 'e',
            self.params['2'] == 'l',
            self.params['3'] == 'l',
            self.params['4'] == 'o',
            self.params['5'] == 'w',
            self.params['6'] == 'o',
            self.params['7'] == 'r',
            self.params['8'] == 'l',
            self.params['9'] == 'd'
        ]))

if __name__ == '__main__':
    generations = 1000  # Number of times to evole/breed the population.
    population = 40  # Number of individuals in each generation.

    # create initial population
    individuals = []
    for i in range(population):
        individuals += [ HelloGreeter() ]

    # create evolver
    evolver = Evolver(retain=0.4, lucky_chance=0.1, mutate_chance=0.2)

    # run evolver
    individuals = evolver.optimize(individuals, generations)
