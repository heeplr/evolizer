"""simple evolutionary optimizer"""

import random
import signal


class Individual(object):
    """one individual with a genotype and phenotype"""

    # the genome
    PARAM_CHOICES = {}
    param_choices = {}

    def __init__(self, param_choices=None, params={}):
        """
        :param param_choices: initial dictionary of parameter:possible_values
        :param params: initial dictionary of parameter:value (will be generated randomly if unset)
        """
        # store all possible parameters
        if self.PARAM_CHOICES:
            self.param_choices = { **self.param_choices, **self.PARAM_CHOICES }
        if param_choices:
            self.param_choices = { **self.param_choices, **param_choices }
        # place to remember params that were evaluated last so we don't
        # evaluate the same params twice
        self.evaluated_params = None
        # genotype of this individual
        self.params = params
        # got params already?
        if len(self.params) > 0:
            return
        # create new random genotype
        self.shuffle()

    def __repr__(self):
        return f"<{self.__class__.__name__}(fitness={self.fitness()}, params=\"{self.params}\")>"

    def live(self):
        """use self.params to live"""
        pass

    def fitness(self):
       """Returns fitness of this individual as float. The larger the fitter."""
       raise NotImplementedError("we need a fitness() function")

    def finished(self):
        """
        check if we can finish early
        :result: true if this individual is perfect, false to carry on
        """
        return False

    def mutate(self):
        """Randomly mutate individual."""

        # Choose a random key.
        mutation = random.choice(list(self.param_choices.keys()))
        # Mutate one of the params.
        self.params[mutation] = random.choice(self.param_choices[mutation])

    def shuffle(self):
        """create new random genome (params) from genes (param_choices)"""
        # random choice for every parameter
        for key in self.param_choices:
            self.params[key] = random.choice(self.param_choices[key])

    @staticmethod
    def crossover(mother, father):
        """Make two children as parts of their parents.

        Args:
            mother (dict): Network parameters
            father (dict): Network parameters

        Returns:
            (list): Two network objects

        """
        child_params = {}

        # Loop through the parameters and pick params for the kid.
        for param in mother.param_choices:
            child_params[param] = random.choice(
                [mother.params[param], father.params[param]]
            )

        # Now create a new Indidvidual object.
        child = mother.__class__(
            params=child_params, param_choices=mother.param_choices
        )
        return child


class Evolver(object):
    """genetic algorithm evolution helper class"""

    def __init__(self, retain=0.4, lucky_chance=0.1, mutate_chance=0.2,
                       freak_chance=0, best_count=10, elite_count=5,
                       min_childcount=1, max_childcount=1):
        """:param retain (float): portion of population to retain after
                each generation (fittest individuals that may reproduce again)
                0.0 means the next generation will only contain children, no parents
                1.0 means there will only be parents and never any children
           :param lucky_chance (float): probability of a rejected individual
                to remain in the population.
                0.0 means only breed best retained parents
                1.0 means all individuals will be retained and there will
                be no children.
           :param mutate_chance (float): Probability of an individual to
                be randomly mutated (0.0/1.0 means no/every individual will
                have one param randomly mutated)
           :param freak_chance (float): Probability of a new completely
                random individual to join a generation for breeding
                0.0 means no random genotype will ever appear
                1.0 means alls parents will be randomized before breeding
           :param best_count (int): top-n individuals to display after
                last generation
           :param elite_count (int): groupsize of all-time best performing
                individuals
           :param min_childcount (int): minimum amount of children two parents have
           :param max_childcount (int): maximum amount of children two parents can have
        """
        self.freak_chance = freak_chance
        self.mutate_chance = mutate_chance
        self.lucky_chance = lucky_chance
        self.retain = retain
        self.best_count = best_count
        self.elite_count = elite_count
        self.min_childcount = min_childcount
        self.max_childcount = max_childcount
        # all-time best performers
        self.elite = []
        # all parents won't work
        if self.retain == 1.0:
            raise ValueError("retain rate of 1.0 means there can never be any children")
        # no selection won't work
        if self.lucky_chance == 1.0:
            raise ValueError("keeping every individual for breeding would disable selection")
        # all randomness makes no sense
        if freak_chance == 1.0:
            raise ValueError("100% freaks will prevent evolution")
        # install CTL+C signal handler
        signal.signal(signal.SIGINT, self.summary)

    def evolve(self, population):
        """evolve one generation"""

        # Get scores for each individual.
        graded = sorted(population, key=lambda i: i.fitness(), reverse=True)

        # Get the number we want to keep for the next gen.
        retain_length = int(len(graded)*self.retain)

        # possible parents we want to breed.
        parents = graded[:retain_length]

        # For those we aren't keeping, randomly keep some anyway.
        for individual in graded[retain_length:]:
            if self.lucky_chance > random.random():
                parents +=  [ individual ]

        # Now find out how many childre we need to meet population goal
        parents_length = len(parents)
        desired_length = len(population) - parents_length

        # Add children, which are bred from two random parents.
        children = []
        while len(children) < desired_length:
            # Get a random mom and dad.
            male_idx = random.randint(0, parents_length-1)
            female_idx = random.randint(0, parents_length-1)
            # Assure they aren't the same individual...
            if male_idx == female_idx:
                continue
            # determine childcount
            childcount = random.randint(self.min_childcount, self.max_childcount)
            # don't overcrowd population
            if len(children) + childcount > desired_length:
                childcount = desired_length - len(children)
            # breed n children
            for n in range(childcount):
                # breed new individual
                child = Individual.crossover(parents[male_idx], parents[female_idx])
                # Randomly mutate some of the individuals
                if self.mutate_chance >= random.random():
                    child.mutate()
                # add a freak?
                if self.freak_chance >= random.random():
                    # shuffle genome
                    child.shuffle()
                # add to list of children
                children += [ child ]

        # add children to population
        population = parents + children

        # sort population by fitness
        population = sorted(population, key=lambda x: x.fitness(), reverse=True)

        return population

    def optimize(self, individuals, generations=100):
        # store population
        self.individuals = individuals
        # evolve all generations
        for g in range(generations):
            print(f"evolving generation: {g}")

            # evaluate current population
            for i in self.individuals:
                print(f" evaluating individual: {i}")
                # don't evaluate again if params didn't change
                if not i.evaluated_params or i.evaluated_params != i.params:
                    # let the individual live a life according to its parameters
                    # (create phenotype from genotype)
                    i.live()
                    # remember evaluated params
                    i.evaluated_params = i.params
                print(f"  score: {i.fitness()}")

            # best performer from this generation
            best = sorted(self.individuals, key=lambda x: x.fitness(), reverse=True)[0]
            # append to all-time hitlist
            self.elite += [ best ]
            # only keep n best individuals in all-time hitlist
            self.elite = sorted(self.elite, key=lambda x: x.fitness(), reverse=True)
            self.elite = self.elite[:self.elite_count]

            # generation status
            print(
                f" avg. fitness: {self.avg_fitness(self.individuals)}\n"
                f" best: {best.fitness()}"
            )

            # check if one individual is the chosen one
            if any([ x.finished() for x in self.individuals ]):
                print(f" finishing early in generation {g}")
                # return early
                break

            # Evolve this generation, except on the last iteration.
            if g != generations - 1:
                self.individuals = self.evolve(self.individuals)

        # print out summary
        self.summary()

        # last generation
        return individuals

    def summary(self, sig=None, frame=None):
        # Print out the top 10 networks.
        print(f"best {self.best_count} of last generation:")
        print("\n".join([ str(i) for i in self.individuals[:self.best_count] ]))
        print(f"best {self.elite_count} of all-time elite:")
        print("\n".join([ str(i) for i in self.elite[:self.elite_count] ]))
        # if CTRL+C was pressed, exit immediately
        if sig != None:
            sys.exit(0)

    @staticmethod
    def avg_fitness(population):
        return sum(map(lambda x: x.fitness(), population)) / len(population)
