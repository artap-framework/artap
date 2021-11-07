from .algorithm import Algorithm
from .individual import Individual

import time
import numpy as np

try:
    from pymoo.core.problem import ElementwiseProblem
    from pymoo.factory import get_termination
    from pymoo.optimize import minimize

    from pymoo.core.problem import starmap_parallelized_eval
    from multiprocessing.pool import ThreadPool


    class MooProblem(ElementwiseProblem):
        def __init__(self, problem, algorithm, moo_algorithm):
            self.problem = problem
            self.algorithm = algorithm
            self.moo_algorithm = moo_algorithm

            lb = []
            ub = []
            for parameter in self.problem.parameters:
                bounds = parameter['bounds']

                lb.append(bounds[0])
                ub.append(bounds[1])

            # initialize the pool
            if self.algorithm.options["max_processes"] > 1:
                pool = ThreadPool(self.algorithm.options["max_processes"])

                super().__init__(n_var=len(problem.parameters),
                                 n_obj=len(problem.costs),
                                 n_constr=2,
                                 xl=np.array(lb),
                                 xu=np.array(ub),
                                 runner=pool.starmap,
                                 func_eval=starmap_parallelized_eval)
            else:
                super().__init__(n_var=len(problem.parameters),
                                 n_obj=len(problem.costs),
                                 n_constr=2,
                                 xl=np.array(lb),
                                 xu=np.array(ub))

        def _evaluate(self, x, out, *args, **kwargs):
            individual = Individual(list(x))

            # evaluate
            self.algorithm.evaluator.evaluate([individual])

            # append to problem
            inequality_constraints = self.problem.evaluate_inequality_constraints(x)
            inequality_constraints_positive = all(v < 0 for (v) in inequality_constraints)

            if inequality_constraints_positive:
                self.problem.individuals.append(individual)
                # add to population
                individual.population_id = self.moo_algorithm.n_gen

            out["F"] = individual.costs
            out["G"] = inequality_constraints


    class Pymoo(Algorithm):
        def __init__(self, problem, name="pymoo Optimization"):
            super().__init__(problem, name)

            self.options.declare(name='n_iterations', default=50, lower=1,
                                 desc='Maximum evaluations')
            self.options.declare(name='algorithm', default=None,
                                 desc='Algorithm')

        def run(self):
            t_s = time.time()

            self.problem.logger.info("pymoo: {}".format(type(self.options["algorithm"]).__name__))

            moo_algorithm = self.options["algorithm"]
            moo_problem = MooProblem(self.problem, self, moo_algorithm)

            termination = get_termination("n_gen", self.options["n_iterations"])

            moo_algorithm.setup(moo_problem,
                                termination,
                                seed=1,
                                save_history=True,
                                verbose=self.options["verbose_level"] > 0)

            # until the algorithm has no terminated
            while moo_algorithm.has_next():
                # do the next iteration
                moo_algorithm.next()

                # do same more things, printing, logging, storing or even modifying the algorithm object
                # print(moo_algorithm.n_gen, moo_algorithm.evaluator.n_eval)

            # obtain the result objective from the algorithm
            res = moo_algorithm.result()

            t = time.time() - t_s
            self.problem.logger.info("NLopt: elapsed time: {} s".format(t))

            # create last population
            if res.X.ndim == 2:
                for x, f in zip(res.X, res.F):
                    individual = Individual(list(x))
                    individual.costs = list(f)

                    # append to problem
                    self.problem.individuals.append(individual)
                    # add to population
                    individual.population_id = moo_algorithm.n_gen + 1
            else:
                individual = Individual(list(res.X))
                individual.costs = list(res.F)

                # append to problem
                self.problem.individuals.append(individual)
                # add to population
                individual.population_id = moo_algorithm.n_gen + 1

            # sync changed individual informations
            self.problem.data_store.sync_all()

except ImportError:
    print("pymoo is not present test skiped")