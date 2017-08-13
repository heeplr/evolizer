#!/usr/bin/env python2

"""Entry point to evolving the neural network. Start here."""
import random

class Individual(object):

    def __init__(self, param_choices=None):
        # store all possible parameters
        self.param_choices = param_choices
        # Create a random individual
        self.params = {}
        # hardcoded parameters
        self.h_param_choices = {
            'fertility' : range(10)
        }
        self.h_params = {}
        # random choice for every parameter
        for key in self.param_choices:
            self.params[key] = random.choice(self.param_choices[key])
        for key in self.h_param_choices:
            self.h_params[key] = random.choice(self.h_param_choices[key])

    def __repr__(self):
        return "<{}(fitness={}, fertility={})>".format(
            self.__class__.__name__,
            self.fitness(),
            self.h_params['fertility']
        )

    def live(self):
        """use self.params to live"""
        pass

    def fitness(self):
       """determine fitness of this individual"""
       raise NotImplementedError("we need a fitness() function")

    def mutate(self):
        """Randomly mutate individual."""

        # 50/50 chance to mutate normal or hardcoded param
        if random.random() > 0.5:
            choices = self.param_choices
            params = self.params
        else:
            choices = self.h_param_choices
            params = self.h_params

        # Choose a random key.
        mutation = random.choice(list(choices.keys()))
        # Mutate one of the params.
        params[mutation] = random.choice(choices[mutation])

    @staticmethod
    def crossover(mother, father):
        """Make two children as parts of their parents.

        Args:
            mother (dict): Network parameters
            father (dict): Network parameters

        Returns:
            (list): Two network objects

        """
        children = []
        for _ in range(mother.h_params['fertility']):

            child_params = {}

            # Loop through the parameters and pick params for the kid.
            for param in mother.param_choices:
                child_params[param] = random.choice(
                    [mother.params[param], father.params[param]]
                )

            # Now create a new Indidvidual object.
            child = mother.__class__()
            child.params = child_params

            children += [ child ]

        return children

class Evolver(object):
    """genetic algorithm evolution helper class"""

    def __init__(self, retain=0.4,
                 random_select=0.1, mutate_chance=0.2):
        """:param retain (float): Percentage of population to retain after
                each generation
           :param random_select (float): Probability of a rejected network
                remaining in the population
           :param mutate_chance (float): Probability a network will be
                randomly mutated
        """
        self.mutate_chance = mutate_chance
        self.random_select = random_select
        self.retain = retain

    def evolve(self, population):
        """evolve one generation"""

        # Get scores for each network.
        graded = sorted(population, key=lambda i: i.fitness(), reverse=True)

        # Get the number we want to keep for the next gen.
        retain_length = int(len(graded)*self.retain)

        # Get the number we want to keep for the next gen.
        retain_length = int(len(graded)*self.retain)

        # The parents are every network we want to keep.
        parents = graded[:retain_length]

        # For those we aren't keeping, randomly keep some anyway.
        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents +=  [ individual ]

        # Randomly mutate some of the networks we're keeping.
        for individual in parents:
            if self.mutate_chance > random.random():
                individual.mutate()

        # Now find out how many spots we have left to fill.
        parents_length = len(parents)
        desired_length = len(population) - parents_length
        children = []

        # Add children, which are bred from two remaining networks.
        while len(children) < desired_length:

            # Get a random mom and dad.
            male = random.randint(0, parents_length-1)
            female = random.randint(0, parents_length-1)

            # Assuming they aren't the same network...
            if male != female:
                male = parents[male]
                female = parents[female]

                # Breed them.
                babies = Individual.crossover(male, female)

                # Add the children one at a time.
                for baby in babies:
                    # Don't grow larger than desired length.
                    if len(children) < desired_length:
                        children += [ baby ]

        # add children
        parents += children

        # sort by fitness
        parents = sorted(parents, key=lambda x: x.fitness(), reverse=True)

        return parents

    @staticmethod
    def avg_fitness(population):
        return sum(map(lambda x: x.fitness(), population)) / len(population)

class Candidate(Individual):
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

    def __init__(self):
        super(Candidate, self).__init__(Candidate.PARAM_CHOICES)

    def __repr__(self):
        return "<Candidate(fitness={}, fertility={}, msg=\"{}\")>".format(
            self.fitness(),
            self.h_params['fertility'],
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

    def fitness(self):
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

if __name__ == '__main__':
    generations = 1000  # Number of times to evole the population.
    population = 40  # Number of networks in each generation.

    # create population
    individuals = []
    for i in xrange(population):
        individuals += [ Candidate() ]

    # create evolver
    evolver = Evolver(retain=0.4, random_select=0.1, mutate_chance=0.2)

    # Evolve the generation.
    for g in xrange(generations):

        # evaluate current population
        for i in individuals:
            # let the individual live a life according to its parameters
            i.live()

        print evolver.avg_fitness(individuals)

        # Evolve, except on the last iteration.
        if g != generations - 1:
            individuals = evolver.evolve(individuals)

    # Print out the top 5 networks.
    print individuals[:5]
