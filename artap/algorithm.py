from .problem import Problem
from .population import Population, Population_NSGA_II
from .individual import Individual_NSGA_II, Individual

from abc import ABCMeta, abstractmethod
import random

class ConfigDictionary(object):
    """
    Attributes
    ----------
    _dict : dict of dict
        Dictionary of entries. Each entry is a dictionary consisting of value, values, types, desc, lower, and upper.
    _read_only : bool
        If True, setting (via __setitem__ or update) is not permitted.
    """

    def __init__(self, read_only=False):
        """
        Initialize all attributes.

        Parameters
        ----------
        read_only : bool
            If True, setting (via __setitem__ or update) is not permitted.
        """
        self._dict = {}
        self._read_only = read_only

    def _assert_valid(self, name, value):
        """
        Check whether the given value is valid, where the key has already been declared.

        The optional checks consist of ensuring: the value is one of a list of acceptable values,
        the type of value is one of a list of acceptable types, value is not less than lower,
        value is not greater than upper, and value satisfies is_valid.

        Parameters
        ----------
        name : str
            The key for the declared entry.
        value : object
            The default or user-set value to check for value, type, lower, and upper.
        """
        meta = self._dict[name]
        values = meta['values']
        types = meta['types']
        lower = meta['lower']
        upper = meta['upper']
        is_valid = meta['is_valid']

        if not (value is None and meta['allow_none']):
            # If only values is declared
            if values is not None:
                if value not in values:
                    raise ValueError("Entry '{}'\'s value is not one of {}".format(name, values))
            # If only types is declared
            elif types is not None:
                if not isinstance(value, types):
                    raise TypeError("Entry '{}' has the wrong type ({})".format(name, types))

            if upper is not None:
                if value > upper:
                    msg = "Value of {} exceeds maximum of {} for entry 'x'"
                    raise ValueError(msg.format(value, upper))
            if lower is not None:
                if value < lower:
                    msg = "Value of {} exceeds minimum of {} for entry 'x'"
                    raise ValueError(msg.format(value, lower))

        # General function test
        if is_valid is not None and not is_valid(value):
            raise ValueError("Function is_valid returns False for {}.".format(name))

    def declare(self, name, default, values=None, types=None, desc='',
                upper=None, lower=None, is_valid=None, allow_none=False):
        r"""
        Declare an option.

        The value of the option must satisfy the following:
        1. If values only was given when declaring, value must be in values.
        2. If types only was given when declaring, value must satisfy isinstance(value, types).
        3. It is an error if both values and types are given.

        Parameters
        ----------
        name : str
            Name of the option.
        default : object or Null
            Optional default value that must be valid under the above 3 conditions.
        values : set or list or tuple or None
            Optional list of acceptable option values.
        types : type or tuple of types or None
            Optional type or list of acceptable option types.
        desc : str
            Optional description of the option.
        upper : float or None
            Maximum allowable value.
        lower : float or None
            Minimum allowable value.
        is_valid : function or None
            General check function that returns True if valid.
        allow_none : bool
            If True, allow None as a value regardless of values or types.
        """

        if values is not None and not isinstance(values, (set, list, tuple)):
            raise TypeError("'values' must be of type None, list, or tuple - not %s." % values)
        if types is not None and not isinstance(types, (type, set, list, tuple)):
            raise TypeError("'types' must be None, a type or a tuple  - not %s." % types)

        if types is not None and values is not None:
            raise RuntimeError("'types' and 'values' were both specified for option '%s'." %
                               name)

        self._dict[name] = {
            'value': default,
            'values': values,
            'types': types,
            'desc': desc,
            'upper': upper,
            'lower': lower,
            'is_valid': is_valid,
            'allow_none': allow_none
        }

        # check for validity
        self._assert_valid(name, default)

    def update(self, in_dict):
        """
        Update the internal dictionary with the given one.

        Parameters
        ----------
        in_dict : dict
            The incoming dictionary to add to the internal one.
        """
        for name in in_dict:
            self[name] = in_dict[name]

    def __iter__(self):
        """
        Provide an iterator.

        Returns
        -------
        iterable
            iterator over the keys in the dictionary.
        """
        return iter(self._dict)

    def __contains__(self, key):
        """
        Check if the key is in the local dictionary.

        Parameters
        ----------
        key : str
            name of the entry.

        Returns
        -------
        boolean
            whether key is in the local dict.
        """
        return key in self._dict

    def __setitem__(self, name, value):
        """
        Set an entry in the local dictionary.

        Parameters
        ----------
        name : str
            name of the entry.
        value : -
            value of the entry to be value- and type-checked if declared.
        """
        if self._read_only:
            msg = "Tried to set '{}' on a read-only OptionsDictionary."
            raise KeyError(msg.format(name))

        # The key must have been declared.
        if name not in self._dict:
            msg = "Key '{}' cannot be set because it has not been declared."
            raise KeyError(msg.format(name))

        self._assert_valid(name, value)
        self._dict[name]['value'] = value

    def __getitem__(self, name):
        """
        Get an entry from the local dict, global dict, or declared default.

        Parameters
        ----------
        name : str
            name of the entry.

        Returns
        -------
        value : -
            value of the entry.
        """
        # If the entry has been set in this system, return the set value
        try:
            meta = self._dict[name]
            return meta['value']
        except KeyError:
            raise KeyError("Entry '{}' cannot be found".format(name))

class Algorithm(metaclass=ABCMeta):
    """ Base class for optimization algorithms. """

    def __init__(self, problem: Problem, name="Algorithm"):
        self.name = name
        self.problem = problem
        self.options = ConfigDictionary()

        self.options.declare(name='verbose_level', default=1, lower=0,
                             desc='Verbose level')
    @abstractmethod
    def run(self):
        pass


class Sensitivity(Algorithm):
    def __init__(self, problem, parameters, name='Sensitivity analysis'):
        self.parameters = parameters
        super().__init__(problem, name)

    def run(self):
        parameters = []
        for parameter in self.problem.parameters.items():
            parameters.append(float(parameter[1]['initial_value']))

        for parameter_name in self.parameters:
            parameter_values = []
            population = Population(self.problem)

            index = 0
            selected_parameter = None
            for parameter in self.problem.parameters.items():
                if parameter[0] == parameter_name:
                    selected_parameter = parameter
                    break
                index += 1

            individuals = []
            for i in range(self.problem.max_population_size):
                value = Individual.gen_number(selected_parameter[1]['bounds'], selected_parameter[1]['precision'],
                                              'normal')
                parameters[index] = value
                parameter_values.append(value)
                individual = Individual(parameters.copy(), self.problem)
                individuals.append(individual)

            population.individuals = individuals
            population.evaluate()
            costs = []
            # TODO: Make also for multi-objective
            for individual in population.individuals:
                costs.append(individual.costs)

            self.problem.populations.append(population)