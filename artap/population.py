from .individual import Individual


class Population:
    def __init__(self, individuals: list = None, archives: list = None):
        if individuals is None:
            self.individuals = []
        else:
            self.individuals = individuals.copy()

        if archives is None:
            self.archives = []
        else:
            self.archives = archives.copy()

        self.pareto_vectors: list = []
        self.pareto_costs: list = []

    def __str__(self):
        string = "individuals: {}\n".format(len(self.individuals))
        for individual in self.individuals:
            string += "\t{},\n".format(individual.__str__())
        return string

    def gen_population_from_table(self, table):
        for parameters in table:
            individual = Individual(parameters)
            self.individuals.append(individual)

    def to_list(self, population_number):
        table = []
        for individual in self.individuals:
            params = individual.to_list()
            params.insert(0, self.individuals.index(individual) + 1)
            # population index
            params.insert(1, population_number)
            table.append(params)

        return table
