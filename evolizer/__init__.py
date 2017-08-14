
import random

class Individual(object):

    def __init__(self, param_choices=None):
        # store all possible parameters
        self.param_choices = param_choices
        # Create a random individual
        self.params = {}
        # add hardcoded parameters
        self.param_choices['fertility'] = range(1,10)
        # random choice for every parameter
        for key in self.param_choices:
            self.params[key] = random.choice(self.param_choices[key])

    def __repr__(self):
        return "<{}(fitness={}, fertility={})>".format(
            self.__class__.__name__,
            self.fitness(),
            self.params['fertility']
        )

    def live(self):
        """use self.params to live"""
        pass

    def fitness(self):
       """determine fitness of this individual"""
       raise NotImplementedError("we need a fitness() function")

    def mutate(self):
        """Randomly mutate individual."""

        # Choose a random key.
        mutation = random.choice(list(self.param_choices.keys()))
        # Mutate one of the params.
        self.params[mutation] = random.choice(self.param_choices[mutation])

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
        for _ in range(mother.params['fertility']):

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

    def optimize(self, individuals, generations=100):
        # evolve all generations
        for g in xrange(generations):

            # evaluate current population
            for i in individuals:
                # let the individual live a life according to its parameters
                i.live()

            print self.avg_fitness(individuals)

            # Evolve, except on the last iteration.
            if g != generations - 1:
                individuals = self.evolve(individuals)

        # last generation
        return individuals

    @staticmethod
    def avg_fitness(population):
        return sum(map(lambda x: x.fitness(), population)) / len(population)
