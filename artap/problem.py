from abc import ABC, abstractmethod

from .datastore import SqliteDataStore
from .individual import Individual
from .utils import flatten


"""
 Module is dedicated to describe optimization problem. 
"""


class Problem(ABC):
    """ Is a main class wich collects information about optimization task """    
           
    def __init__(self, name, parameters, costs, datastore=None, working_dir=None):
        self.name = name

        self.working_dir = working_dir
        self.parameters = parameters
        self.costs = {cost: 0 for cost in costs}

        if datastore is None:
            self.datastore = SqliteDataStore(self, working_dir=working_dir)
            self.datastore.create_structure_individual(self.parameters, self.costs)
            self.datastore.create_structure_parameters(self.get_parameters_list())
            self.datastore.create_structure_costs(self.costs)

        else:
            self.datastore = datastore
        
        self.id = self.datastore.get_id()
        self.populations = []
        
    def add_population(self, population):                
        self.populations.append(population)
        
    def evaluate_individual(self, x, population = 0):
        individ = Individual(x, self, population)        
        individ.evaluate()
        self.datastore.write_individual(individ.to_list())
        self.populations[population].individuals.append(individ)
        
        if len(individ.costs) == 1:
            return individ.costs[0]
        else:
            return individ.costs
                       
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
    
    @property
    def get_initial_values(self):
        values = []
        for parameter in self.parameters.items():
            if 'initial_value' in parameter[1]:
                values.append(parameter[1]['initial_value'])    
            else:
                values.append(0)
        return values

    @abstractmethod
    def eval(self):
        pass

    def get_parameters_list(self):
        parameters_list =[]
        names = list(self.parameters.keys())
        i = 0
        for sudb_dict in list(self.parameters.values()):
            parameter = [names[i]]
            parameter.extend(flatten(sudb_dict.values()))
            parameters_list.append(parameter)
            i += 1
        return parameters_list


class ProblemDataStore(Problem):
    def __init__(self, datastore):
        self.datastore = datastore
        self.datastore.read_problem(self)

    def eval(self):
        assert 0

    def to_table(self):
        table = []
        line = ["Population ID"]
        for parameter in self.get_parameters_list():
            line.append(parameter[0])
        for cost in self.costs:
            line.append(cost    )
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