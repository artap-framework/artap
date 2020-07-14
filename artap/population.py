from .individual import Individual


class Population:

    counter = 0

    def __init__(self, individuals=None):
        self.id = Population.counter
        Population.counter += 1
        self.individuals = []
        if individuals is not None:
            self.set_individuals(individuals)
        self.pareto_vectors: list = []
        self.pareto_costs: list = []

    def set_individuals(self, individuals=None):
        self.individuals = individuals
        for individual in self.individuals:
            individual.population_id = self.id

    def __str__(self):
        string = "individuals: {}\n".format(len(self.individuals))
        for individual in self.individuals:
            string += "\t{},\n".format(individual.__str__())
        return string

    def __eq__(self, other):
        if not isinstance(other, Population):
            return NotImplemented

        return self.individuals == other.individuals and self.pareto_vectors == other.pareto_vectors and self.pareto_costs == other.pareto_costs