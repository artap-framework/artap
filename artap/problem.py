from .datastore import DataStore, SqliteDataStore, SqliteHandler, DummyDataStore
from .utils import flatten
from .utils import ConfigDictionary
from .server import ArtapServer
from .surrogate import SurrogateModelEval
from abc import ABC, abstractmethod

import os
import multiprocessing
import logging
import datetime

"""
 Module is dedicated to describe optimization problem. 
"""

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

_log_level = [CRITICAL, ERROR, WARNING, INFO, DEBUG]


class ProblemBase(ABC):

    def __init__(self):
        self.name: str = None
        self.description = ""
        self.parameters: dict = None
        self.costs: list = None
        self.data_store: DataStore = None
        self.server = None

        # options
        self.options = ConfigDictionary()

        self.options.declare(name='calculate_gradients', default=False,
                             desc='calculate gradient for individuals')
        self.options.declare(name='save_level', default="individual",
                             desc='Save level')
        self.options.declare(name='log_level', default=logging.INFO, values=_log_level,
                             desc='Log level')
        self.options.declare(name='log_file_handler', default=False,
                             desc='Enable file handler')
        self.options.declare(name='log_db_handler', default=True,
                             desc='Enable DB handler')
        self.options.declare(name='log_console_handler', default=True,
                             desc='Enable console handler')
        # TODO: move to Algorithm class
        self.options.declare(name='max_processes', default=max(int(2 / 3 * multiprocessing.cpu_count()), 1),
                             desc='Max running processes')

        # tmp name
        d = datetime.datetime.now()
        ts = d.strftime("{}-%f".format(self.__class__.__name__))
        # create logger
        self.logger = logging.getLogger(ts)
        self.logger.setLevel(self.options['log_level'])

        for h in list(self.logger.handlers):
            print(h)

        # create formatter
        self.formatter = logging.Formatter('%(asctime)s (%(levelname)s): %(name)s - %(funcName)s (%(lineno)d) - %(message)s')

        if self.options['log_console_handler']:
            # create console handler and set level to debug
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            # add formatter to StreamHandler
            stream_handler.setFormatter(self.formatter)
            # add StreamHandler to logger
            self.logger.addHandler(stream_handler)

    def __del__(self):
        # for h in list(self.logger.handlers):
        #    print(h)
        pass

    def run_server(self, open_viewer=False, daemon=True, local_host=True):
        # testing - Artap Server
        self.server = ArtapServer(problem=self, local_host=local_host)
        self.server.run_server(open_viewer, daemon)

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
    """ The Class Problem Is a main class which collects information about optimization task """

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self, name, parameters, costs, data_store=None, working_dir=None):
        super().__init__()
        self.name = name
        self.working_dir = working_dir

        forbidden_path = os.sep + "workspace" + os.sep + "common_data"
        if working_dir is not None:
            if forbidden_path in self.working_dir:
                raise IOError('Folder "/workspace/common_data" is read only.')

        self.parameters = parameters
        self.costs = {cost: 0.0 for cost in costs}

        # working dir must be set
        if self.options['log_file_handler'] and working_dir:
            # create file handler and set level to debug
            file_handler = logging.FileHandler(self.working_dir + "/data.log")
            file_handler.setLevel(logging.DEBUG)
            # add formatter to FileHandler
            file_handler.setFormatter(self.formatter)
            # add FileHandler to logger
            self.logger.addHandler(file_handler)

        if data_store is None:
            # self.data_store = SqliteDataStore(problem=self, working_dir=self.working_dir, create_database=True)
            self.data_store = DummyDataStore(self)
            self.data_store.create_structure()

        else:
            self.data_store = data_store
            self.data_store.problem = self
        
        self.id = self.data_store.get_id()

        # working dir must be set
        if self.options['log_db_handler'] and isinstance(self.data_store, SqliteDataStore):
            # create file handler and set level to debug
            file_handler = SqliteHandler(self.data_store)
            file_handler.setLevel(logging.DEBUG)
            # add formatter to SqliteHandler
            file_handler.setFormatter(self.formatter)
            # add SqliteHandler to logger
            self.logger.addHandler(file_handler)

        self.logger.debug("START")
        # self.logger.debug('This message should go to the log file')
        # self.logger.info('So should this')
        # self.logger.warning('And this, too')

        # surrogate model (default - only simple eval)
        self.surrogate = SurrogateModelEval(self)

    def __del__(self):
        super().__del__()

    def parameters_len(self):
        return len(self.parameters)

    # TODO: FIX table.append([parameter[2], parameter[3]])
    def get_bounds(self):
        table = []
        for parameter in self.get_parameters_list():
            table.append([parameter[2], parameter[3]])
        return table

    def get_initial_values(self):
        values = []
        for parameter in self.parameters.items():
            if 'initial_value' in parameter[1]:
                values.append(parameter[1]['initial_value'])
            else:
                values.append(0)
        return values

    @abstractmethod
    def evaluate(self, x: list):
        """ :param x: list of the variables """
        pass

    def evaluate_constraints(self, x: list):
        """ :param x: list of the variables """
        pass


class ProblemDataStore(ProblemBase):

    def __init__(self, data_store, working_dir=None):
        super().__init__()
        self.working_dir = working_dir

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
        for population in self.data_store.populations:
            for individual in population.individuals:
                line = [individual.population_id]
                for parameter in individual.parameters:
                    line.append(parameter)
                for cost in individual.costs:
                    line.append(cost)
                table.append(line)
        return table
