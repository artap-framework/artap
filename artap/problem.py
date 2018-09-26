from abc import ABC, abstractmethod

from .datastore import SqliteDataStore
from .individual import Individual
from .utils import flatten


"""
 Module is dedicated to describe optimization problem. 
"""


class ProblemBase(ABC):

    def __init__(self):
        self.name: str = None
        self.populations: list = None
        self.parameters: dict = None
        self.costs: list = None
        self.data_store: SqliteDataStore = None
        self._algorithm = None
        self.max_population_size = 1
        self.max_population_count = 10

    def get_parameters_list(self):
        parameters_list = []
        names = list(self.parameters.keys())
        i = 0
        for sub_dict in list(self.parameters.values()):
            parameter = [names[i]]
            parameter.extend(flatten(sub_dict.values()))
            parameters_list.append(parameter)
            i += 1
        return parameters_list


class Problem(ProblemBase):
    """ Is a main class which collects information about optimization task """
           
    def __init__(self, name, parameters, costs, data_store=None, working_dir=None):

        super().__init__()
        self.name = name
        self.working_dir = working_dir
        self.parameters = parameters
        self.costs = {cost: 0 for cost in costs}

        if data_store is None:
            self.data_store = SqliteDataStore(self, working_dir=working_dir)
            self.data_store.create_structure_individual(self.parameters, self.costs)
            self.data_store.create_structure_parameters(self.get_parameters_list())
            self.data_store.create_structure_costs(self.costs)

        else:
            self.data_store = data_store
        
        self.id = self.data_store.get_id()
        self.populations = []
        
    def add_population(self, population):                
        self.populations.append(population)
        
    def evaluate_individual(self, x, population=0):
        individual = Individual(x, self, population)
        individual.evaluate()
        self.data_store.write_individual(individual.to_list())
        self.populations[population].individuals.append(individual)
        
        if len(individual.costs) == 1:
            return individual.costs[0]
        else:
            return individual.costs

    def eval_batch(self, table):
        n = len(table)
        results = [0] * n
        for i in range(n):
            results[i] = self.eval(table[i])
        return results

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        self._algorithm = algorithm

    def get_initial_values(self):
        values = []
        for parameter in self.parameters.items():
            if 'initial_value' in parameter[1]:
                values.append(parameter[1]['initial_value'])    
            else:
                values.append(0)
        return values

    @abstractmethod
    def eval(self, x: list):
        pass


class ProblemDataStore(ProblemBase):

    def __init__(self, data_store):

        super().__init__()
        self.data_store = data_store
        self.data_store.read_problem(self)

    def to_table(self):
        table = []
        line = ["Population ID"]
        for parameter in self.get_parameters_list():
            line.append(parameter[0])
        for cost in self.costs:
            line.append(cost)
        table.append(line)
        for population in self.populations:
            for individual in population.individuals:
                line = [population.number]
                for parameter in individual.parameters:
                    line.append(parameter)
                for cost in individual.costs:
                    line.append(cost)
                table.append(line)
        return table
