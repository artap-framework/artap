import collections
from numpy.random import normal
from random import random


def flatten(l):
    output = []
    if isinstance(l, collections.Iterable):
        for item in l:
            if isinstance(item, collections.Iterable):
                output.append(flatten(item))
            else:
                output.append(item)
    else:
        output.append(l)

    return output


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


class VectorAndNumbers:
    @classmethod
    def gen_number(cls, bounds=None, precision=0, distribution="uniform", p_type="real"):

        number = 0
        if bounds is None:
            bounds = [0, 1]

        if precision == 0:
            precision = 1e-12

        if distribution == "uniform":
            number = random() * (bounds[1] - bounds[0]) + bounds[0]
            number = round(number / precision) * precision

        if distribution == "normal":
            mean = (bounds[0] + bounds[1]) / 2
            std = (bounds[1] - bounds[0]) / 6
            number = normal(mean, std)

        if p_type == "integer":
            number = int(number)

        return number

    @classmethod
    def gen_vector(cls, design_parameters: dict):

        parameters_vector = []
        for parameter in design_parameters:

            if not ('bounds' in parameter):
                bounds = [parameter["initial_value"] * 0.5, parameter["initial_value"] * 1.5]
            else:
                bounds = parameter['bounds']

            if not ('precision' in parameter):
                precision = None
            else:
                precision = parameter['precision']

            if not ('parameter_type' in parameter):
                p_type = "real"
            else:
                p_type = parameter['parameter_type']

            if (precision is None) and (bounds is None):
                parameters_vector.append(cls.gen_number(p_type=p_type))
                continue

            if precision is None:
                parameters_vector.append(cls.gen_number(bounds=bounds, p_type=p_type))
                continue

            if bounds is None:
                parameters_vector.append(cls.gen_number(precision=precision, p_type=p_type))
                continue

            parameters_vector.append(cls.gen_number(bounds, precision))

        return parameters_vector.copy()
