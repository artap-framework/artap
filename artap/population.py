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

    def __eq__(self, other):
        if not isinstance(other, Population):
            return NotImplemented

        return self.individuals == other.individuals and self.archives == other.archives and self.pareto_vectors == other.pareto_vectors and self.pareto_costs == other.pareto_costs