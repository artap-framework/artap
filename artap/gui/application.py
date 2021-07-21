import importlib.util
import inspect

# Artap imports
from ..algorithm_genetic import NSGAII
from ..datastore import SqliteDataStore
from ..problem import Problem
from ..results import Results

from .tree_model import TreeModel


class ProblemData:

    def __init__(self, problem_window=None):
        self.problem = None
        self.results = None
        self.problem_tree = None
        self.code = None
        self.problem_window = problem_window

    def read_problem_file(self, code_file_name) -> str:
        with open(code_file_name[0]) as code_file:
            self.code = code_file.read()
        module_path = code_file_name[0]
        module_name = module_path.replace(".py", '')
        module_name = module_name.split('/')[-1]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.problem = None
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                if name.find('Problem') != -1:
                    self.problem = obj()
                    break
        return self.code

    def parse_problem(self, problem_file=None):
        pass

    def process_results(self, database_file=None):
        if database_file is not None:
            self.problem = Problem()
            SqliteDataStore(self.problem, database_name=database_file[0])
        self.results = Results(self.problem)
        ids = self.results.get_population_ids()
        self.problem_tree = dict()
        populations = dict()
        for i, ide in enumerate(ids):
            population = dict()
            for j, individual in enumerate(self.results.population(i)):
                item = dict()
                item['vector'] = individual.vector
                item['costs'] = individual.costs
                item['Pareto front'] = individual.features['front_number']
                population['Individual {}'.format(j)] = item

            populations['Population {}'.format(i)] = population
        self.problem_tree[self.problem.name] = populations

        headers = ["Item", "Value"]

        self.problem_window.show_results(self.results)
        problem_model = TreeModel(headers, self.problem_tree)
        self.problem_window.tree_view.setModel(problem_model)
        self.problem_window.tree_view.setModel(problem_model)
        self.problem_window.tree_view.setWindowTitle("Simple Tree Model")

    def run_problem(self):
        if self.code is not None:
            database_file = 'data.sqlite'
            datastore = SqliteDataStore(self.problem, database_name=database_file, mode='write')
            algorithm = NSGAII(self.problem)
            algorithm.options['max_population_number'] = 10
            algorithm.options['max_population_size'] = 10
            algorithm.run()
            datastore.sync_all()
            self.process_results()


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Application:
    def __init__(self):
        self.problems = []
