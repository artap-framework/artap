from abc import abstractmethod

import numpy
import numpy as np

from .individual import Individual
from .algorithm import Algorithm
from .problem import Problem
from .algorithm_genetic import GeneralEvolutionaryAlgorithm
from .operators import RandomGenerator, NoNormalization, ZeroToOneNormalization
from .archive import Archive
from copy import copy, deepcopy


# class LocalSearch(Algorithm):
#
#     def __init__(self,
#                  x0=None,
#                  sampling=RandomGenerator(),
#                  n_sample_points="auto",
#                  n_max_sample_points=20,
#                  **kwargs):
#
#         super().__init__(**kwargs)
#         self.sampling = sampling
#         self.n_sample_points = n_sample_points
#         self.n_max_sample_points = n_max_sample_points
#         self.x0 = x0
#         # self.default_termination = SingleObjectiveSpaceToleranceTermination(n_last=5, tol=1e-8)
#
#         self.is_local_initialized = False
#
#     def _setup(self, problem, x0=None, **kwargs):
#         if self.x0 is None:
#             self.x0 = x0
#
#     def _initialize_infill(self):
#         # calculate the default number of sample points
#         if self.n_sample_points == "auto":
#             self.n_sample_points = min(self.problem.n_var * 5, self.n_max_sample_points)
#
#         # no initial point is provided - sample in bounds and take the best
#         if self.x0 is None:
#             if not self.problem.has_bounds():
#                 raise Exception("Either provide an x0 or a problem with variable bounds!")
#             pop = self.sampling.generate()
#         else:
#             # pop = pop_from_array_or_individual(self.x0)
#             pop = self.sampling.generate()
#
#         return pop
#
#     def _initialize_advance(self, infills=None, **kwargs):
#         super()._initialize_advance(infills=infills, **kwargs)
#
#         self.evaluator.evaluate(infills)
#         # self.x0 = FitnessSurvival().do(self.problem, infills, n_survive=1)[0]
#
#     def _infill(self):
#         if not self.is_local_initialized:
#             return self._local_initialize_infill()
#         else:
#             return self._local_infill()
#
#     def _advance(self, **kwargs):
#         if not self.is_local_initialized:
#             self.is_local_initialized = True
#             return self._local_initialize_advance(**kwargs)
#         else:
#             return self._local_advance(**kwargs)
#
#     def _local_initialize_infill(self, *args, **kwargs):
#         return self._local_infill(*args, **kwargs)
#
#     def _local_initialize_advance(self, *args, **kwargs):
#         return self._local_advance(*args, **kwargs)
#
#     @abc.abstractmethod
#     def _local_infill(self):
#         pass
#
#     @abc.abstractmethod
#     def _local_advance(self, **kwargs):
#         pass


class Termination:

    def __init__(self) -> None:
        """
        Base class for the implementation of a termination criterion for an algorithm.
        """
        super().__init__()

        # the algorithm can be forced to terminate by setting this attribute to true
        self.force_termination = False

    def do_continue(self, algorithm):
        """
        Whenever the algorithm objects wants to know whether it should continue or not it simply
        asks the termination criterion for it.
        Parameters
        ----------
        algorithm : class
            The algorithm object that is asking if it has terminated or not.
        Returns
        -------
        do_continue : bool
            Whether the algorithm has terminated or not.
        """

        if self.force_termination:
            return False
        else:
            return self._do_continue(algorithm)

    # the concrete implementation of the algorithm
    def _do_continue(self, algorithm, **kwargs):
        pass

    def has_terminated(self, algorithm):
        """
        Instead of asking if the algorithm should continue it can also ask if it has terminated.
        (just negates the continue method.)
        """
        return not self.do_continue(algorithm)


class NoTermination(Termination):
    def _do_continue(self, algorithm, **kwargs):
        return True


class MaximumGenerationTermination(Termination):

    def __init__(self, n_max_gen) -> None:
        super().__init__()
        self.n_max_gen = n_max_gen

        if self.n_max_gen is None:
            self.n_max_gen = float("inf")

    def _do_continue(self, algorithm, **kwargs):
        return algorithm.n_gen < self.n_max_gen


class MaximumFunctionCallTermination(Termination):

    def __init__(self, n_max_evals) -> None:
        super().__init__()
        self.n_max_evals = n_max_evals

        if self.n_max_evals is None:
            self.n_max_evals = float("inf")

    def _do_continue(self, algorithm, **kwargs):
        return algorithm.evaluator.n_eval < self.n_max_evals


class CMAES(GeneralEvolutionaryAlgorithm):

    def __init__(self, problem: Problem, name="CMA_ES", evaluator_type=None):
        super().__init__(problem, name, evaluator_type)

        self.options.declare(name='x0', default=None, desc='initial_guess')
        self.options.declare(name='prob_cross', default=1.0, lower=0,
                             desc='prob_cross')

        self.options.declare(name='prob_mutation', default=1.0 / (len(problem.parameters)), lower=0,
                             desc='prob_mutation')
        self.options.declare(name='n_max_sample_points', default=20, desc='number_of_max_sample_points')

        self.n = self.options['max_population_size']
        self.options.declare(name='cmaes_verbose', default=-9, desc='cmaes_verbose')
        self.options.declare(name='verb_log', default=0)
        self.options.declare(name='maxfevals', default=np.inf, desc='maxfevals')
        self.options.declare(name='tolfun', default=1e-11)
        self.options.declare(name='tolx', default=1e-11)

        # set random generator
        self.individual_features['dominate'] = []
        self.individual_features['crowding_distance'] = 0
        self.individual_features['domination_counter'] = 0
        self.individual_features['front_number'] = 0

        self.es = None
        self.cma = None

        self.normalize = True
        self.norm = None
        '''
        Parameters
        ----------
        x0 : list or `numpy.ndarray`
              initial guess of minimum solution
              before the application of the geno-phenotype transformation
              according to the ``transformation`` option.  It can also be
              a string holding a Python expression that is evaluated
              to yield the initial guess - this is important in case
              restarts are performed so that they start from different
              places.  Otherwise ``x0`` can also be a `cma.CMAEvolutionStrategy`
              object instance, in that case ``sigma0`` can be ``None``.
        sigma : float
              Initial standard deviation in each coordinate.
              ``sigma0`` should be about 1/4th of the search domain width
              (where the optimum is to be expected). The variables in
              ``objective_function`` should be scaled such that they
              presumably have similar sensitivity.
              See also `ScaleCoordinates`.
        parallelize : bool
              Whether the objective function should be called for each single evaluation or batch wise.
        restarts : int, default 0
              Number of restarts with increasing population size, see also
              parameter ``incpopsize``, implementing the IPOP-CMA-ES restart
              strategy, see also parameter ``bipop``; to restart from
              different points (recommended), pass ``x0`` as a string.
        restart_from_best : bool, default false
               Which point to restart from
        incpopsize : int
              Multiplier for increasing the population size ``popsize`` before each restart
        eval_initial_x : bool
              Evaluate initial solution, for ``None`` only with elitist option
        noise_handler : class
              A ``NoiseHandler`` class or instance or ``None``. Example:
              ``cma.fmin(f, 6 * [1], 1, noise_handler=cma.NoiseHandler(6))``
              see ``help(cma.NoiseHandler)``.
        noise_change_sigma_exponent : int
              Exponent for the sigma increment provided by the noise handler for
              additional noise treatment. 0 means no sigma change.
        noise_kappa_exponent : int
              Instead of applying reevaluations, the "number of evaluations"
              is (ab)used as scaling factor kappa (experimental).
        bipop : bool
              If `True`, run as BIPOP-CMA-ES; BIPOP is a special restart
              strategy switching between two population sizings - small
              (like the default CMA, but with more focused search) and
              large (progressively increased as in IPOP). This makes the
              algorithm perform well both on functions with many regularly
              or irregularly arranged local optima (the latter by frequently
              restarting with small populations).  For the `bipop` parameter
              to actually take effect, also select non-zero number of
              (IPOP) restarts; the recommended setting is ``restarts<=9``
              and `x0` passed as a string using `numpy.rand` to generate
              initial solutions. Note that small-population restarts
              do not count into the total restart count.
        AdaptSigma : True
              Or False or any CMAAdaptSigmaBase class e.g. CMAAdaptSigmaTPA, CMAAdaptSigmaCSA
        maxfevals : inf
            Maximum number of function evaluations
        tolfun : 1e-11
            Termination criterion: tolerance in function value, quite useful
        tolx : 1e-11
            Termination criterion: tolerance in x-changes
        cmaes_verbose : 3
            Verbosity e.g. of initial/final message, -1 is very quiet, -9 maximally quiet, may not be fully implemented
        verb_log : 1
            Verbosity: write data to files every verb_log iteration, writing can be time critical on fast to
            evaluate functions
        kwargs : dict
              A dictionary with additional options passed to the constructor
              of class ``CMAEvolutionStrategy``, see ``cma.CMAOptions`` ()
              for a list of available options.
        '''
        self.x0 = self.options['x0']
        self.sigma = 0.5
        self.restarts = 0
        self.restart_from_best = 'False'
        self.incpopsize = 2
        self.eval_initial_x = False
        self.noise_handler = None
        self.noise_change_sigma_exponent = 1
        self.noise_kappa_exponent = 0
        self.bipop = False
        self.n_sample_points = "auto"
        self.default_termination = NoTermination()
        self.send_array_to_yield = True
        self.parallelize = True
        self.al = None
        self.sampling = RandomGenerator()

        self.verbose = False
        self.return_least_infeasible = False
        # an algorithm can defined the default termination which can be overwritten
        self.default_termination = None
        # whether the algorithm as terminated or not
        self.has_terminated = None

        self._setup(problem)

    def _setup(self, problem, seed=None, **kwargs):
        self.n_gen = 0

        xl, xu = problem.bounds()
        if self.normalize:
            self.norm, self.options['bounds'] = self.bounds_if_normalize(xl, xu)
        else:
            self.norm = NoNormalization()
            self.options['bounds'] = [xl, xu]

        self.options['seed'] = seed

        if isinstance(self.termination, MaximumGenerationTermination):
            self.options['maxiter'] = self.termination.n_max_gen
        elif isinstance(self.termination, MaximumFunctionCallTermination):
            self.options['maxfevals'] = self.termination.n_max_evals

    def bounds_if_normalize(self, xl, xu):
        norm = ZeroToOneNormalization(xl=xl, xu=xu)

        _xl, _xu = np.zeros_like(xl), np.ones_like(xu)
        if xl is not None:
            _xl[np.isnan(xl)] = np.nan
        if xu is not None:
            _xu[np.isnan(xu)] = np.nan

        return norm, [_xl, _xu]

    def _initialize_advance(self, **kwargs):
        super()._initialize_advance(**kwargs)

        kwargs = dict(
            options=self.options,
            parallelize=self.parallelize,
            restarts=self.restarts,
            restart_from_best=self.restart_from_best,
            incpopsize=self.incpopsize,
            eval_initial_x=self.eval_initial_x,
            noise_handler=self.noise_handler,
            noise_change_sigma_exponent=self.noise_change_sigma_exponent,
            noise_kappa_exponent=self.noise_kappa_exponent,
            bipop=self.bipop)

        x0 = self.norm.forward(self.x0.X)
        # self.es = my_fmin(x0, self.sigma, **kwargs)

        # do this to allow the printout in the first generation
        self.next_X = next(self.es)

    def _local_advance(self, infills=None, **kwargs):

        if infills is not None:

            # set infeasible individual's objective values to np.nan - then CMAES can handle it
            for ind in infills:
                if not ind.feasible[0]:
                    ind.F[0] = np.nan

            F = infills.get("F")[:, 0].tolist()
            if not self.send_array_to_yield:
                F = F[0]

            try:
                self.next_X = self.es.send(F)
            except:
                self.next_X = None

    def has_next(self):
        return not self.has_terminated

    def next(self):

        # get the infill solutions
        infills = self.infill()

        # call the advance with them after evaluation
        if infills is not None:
            self.evaluator.evaluate(infills)
            self.advance(infills=infills)

        # if the algorithm does not follow the infill-advance scheme just call advance
        else:
            self.advance()

    def infill(self):
        if self.problem is None:
            raise Exception("Please call `setup(problem)` before calling next().")

        # the first time next is called simply initial the algorithm - makes the interface cleaner
        if not self.is_initialized:

            # hook mostly used by the class to happen before even to initialize
            self._initialize()

            # execute the initialization infill of the algorithm
            infills = self._initialize_infill()

        else:
            # request the infill solutions if the algorithm has implemented it
            infills = self._infill()

        # set the current generation to the offsprings
        if infills is not None:
            infills.set("n_gen", self.n_gen)

        return infills

    def advance(self, infills=None, **kwargs):

        # if infills have been provided set them as offsprings and feed them into advance
        self.off = infills

        # if the algorithm has not been already initialized
        if not self.is_initialized:

            # set the generation counter to 1
            self.n_gen = 1

            # assign the population to the algorithm
            self.pop = infills

            # do whats necessary after the initialization
            self._initialize_advance(infills=infills, **kwargs)

            # set this algorithm to be initialized
            self.is_initialized = True

        else:

            # increase the generation counter by one
            self.n_gen += 1

            # call the implementation of the advance method - if the infill is not None
            self._advance(infills=infills, **kwargs)

        # execute everything which needs to be done after having the algorithm advanced to the next generation
        self._post_advance()

        # set whether the algorithm has terminated or not
        self.has_terminated = not self.termination.do_continue(self)

        # if the algorithm has terminated call the finalize method
        if self.has_terminated:
            return self.finalize()

    def _post_advance(self):

        # update the current optimum of the algorithm
        self._set_optimum()

        # display the output if defined by the algorithm
        if self.verbose and self.display is not None:
            self.display.do(self.problem, self.evaluator, self, pf=self.pf)

        # if a callback function is provided it is called after each iteration
        if self.callback is not None:
            if isinstance(self.callback, Callback):
                self.callback.notify(self)
            else:
                self.callback(self)

        if self.save_history:
            _hist, _callback = self.history, self.callback

            self.history, self.callback = None, None
            obj = copy.deepcopy(self)

            self.history, self.callback = _hist, _callback
            self.history.append(obj)

    def run(self):
        start = time.time()
        self.problem.logger.info("PSOGA: {}/{}".format(self.options['max_population_number'],
                                                       self.options['max_population_size']))





        t = time.time() - start
        self.problem.logger.info("PSOGA: elapsed time: {} s".format(t))
        # sync changed individual informations
        self.problem.data_store.sync_all()
