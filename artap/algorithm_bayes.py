from .problem import Problem
from .algorithm import Algorithm
from .job import Job

import warnings
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize

from sklearn.gaussian_process.kernels import Matern
from sklearn.gaussian_process import GaussianProcessRegressor

"""
Parts from 

author='Fernando Nogueira'
https://github.com/fmfn/BayesianOptimization'
author_email="fmfnogueira@gmail.com"
description='A Python implementation of global optimization with gaussian processes.'
"""


class Bayes(Algorithm):
    """ BayesOpt algorithms """

    def __init__(self, problem: Problem, name="BayesOpt"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='l_type', default='L_EMPIRICAL', values=_l_type,
                             desc='Type of learning for the kernel params')
        self.options.declare(name='sc_type', default='SC_MAP', values=_sc_type,
                             desc='Type of learning for the kernel params')
        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum BayesOpt evaluations')
        self.options.declare(name='init_method', default=1,
                             desc='Init method') # 1-LHS, 2-Sobol
        self.options.declare(name='n_init_samples', default=10, lower=1,
                             desc='Number of samples before optimization')
        self.options.declare(name='n_iter_relearn', default=10, lower=1,
                             desc='Number of samples before relearn kernel')
        self.options.declare(name='surr_name', default='sGaussianProcessML', values=_surr_name,
                             desc='Name of the surrogate function')
        self.options.declare(name='surr_noise', default=1e-10, lower=0.0,
                             desc='Variance of observation noise')


class BayesSerial(Bayes):
    def __init__(self, algorithm):
        n = len(algorithm.problem.parameters)
        super().__init__(n)

        # algorithm
        self.algorithm = algorithm

        # Size design variables.
        self.lb = np.empty((n,))
        self.ub = np.empty((n,))
        self.params = {}

        self.job = Job(self.algorithm.problem)

    def evaluateSample(self, x):
        return self.job.evaluate_scalar(x)

# class BayesOptSerial(BayesOpt):
#     """ BayesOpt algorithms """
#
#     def __init__(self, problem: Problem, name="BayesOpt"):
#         super().__init__(problem, name)
#
#         self.bo = BayesOptClassSerial(self)
#
#     def run(self):
#         # Figure out bounds vectors.
#         i = 0
#         for id in self.problem.parameters:
#             bounds = self.problem.parameters[id]['bounds']
#
#             self.bo.lb[i] = bounds[0]
#             self.bo.ub[i] = bounds[1]
#
#             i += 1
#
#         # set bayesopt
#         self.bo.params['n_iterations'] = self.options['n_iterations']
#         self.bo.params['n_init_samples'] = self.options['n_init_samples']
#         self.bo.params['n_iter_relearn'] = self.options['n_iter_relearn']
#         self.bo.params['surr_name'] = self.options['surr_name']
#         self.bo.params['surr_noise'] = self.options['surr_noise']
#         self.bo.params['init_method'] = self.options['init_method']
#         self.bo.params['l_type'] = self.options['l_type']
#         self.bo.params['sc_type'] = self.options['sc_type']
#         self.bo.params['verbose_level'] = self.options['verbose_level']
#
#         t_s = time.time()
#         self.problem.logger.info("BayesOpt: surr_name{}".format(self.options['surr_name']))
#         mvalue, x_out, error = self.bo.optimize()
#         t = time.time() - t_s
#         self.problem.logger.info("BayesOpt: elapsed time: {} s".format(t))
#
#         if error != 0:
#             print('Optimization FAILED.')
#             print("Error", error)
#             print('-' * 35)
#         else:
#             pass
#             # print('Optimization Complete, %f seconds' % (clock() - start))
#             # print("Result", x_out, mvalue)
#             # print('-' * 35)

class Queue:
    def __init__(self):
        self._queue = []

    @property
    def empty(self):
        return len(self) == 0

    def __len__(self):
        return len(self._queue)

    def __next__(self):
        if self.empty:
            raise StopIteration("Queue is empty, no more objects to retrieve.")
        obj = self._queue[0]
        self._queue = self._queue[1:]
        return obj

    def next(self):
        return self.__next__()

    def add(self, obj):
        """Add object to end of queue."""
        self._queue.append(obj)


# class Observable(object):
#     """
#
#     Inspired/Taken from
#         https://www.protechtraining.com/blog/post/879#simple-observer
#     """
#     def __init__(self, events):
#         # maps event names to subscribers
#         # str -> dict
#         self._events = {event: dict() for event in events}
#
#     def get_subscribers(self, event):
#         return self._events[event]
#
#     def subscribe(self, event, subscriber, callback=None):
#         if callback == None:
#             callback = getattr(subscriber, 'update')
#         self.get_subscribers(event)[subscriber] = callback
#
#     def unsubscribe(self, event, subscriber):
#         del self.get_subscribers(event)[subscriber]
#
#     def dispatch(self, event):
#         for _, callback in self.get_subscribers(event).items():
#             callback(event, self)


def acq_max(ac, gp, y_max, bounds, random_state, n_warmup=100000, n_iter=250):
    """
    A function to find the maximum of the acquisition function

    It uses a combination of random sampling (cheap) and the 'L-BFGS-B'
    optimization method. First by sampling `n_warmup` (1e5) points at random,
    and then running L-BFGS-B from `n_iter` (250) random starting points.

    Parameters
    ----------
    :param ac:
        The acquisition function object that return its point-wise value.

    :param gp:
        A gaussian process fitted to the relevant data.

    :param y_max:
        The current maximum known value of the target function.

    :param bounds:
        The variables bounds to limit the search of the acq max.

    :param random_state:
        instance of np.RandomState random number generator

    :param n_warmup:
        number of times to randomly sample the aquisition function

    :param n_iter:
        number of times to run scipy.minimize

    Returns
    -------
    :return: x_max, The arg max of the acquisition function.
    """

    # Warm up with random points
    x_tries = random_state.uniform(bounds[:, 0], bounds[:, 1],
                                   size=(n_warmup, bounds.shape[0]))
    ys = ac(x_tries, gp=gp, y_max=y_max)
    x_max = x_tries[ys.argmax()]
    max_acq = ys.max()

    # Explore the parameter space more throughly
    x_seeds = random_state.uniform(bounds[:, 0], bounds[:, 1],
                                   size=(n_iter, bounds.shape[0]))
    for x_try in x_seeds:
        # Find the minimum of minus the acquisition function
        res = minimize(lambda x: -ac(x.reshape(1, -1), gp=gp, y_max=y_max),
                       x_try.reshape(1, -1),
                       bounds=bounds,
                       method="L-BFGS-B")

        # See if success
        if not res.success:
            continue

        # Store it if better than previous minimum(maximum).
        if max_acq is None or -res.fun[0] >= max_acq:
            x_max = res.x
            max_acq = -res.fun[0]

    # Clip output to make sure it lies within the bounds. Due to floating
    # point technicalities this is not always the case.
    return np.clip(x_max, bounds[:, 0], bounds[:, 1])


class UtilityFunction(object):
    """
    An object to compute the acquisition functions.
    """

    def __init__(self, kind, kappa, xi):
        """
        If UCB is to be used, a constant kappa is needed.
        """
        self.kappa = kappa

        self.xi = xi

        if kind not in ['ucb', 'ei', 'poi']:
            err = "The utility function " \
                  "{} has not been implemented, " \
                  "please choose one of ucb, ei, or poi.".format(kind)
            raise NotImplementedError(err)
        else:
            self.kind = kind

    def utility(self, x, gp, y_max):
        if self.kind == 'ucb':
            return self._ucb(x, gp, self.kappa)
        if self.kind == 'ei':
            return self._ei(x, gp, y_max, self.xi)
        if self.kind == 'poi':
            return self._poi(x, gp, y_max, self.xi)

    @staticmethod
    def _ucb(x, gp, kappa):
        mean, std = gp.predict(x, return_std=True)

        return mean + kappa * std

    @staticmethod
    def _ei(x, gp, y_max, xi):
        mean, std = gp.predict(x, return_std=True)

        z = (mean - y_max - xi)/std
        return (mean - y_max - xi) * norm.cdf(z) + std * norm.pdf(z)

    @staticmethod
    def _poi(x, gp, y_max, xi):
        mean, std = gp.predict(x, return_std=True)

        z = (mean - y_max - xi)/std
        return norm.cdf(z)


def ensure_rng(random_state=None):
    """
    Creates a random number generator based on an optional seed.  This can be
    an integer or another random state for a seeded rng, or None for an
    unseeded rng.
    """
    if random_state is None:
        random_state = np.random.RandomState()
    elif isinstance(random_state, int):
        random_state = np.random.RandomState(random_state)
    else:
        assert isinstance(random_state, np.random.RandomState)
    return random_state


class TargetSpace(object):
    """
    Holds the param-space coordinates (X) and target values (Y)
    Allows for constant-time appends while ensuring no duplicates are added

    Example
    -------
    >>> def target_func(p1, p2):
    >>>     return p1 + p2
    >>> pbounds = {'p1': (0, 1), 'p2': (1, 100)}
    >>> space = TargetSpace(target_func, pbounds, random_state=0)
    >>> x = space.random_points(1)[0]
    >>> y = space.register_point(x)
    >>> assert self.max_point()['max_val'] == y
    """
    def __init__(self, target_func, pbounds, random_state=None):
        """
        Parameters
        ----------
        target_func : function
            Function to be maximized.

        pbounds : dict
            Dictionary with parameters names as keys and a tuple with minimum
            and maximum values.

        random_state : int, RandomState, or None
            optionally specify a seed for a random number generator
        """
        self.random_state = ensure_rng(random_state)

        # The function to be optimized
        self.target_func = target_func

        # Get the name of the parameters
        self._keys = sorted(pbounds)
        # Create an array with parameters bounds
        self._bounds = np.array(
            [item[1] for item in sorted(pbounds.items(), key=lambda x: x[0])],
            dtype=np.float
        )

        # preallocated memory for X and Y points
        self._params = np.empty(shape=(0, self.dim))
        self._target = np.empty(shape=(0))

        # keep track of unique points we have seen so far
        self._cache = {}

    def __contains__(self, x):
        return tuple(map(float, x)) in self._cache
        # return _hashable(x) in self._cache

    def __len__(self):
        assert len(self._params) == len(self._target)
        return len(self._target)

    @property
    def empty(self):
        return len(self) == 0

    @property
    def params(self):
        return self._params

    @property
    def target(self):
        return self._target

    @property
    def dim(self):
        return len(self._keys)

    @property
    def keys(self):
        return self._keys

    @property
    def bounds(self):
        return self._bounds

    def params_to_array(self, params):
        try:
            assert set(params) == set(self.keys)
        except AssertionError:
            raise ValueError(
                "Parameters' keys ({}) do ".format(sorted(params)) +
                "not match the expected set of keys ({}).".format(self.keys)
            )
        return np.asarray([params[key] for key in self.keys])

    def array_to_params(self, x):
        try:
            assert len(x) == len(self.keys)
        except AssertionError:
            raise ValueError(
                "Size of array ({}) is different than the ".format(len(x)) +
                "expected number of parameters ({}).".format(len(self.keys))
            )
        return dict(zip(self.keys, x))

    def _as_array(self, x):
        try:
            x = np.asarray(x, dtype=float)
        except TypeError:
            x = self.params_to_array(x)

        x = x.ravel()
        try:
            assert x.size == self.dim
        except AssertionError:
            raise ValueError(
                "Size of array ({}) is different than the ".format(len(x)) +
                "expected number of parameters ({}).".format(len(self.keys))
            )
        return x

    def register(self, params, target):
        """
        Append a point and its target value to the known data.

        Parameters
        ----------
        x : ndarray
            a single point, with len(x) == self.dim

        y : float
            target function value

        Raises
        ------
        KeyError:
            if the point is not unique

        Notes
        -----
        runs in ammortized constant time

        Example
        -------
        >>> pbounds = {'p1': (0, 1), 'p2': (1, 100)}
        >>> space = TargetSpace(lambda p1, p2: p1 + p2, pbounds)
        >>> len(space)
        0
        >>> x = np.array([0, 0])
        >>> y = 1
        >>> space.add_observation(x, y)
        >>> len(space)
        1
        """
        x = self._as_array(params)
        if x in self:
            raise KeyError('Data point {} is not unique'.format(x))

        # Insert data into unique dictionary
        self._cache[tuple(map(float, x.ravel()))] = target

        self._params = np.concatenate([self._params, x.reshape(1, -1)])
        self._target = np.concatenate([self._target, [target]])

    def probe(self, params):
        """
        Evaulates a single point x, to obtain the value y and then records them
        as observations.

        Notes
        -----
        If x has been previously seen returns a cached value of y.

        Parameters
        ----------
        x : ndarray
            a single point, with len(x) == self.dim

        Returns
        -------
        y : float
            target function value.
        """
        x = self._as_array(params)

        try:
            target = self._cache[tuple(map(float, x))]
        except KeyError:
            params = dict(zip(self._keys, x))
            target = self.target_func(**params)
            self.register(x, target)
        return target

    def random_sample(self):
        """
        Creates random points within the bounds of the space.

        Returns
        ----------
        data: ndarray
            [num x dim] array points with dimensions corresponding to `self._keys`

        Example
        -------
        >>> target_func = lambda p1, p2: p1 + p2
        >>> pbounds = {'p1': (0, 1), 'p2': (1, 100)}
        >>> space = TargetSpace(target_func, pbounds, random_state=0)
        >>> space.random_points(1)
        array([[ 55.33253689,   0.54488318]])
        """
        # TODO: support integer, category, and basic scipy.optimize constraints
        data = np.empty((1, self.dim))
        for col, (lower, upper) in enumerate(self._bounds):
            data.T[col] = self.random_state.uniform(lower, upper, size=1)
        return data.ravel()

    def max(self):
        """Get maximum target value found and corresponding parametes."""
        try:
            res = {
                'target': self.target.max(),
                'params': dict(
                    zip(self.keys, self.params[self.target.argmax()])
                )
            }
        except ValueError:
            res = {}
        return res

    def res(self):
        """Get all target values found and corresponding parametes."""
        params = [dict(zip(self.keys, p)) for p in self.params]

        return [
            {"target": target, "params": param}
            for target, param in zip(self.target, params)
        ]

    def set_bounds(self, new_bounds):
        """
        A method that allows changing the lower and upper searching bounds

        Parameters
        ----------
        new_bounds : dict
            A dictionary with the parameter name and its new bounds
        """
        for row, key in enumerate(self.keys):
            if key in new_bounds:
                self._bounds[row] = new_bounds[key]


# class BayesianOptimization(Observable):
class BayesianOptimization(object):
    def __init__(self, f, pbounds, random_state=None, verbose=2):
        """"""
        self._random_state = ensure_rng(random_state)

        # Data structure containing the function to be optimized, the bounds of
        # its domain, and a record of the evaluations we have done so far
        self._space = TargetSpace(f, pbounds, random_state)

        # queue
        self._queue = Queue()

        # Internal GP regressor
        self._gp = GaussianProcessRegressor(
            kernel=Matern(nu=2.5),
            alpha=1e-6,
            normalize_y=True,
            n_restarts_optimizer=25,
            random_state=self._random_state,
        )

        self._verbose = verbose
        # super(BayesianOptimization, self).__init__(events=DEFAULT_EVENTS)
        super(BayesianOptimization, self).__init__()

    @property
    def space(self):
        return self._space

    @property
    def max(self):
        return self._space.max()

    @property
    def res(self):
        return self._space.res()

    def register(self, params, target):
        """Expect observation with known target"""
        self._space.register(params, target)
        # self.dispatch(Events.OPTMIZATION_STEP)

    def probe(self, params, lazy=True):
        """Probe target of x"""
        if lazy:
            self._queue.add(params)
        else:
            self._space.probe(params)
            # self.dispatch(Events.OPTMIZATION_STEP)

    def suggest(self, utility_function):
        """Most promissing point to probe next"""
        if len(self._space) == 0:
            return self._space.array_to_params(self._space.random_sample())

        # Sklearn's GP throws a large number of warnings at times, but
        # we don't really need to see them here.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if len(self._space.params) % 5 == 0:
                self._gp.fit(self._space.params, self._space.target)

        # Finding argmax of the acquisition function.
        suggestion = acq_max(
            ac=utility_function.utility,
            gp=self._gp,
            y_max=self._space.target.max(),
            bounds=self._space.bounds,
            random_state=self._random_state
        )

        return self._space.array_to_params(suggestion)

    def _prime_queue(self, init_points):
        """Make sure there's something in the queue at the very beginning."""
        if self._queue.empty and self._space.empty:
            init_points = max(init_points, 1)

        for _ in range(init_points):
            self._queue.add(self._space.random_sample())

    def _prime_subscriptions(self):
        #if not any([len(subs) for subs in self._events.values()]):
        #    _logger = _get_default_logger(self._verbose)
        #    self.subscribe(Events.OPTMIZATION_START, _logger)
        #    self.subscribe(Events.OPTMIZATION_STEP, _logger)
        #    self.subscribe(Events.OPTMIZATION_END, _logger)
        pass

    def maximize(self,
                 init_points=5,
                 n_iter=25,
                 acq='ucb',
                 kappa=2.576,
                 xi=0.0,
                 **gp_params):
        """Mazimize your function"""
        self._prime_subscriptions()
        # self.dispatch(Events.OPTMIZATION_START)
        self._prime_queue(init_points)
        self.set_gp_params(**gp_params)

        util = UtilityFunction(kind=acq, kappa=kappa, xi=xi)
        iteration = 0
        while not self._queue.empty or iteration < n_iter:
            try:
                x_probe = next(self._queue)
            except StopIteration:
                x_probe = self.suggest(util)
                iteration += 1

            self.probe(x_probe, lazy=False)

        # self.dispatch(Events.OPTMIZATION_END)

    def set_bounds(self, new_bounds):
        """
        A method that allows changing the lower and upper searching bounds

        Parameters
        ----------
        new_bounds : dict
            A dictionary with the parameter name and its new bounds
        """
        self._space.set_bounds(new_bounds)

    def set_gp_params(self, **params):
        self._gp.set_params(**params)