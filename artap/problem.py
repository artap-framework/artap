"""
 Module is dedicated to describe optimization problem.
"""

from .datastore import SqliteDataStore, DummyDataStore
from .utils import ConfigDictionary
from .surrogate import SurrogateModelEval
from abc import abstractmethod

import logging
import datetime
import tempfile
import os
import shutil
import atexit
import platform

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

_log_level = [CRITICAL, ERROR, WARNING, INFO, DEBUG]


class Problem:
    """ The Class Problem Is a main class which collects information about optimization task """

    # __is_frozen = False

    def __init__(self, **kwargs):

        self.options = ConfigDictionary()
        # options
        self.options.declare(name='calculate_gradients', default=False,
                             desc='calculate gradient for individuals')
        self.options.declare(name='log_level', default=logging.INFO, values=_log_level,
                             desc='Log level')
        self.options.declare(name='log_file_handler', default=False,
                             desc='Enable file handler')
        self.options.declare(name='log_db_handler', default=True,
                             desc='Enable DB handler')
        self.options.declare(name='log_console_handler', default=True,
                             desc='Enable console handler')
        self.options.declare(name='time_out', default=600,
                             desc='Maximal time for calculation')
        self.options.declare(name='save_data_files', default=False,
                             desc='Saving data from computation')

        # tmp name
        d = datetime.datetime.now()
        ts = d.strftime("{}-%f".format(self.__class__.__name__))

        # create logger
        self.logger = logging.getLogger(ts)
        self.logger.setLevel(self.options['log_level'])

        # create formatter
        self.formatter = logging.Formatter('%(asctime)s (%(levelname)s): '
                                           '%(name)s - %(funcName)s (%(lineno)d) - %(message)s')

        if self.options['log_console_handler']:
            # create console handler and set level to debug
            stream_err_handler = logging.StreamHandler()
            stream_err_handler.setLevel(logging.DEBUG)
            # add formatter to StreamHandler
            stream_err_handler.setFormatter(self.formatter)
            # add StreamHandler to logger
            self.logger.addHandler(stream_err_handler)

            # stream_std_handler = logging.StreamHandler()
            # stream_std_handler.setLevel(logging.INFO)
            # # add formatter to StreamHandler
            # stream_std_handler.setFormatter(self.formatter)
            # # add StreamHandler to logger
            # self.logger.addHandler(stream_std_handler)

        # for h in list(self.logger.handlers):
        #     print(h)

        self.logger.debug("START")

        self.name: str = str()
        self.description: str = str()
        self.parameters: list = list()
        self.costs: list = list()
        self.constraints: list = list()
        self.signs = []

        self.info = {"processor": platform.processor(),
                     "system": platform.system(),
                     "python": platform.python_version(),
                     "hostname": platform.node()}

        # populations
        self.individuals = []
        self.data_store = None
        self.executor = None
        self.failed = []  # storage for failed individuals
        self.data_store = DummyDataStore()
        self.output_files = None

        self.working_dir = tempfile.gettempdir() + os.sep + "artap-{}".format(ts) + os.sep
        os.mkdir(self.working_dir)

        # surrogate model (default - only simple eval)
        self.surrogate = SurrogateModelEval(self)

        # self._freeze()
        self.set(**kwargs)
        for cost in self.costs:
            if 'criteria' in cost:
                if cost['criteria'] == 'minimize':
                    self.signs.append(1)
                else:
                    self.signs.append(-1)
            else:
                self.signs.append(1)

        # clean up
        atexit.register(self.cleanup)

    def populations(self):
        individuals = {}
        for individual in self.individuals:
            if individual.population_id not in individuals:
                individuals[individual.population_id] = []
            individuals[individual.population_id].append(individual)

        return individuals

    def population(self, population_id):
        individuals = []
        for individual in self.individuals:
            if individual.population_id == population_id:
                individuals.append(individual)

        return individuals

    def last_population(self):
        # find max index
        max_index = -1
        for individual in self.individuals:
            if individual.population_id > max_index:
                max_index = individual.population_id

        # add to population
        return self.population(max_index)

    def to_dict(self):
        parameters = list(self.parameters)
        output = {'name': self.name, 'description': self.description, 'parameters': parameters}
        return output

    @staticmethod
    def from_dict():
        pass

    def cleanup(self):
        if self.data_store:
            self.data_store.destroy()

        if self.working_dir.startswith(tempfile.gettempdir() + os.sep + "artap-"):
            shutil.rmtree(self.working_dir)

    @abstractmethod
    def set(self, **kwargs):
        pass

    def parameters_len(self):
        return len(self.parameters)

    # search for and defines the initial values for the optimization problem
    def get_initial_values(self):
        values = []
        for parameter in self.parameters:
            if 'initial_value' in parameter:
                values.append(parameter['initial_value'])
            else:
                values.append(0)
        return values

    def get_parameter_types(self):
        p_types = []
        for parameter in self.parameters:

            if 'parameter_type' in parameter:
                if parameter['parameter_type'].lower == 'real':
                    p_types.append('real')

                if parameter['parameter_type'].lower == 'integer':
                    p_types.append('integer')

                if parameter['parameter_type'].lower == 'boolean':
                    p_types.append('boolean')

            else:
                p_types.append('real')

        return p_types

    @abstractmethod
    def evaluate(self, individual):
        """ :param individual: Individual """
        pass

    @abstractmethod
    def evaluate_inequality_constraints(self, x):
        """ :param x: vector """
        return []

    def __setattr__(self, key, value):
        # if self.__is_frozen and not hasattr(self, key):
        #     raise TypeError(" %r is a frozen class" % self)
        object.__setattr__(self, key, value)

        # working dir must be set
        if hasattr(self.options, 'log_file_handler'):
            if self.working_dir:
                # create file handler and set level to debug
                file_handler = logging.FileHandler(self.working_dir + "/data.log")
                file_handler.setLevel(logging.DEBUG)
                # add formatter to FileHandler
                file_handler.setFormatter(self.formatter)
                # add FileHandler to logger
                self.logger.addHandler(file_handler)

    # def _freeze(self):
    #     self.__is_frozen = True


class ProblemViewDataStore(Problem):
    def __init__(self, database_name):
        super().__init__()
        self.data_store = SqliteDataStore(self, database_name=database_name, mode="read")

    def set(self, **kwargs):
        pass

    def evaluate(self, individual):
        pass
