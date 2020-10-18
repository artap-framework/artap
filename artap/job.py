import time
import sys
from abc import ABCMeta
from .individual import Individual
from .utils import VectorAndNumbers
from math import inf


class Job(metaclass=ABCMeta):
    def __init__(self, problem):
        self.problem = problem

    def evaluate(self, individual):
        # try to calculate the goal function of the individual in case of failure the individual is
        # replaced by another one, at maximum 5 tries

        # Skips calculation of already calculated individual
        if individual.state == individual.State.EVALUATED:
            return

        for i in range(5):
            # info
            individual.features["start_time"] = time.time()
            t_s = time.time()

            # set in progress
            individual.state = individual.State.IN_PROGRESS

            # check the constraints
            constraints = self.problem.evaluate_constraints(individual)

            if constraints:
                individual.features["feasible"] = sum(map(abs, constraints))

            # problem cost function evaluate only in that case when the problem fits the constraints
            try:
                costs = self.problem.surrogate.evaluate(individual)
                individual.costs = costs
                if self.problem is not None:
                    individual.calc_signed_costs(self.problem.signs)  # the idea is to make this conversion only once

                # set evaluated
                individual.state = individual.State.EVALUATED
                # info
                individual.features["finish_time"] = time.time()
                # write to store
                self.problem.data_store.sync_individual(individual)
                return
            except (TimeoutError, RuntimeError) as e:
                print("Job: error:", e)
                failed_individual = Individual(individual.vector)
                failed_individual.state = individual.State.FAILED
                if individual.features["feasible"] == 0.0:
                    individual.features["feasible"] = inf  # TODO: genetic algorithms uses this information, i dont know the
                    # correct solution
                self.problem.failed.append(failed_individual)
                # in the case of failure generate new random individual
                # TODO: create different strategies
                individual.vector = VectorAndNumbers.gen_vector(self.problem.parameters)
                individual.state = individual.State.EMPTY
                continue
            except:
                print("Job: unexpected error:", sys.exc_info()[0])
                raise

        raise RuntimeError("To many failures has appeared.")
