from abc import ABCMeta, abstractmethod
import math


class SurrogateModel(metaclass=ABCMeta):
    def __init__(self, problem):
        # self.name = name
        self.problem = problem

        # surrogate model
        self.regressor = None

        self.x_data = []
        self.y_data = []

        self.trained = False

        # distance
        self.distance_threshold = 0.0

        # stats
        self.eval_counter = 0
        self.predict_counter = 0
        self.eval_stats = True

    def add_data(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    def read_from_data_store(self):
        for population in self.problem.populations:
            for individual in population.individuals:
                self.add_data(individual.vector, individual.costs)

    def init_default_regressor(self):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self, x, *args):
        pass

    def compute(self, individual):
        return self.problem.evaluate(individual)

    def compute_distance(self, x):
        # n = len(limits)
        dist = float("inf")
        for vector in self.x_data:
            dist_tmp = 0.0
            for k in range(len(vector)):
                d = 100.0 * abs(vector[k] - x[k]) / (self.problem.parameters[k]['bounds'][1] - self.problem.parameters[k]['bounds'][0])
                # print("parameter {0:11.6e}, \tvector {1:11.6e}, \tdiff {2:11.6e}, \tlimits {3:11.6e} \tdistance: {4:4.1f} %".format(x[k], vector[k], abs(x[k] - vector[k]), self.problem.parameters[k]['bounds'][1] - self.problem.parameters[k]['bounds'][0], d))
                # dist_tmp = dist_tmp + d
                dist_tmp = max(dist_tmp, d)
            # average value
            # dist_tmp = dist_tmp / n

            if dist_tmp < dist:
                vec = vector
            dist = min(dist, dist_tmp)

            # for k in range(len(vector)):
            #     d = 100.0 * math.fabs(vec[k] - x[k]) / (self.problem.parameters[k]['bounds'][1] - self.problem.parameters[k]['bounds'][0])
            #     print("parameter {0:11.6e}, \tvector {1:11.6e}, \tdiff {2:11.6e}, \tlimits {3:11.6e} \tdistance: {4:4.1f} %".format(x[k], vector[k], abs(x[k] - vector[k]), self.problem.parameters[k]['bounds'][1] - self.problem.parameters[k]['bounds'][0], d))
            # print("dist min: {0:4.1f} %".format(dist))

        return dist

    @abstractmethod
    def evaluate(self, x):
        pass


class SurrogateModelEval(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)
        self.trained = True

    def train(self):
        pass

    def predict(self, individual):
        return self.problem.evaluate(individual)

    def evaluate(self, individual):
        self.eval_counter += 1
        return self.problem.evaluate(individual)

