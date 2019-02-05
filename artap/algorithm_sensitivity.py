from .utils import VectorAndNumbers
from .algorithm import Algorithm
from .population import Population
from .individual import Individual


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

    def run(self):
        parameters = []
        for parameter in self.problem.parameters.items():
            parameters.append(float(parameter[1]['initial_value']))

        population = Population()

        for parameter_name in self.parameters:
            parameter_values = []

            index = 0
            selected_parameter = None
            for parameter in self.problem.parameters.items():
                if parameter[0] == parameter_name:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.options['max_population_size']):
                value = VectorAndNumbers.gen_number(selected_parameter[1]['bounds'], selected_parameter[1]['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy())
                individuals.append(individual)

            population.individuals = self.evaluate(population.individuals)
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

        # write to datastore
        self.problem.data_store.write_population(population)
