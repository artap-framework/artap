from .utils import VectorAndNumbers
from .algorithm import Algorithm
from .population import Population
from .individual import Individual


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

        self.options.declare(name='max_population_size', default=100, lower=1,
                             desc='Maximal number of individuals in population')

    def run(self):
        self.population_size = self.options['max_population_size']

        parameters = []
        for parameter in self.problem.parameters:
            parameters.append(float(parameter['initial_value']))

        population = Population()

        for parameter_name in self.parameters:
            parameter_values = []

            index = 0
            selected_parameter = None
            for parameter in self.parameters:
                if parameter['name'] == parameter_name['name']:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.options['max_population_size']):
                value = VectorAndNumbers.gen_number(selected_parameter['bounds'], selected_parameter['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy())
                individuals.append(individual)

            self.evaluate(population.individuals)
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

        # write to datastore
        self.problem.data_store.write_population(population)
