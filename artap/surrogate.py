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

        # distance in percentage, taking into account bounds
        self.distance_threshold = 0.0

        # stats
        self.eval_counter = 0
        self.predict_counter = 0
        self.eval_stats = True

    def add_data(self, x, y):
        self.x_data.append(x)
        self.y_data.append(y)

    def read_from_data_store(self):
        for individual in self.problem.individuals:
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
    def evaluate(self, individual):
        pass


class SurrogateModelPredict(SurrogateModel):
    def __init__(self, problem):
        super().__init__(problem)

    def evaluate(self, individual):
        values = None
        if self.trained and "predict" in dir(self.problem):
            values = self.problem.predict(individual)
            if values is not None:
                # count prediction
                self.problem.surrogate.predict_counter += 1

        if values is None:
            # evaluate model
            values = self.evaluate_individual(individual)

        # self.problem.logger.info("surrogate: predict / eval counter: {0:5.0f} / {1:5.0f}, total: {2:5.0f}".format(
        #     self.problem.surrogate.predict_counter,
        #     self.problem.surrogate.eval_counter,
        #     self.problem.surrogate.predict_counter + self.problem.surrogate.eval_counter))

        return values

    def evaluate_individual(self, individual):
        # evaluate problem
        value = self.problem.evaluate(individual)
        # increase counter
        self.eval_counter += 1
        # add training date to surrogate model
        self.add_data(individual.vector, value)

        if self.train_step != -1:
            if self.eval_counter % self.train_step == 0:
                # init default regressor
                if self.regressor is None:
                    self.init_default_regressor()

                # train model
                self.train()

        return value


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

