import numpy as np

from artap.problem import Problem
from artap.algorithm_scipy import ScipyNelderMead
from artap.algorithm_bayesopt import BayesOptParallel

class MOR(Problem):
    """ Describe simple one objective optimization problem. """

    def __init__(self, name):
        self.max_population_number = 1
        self.max_population_size = 1

        parameters = {'x_1': {'initial_value': 1, 'bounds': [-1, 1]},
                      'x_2': {'initial_value': 1, 'bounds': [-1, 1]},
                      'x_3': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_4': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_5': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_6': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_7': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_8': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_9': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_10': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_11': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_12': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_13': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_14': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_15': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_16': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_17': {'initial_value': 1, 'bounds': [-1200, 1200]},
                      'x_18': {'initial_value': 0, 'bounds': [-1200, 1200]},
                      'x_19': {'initial_value': 0, 'bounds': [-1200, 1200]},
                      'x_20': {'initial_value': 1, 'bounds': [-1200, 1200]},
                      'x_21': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_22': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_23': {'initial_value': 0, 'bounds': [-1, 1]},
                      'x_24': {'initial_value': 0, 'bounds': [-1, 1]}
                      }

        costs = ['F_1']
        working_dir = "./workspace/common_data/"
        super().__init__(name, parameters, costs, working_dir=working_dir, save_data=False)

    def eval(self, x):
        y_ref = [0.,            8.26672748,  16.1095779,    23.51397124,   30.54870382,
                  37.27974682,   43.76148115,   50.03776958,   56.14389772,   62.10826998,
                  67.9537837,    73.69892948,   79.35867046,   84.94514481,   90.4682271,
                  95.93597674,  101.35499652, 106.73071908,  112.06763605,  117.3694812,
                  122.63937704,  127.87995208,  133.09343473,  138.28172848,  143.44647224,
                  148.58908866, 153.71082291,  158.81277396,  163.8959196,   168.9611367,
                  174.00921754,  179.04088301,  184.0567933,   189.05755661,  194.04373627,
                  199.0158565,   203.97440724,  208.91984804,  213.85261136,  218.77310531,
                  223.68171593,  228.57880913,  233.46473235,  238.33981601,  243.2043747,
                  248.0587083,   252.90310287,  257.73783157,  262.56315534,  267.37932363,
                  272.186575,    276.98513767,  281.77523006,  286.55706127,  291.33083151,
                  296.09673252,  300.85494798,  305.60565385,  310.34901872,  315.08520416,
                  319.81436502,  324.53664969,  329.25220042,  333.96115358,  338.66363989,
                  343.35978468,  348.04970813,  352.73352546,  357.41134714,  362.08327915,
                  366.74942308,  371.40987639,  376.06473255,  380.71408121,  385.35800837,
                  389.99659651,  394.6299248,   399.25806914,  403.8811024,   408.49909448,
                  413.11211246,  417.7202207,   422.32348099,  426.92195262,  431.51569251,
                  436.1047553,   440.68919343,  445.26905728,  449.8443952,   454.41525362,
                  458.98167714,  463.54370859,  468.10138913,  472.65475827,  477.20385399,
                  481.74871279,  486.28936974, 490.82585854,  495.35821159,  499.88646005]

        A_bar = np.array([[x[0], x[1], x[2], x[3]],
                          [x[4], x[5], x[6], x[7]],
                          [x[8], x[9], x[10], x[11]],
                          [x[12], x[13], x[14], x[15]]
                          ])

        B_bar = np.array([x[16], x[17], x[18], x[19]])

        C_bar = np.array([x[20], x[21], x[22], x[23]])

        t_max = 25
        N = 100
        x0 = np.array([0, 0, 0, 0])
        n = len(x0)
        t = np.linspace(0, t_max, N)

        x = np.zeros([n, N])
        y = np.zeros(N)
        u = np.zeros(N)
        u[:] = 1

        # u[0:10] = 3.5
        # u[11:50] = 2
        # u[50:70] = 0.5
        # u[70:] = 0.01

        x[:, 0] = x0
        y[0] = np.dot(C_bar, x0)

        for i in range(1, N):
            x[:, i] = np.dot(A_bar, x[:, i - 1]) + np.dot(B_bar, u[i])
            y[i] = np.dot(C_bar, x[:, i])

        result = 0

        for i in  range(len(y)):
            result += abs(y_ref[i] - y[i]) / N

        print(result)
        print(A_bar)
        print(B_bar)
        print(C_bar)
        return result


if __name__ == '__main__':
    problem = MOR("MorProblem")
    algorithm = ScipyNelderMead(problem)
    #algorithm = BayesOptParallel(problem)
    #algorithm.options['verbose_level'] = 0
    #algorithm.options['n_iter_relearn'] = 20
    #algorithm.options['n_iterations'] = 500
    algorithm.run()
    optimum = problem.populations[-1].individuals[-1].costs[0]  # Takes last cost function

