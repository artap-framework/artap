from .datastore import SqliteDataStore
from .individual import Individual
from .utils import flatten
from .utils import ConfigDictionary

from abc import ABC, abstractmethod
from datetime import datetime
import os
import tempfile
import multiprocessing


"""
 Module is dedicated to describe optimization problem. 
"""


class ProblemBase(ABC):

    def __init__(self):
        self.name: str = None
        self.description = ""
        self.populations: list = None
        self.parameters: dict = None
        self.costs: list = None
        self.data_store: SqliteDataStore = None

        # options
        self.options = ConfigDictionary()

        self.options.declare(name='save_data', default=False,
                             desc='Save data to database')
        self.options.declare(name='save_level', default="problem",
                             desc='Save level')
        # options
        self.options.declare(name='max_processes', default=max(int(2 / 3 * multiprocessing.cpu_count()), 1),
                             desc='Max running processes')


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

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self, name, parameters, costs, data_store=None, working_dir=None, save_data=False):

        super().__init__()
        self.name = name
        self.working_dir = working_dir
        self.parameters = parameters
        self.costs = {cost: 0.0 for cost in costs}
        self.options['save_data'] = save_data

        if (working_dir is None) or (not self.options['save_data']):
            self.working_dir = tempfile.mkdtemp()
        else:
            #time_stamp = str(datetime.now()).replace(' ', '_').replace(':', '-')
            time_stamp = ""

            self.working_dir += time_stamp
            if not os.path.isdir(self.working_dir):
                os.mkdir(self.working_dir)

        if data_store is None:
            self.data_store = SqliteDataStore(problem=self, working_dir=self.working_dir, create_database=True)
            self.data_store.create_structure_task(self)
            self.data_store.create_structure_individual(self.parameters, self.costs)
            self.data_store.create_structure_parameters(self.get_parameters_list())
            self.data_store.create_structure_costs(self.costs)

        else:
            self.data_store = data_store
        
        self.id = self.data_store.get_id()
        self.populations = []
        
    def __del__(self):
        pass
        #print("Problem: def __del__(self):")
        #if not self.save_data:
        #    if os.path.isdir(self.working_dir):
        #        shutil.rmtree(self.working_dir)

    def add_population(self, population):
        self.populations.append(population)

    def chromosome_len(self):
        return len(self.parameters)

    def evaluate_individual(self, x, population=0):
        """

        :param x:
        :param population:
        :return: cost which is calculated
        """

        individual = Individual(x, self, population)
        cost = individual.evaluate()
        self.populations[population].individuals.append(individual)

        return cost

    def evaluate_gradient_richardson(self, individual):
        n = len(self.parameters)
        gradient = [0] * n
        x0 = individual.parameters
        h = 1e-6
        y = self.eval(x0)
        for i in range(len(self.parameters)):
            x = x0.copy()
            x[i] += h
            y_h = self.eval(x)
            D_0_h = gradient[i] = (y_h - y) / h
            x[i] += h
            y_2h = self.eval(x)
            d_0_2h = (y_2h - y) / 2 / h
            gradient[i] = (4*D_0_h - d_0_2h) / 3

        print(gradient)
        return gradient

    def evaluate_gradient(self, individual):
        n = len(self.parameters)
        gradient = [0]*n
        x0 = individual.parameters
        y = self.eval(x0)
        h = 1e-6
        for i in range(len(self.parameters)):
            x = x0.copy()
            x[i] += h
            y_h = self.eval(x)
            gradient[i] = (y_h - y) / h

        print(gradient)
        return gradient

    def eval_batch(self, table):
        n = len(table)
        results = [0] * n
        for i in range(n):
            results[i] = self.eval(table[i])
        return results

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
        """ :param x: list of the variables """
        pass

    # @abstractmethod
    def eval_constraints(self, x: list):
        """ :param x: list of the variables """
        pass

    def eval_gradient(self, x: list):
        """ :param x: list of the variables """
        pass

class ProblemDataStore(ProblemBase):

    def __init__(self, data_store, working_dir=None):

        super().__init__()
        self.data_store = data_store
        self.data_store.read_problem(self)

        if working_dir is None:
            self.working_dir = tempfile.mkdtemp()
            self.options['save_data'] = False
        else:
            self.working_dir = working_dir + self.name
            self.options['save_data'] = True

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
                line = [individual.population_id]
                for parameter in individual.parameters:
                    line.append(parameter)
                for cost in individual.costs:
                    line.append(cost)
                table.append(line)
        return table
