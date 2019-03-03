from .individual import Individual


class Population:
    def __init__(self, individuals: list = None):
        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals.copy()

        self.pareto_vectors: list = []
        self.pareto_costs: list = []

    def __str__(self):
        string = "Population: {} individuals\n".format(len(self.individuals))
        for individual in self.individuals:
            string += "\t{},\n".format(individual.__str__())
        return string

    def gen_population_from_table(self, table):
        for parameters in table:
            individual = Individual(parameters)
            self.individuals.append(individual)

    def to_list(self):
        table = []
        for individual in self.individuals:
            table.append(individual.to_list())

        return table


class PopulationGenetic(Population):

    def __init__(self, individuals=None):
            if individuals is None:
                individuals = []
            super().__init__(individuals)

    def gen_random_population(self, population_size, vector_length, parameters):
        self.individuals = Individual.gen_individuals(population_size, self.id)
