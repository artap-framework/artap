from .datastore import DataStore, FileDataStore, DummyDataStore
from .utils import ConfigDictionary
from .surrogate import SurrogateModelEval
from abc import ABC, abstractmethod

import os
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
        self.options.declare(name='time_out', default=600,
                             desc='Maximal time for calculation')

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


class Problem(ProblemBase):
    """ The Class Problem Is a main class which collects information about optimization task """

    MINIMIZE = -1
    MAXIMIZE = 1

    def __init__(self, name, parameters, costs, working_dir=None):
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

        # default datastore
        self.data_store = DummyDataStore(self)

        # self.id = self.data_store.get_id()

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


# class ProblemSqliteDataStore(ProblemBase):
#
#     def __init__(self, database_name, working_dir=None):
#         super().__init__()
#         self.working_dir = working_dir
#
#         self.data_store = SqliteDataStore(self, database_name=database_name, remove_existing=False)
#         # self.data_store.read_from_datastore()


class ProblemFileDataStore(ProblemBase):

    def __init__(self, database_name, working_dir=None):
        super().__init__()
        self.working_dir = working_dir

        self.data_store = FileDataStore(self, database_name=database_name, remove_existing=False)
        # self.data_store.read_from_datastore()
