from artap.benchmark_functions import BenchmarkFunction
from numpy import exp


class Synthetic2D(BenchmarkFunction):
    """
        Gaussian 2D synthetic test function for testing the robustness.

        Peaks:
        -----
        (1,1) - width 0.3, multiplier 0.7
        (1,3) - width 0.4, multiplier 0.75
        (3,1)*- width 1.0, multiplier 1.0  <- robust solution
        (3,4) - width 0.4, multiplier 1.2  <- global optimum
        (5,2) - width 0.6, multiplier 1.0

        The function is defined on the [0,5], [0,5] region.

        Reference:
        ---------
        Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
        "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
        IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    def set(self, **kwargs):
        self.name = 'Synthetic2D'

        self.set_dimension(**kwargs)
        self.dimension = 2.0
        self.parameters = [{'name': 'x1', 'bounds': [0., 5.]},
                           {'name': 'x2', 'bounds': [0., 5.]}]

        self.global_optimum = 1.21112
        self.global_optimum_coords = [3.0, 4.0]

        self.robust_optimum = 1.0
        self.robust_optimum_coords = [3.0, 1.0]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x1 = x.vector[0]
        x2 = x.vector[1]

        res = 0.7 * exp(-((x1 - 1.) ** 2. + (x2 - 1.) ** 2.) / 0.18) + \
              0.75 * exp(-((x1 - 1.) ** 2. + (x2 - 3.) ** 2.) / 0.32) + \
              exp(-((x1 - 3) ** 2 + (x2 - 1) ** 2) / 2.) + \
              1.2 * exp(-((x1 - 3) ** 2 + (x2 - 4) ** 2) / 0.32) + \
              exp(-((x1 - 5) ** 2. + (x2 - 2) ** 2.) / 0.72)

        return [res]


class Synthetic1D(BenchmarkFunction):
    """
    This function was introduced to test the MEM - multiple-evaluation model schema, to compare it with the single
    evaluation model.

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    def set(self, **kwargs):
        self.name = 'Synthetic1D'

        self.set_dimension(**kwargs)
        self.dimension = 1
        self.parameters = [{'name': 'x1', 'bounds': [0., 12.]}]

        self.global_optimum = 3.23
        self.global_optimum_coords = [11.0]

        self.robust_optimum = 3.23
        self.robust_optimum_coords = [11.0]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x = x.vector[0]

        res = exp(-(x - 1) ** 2. / 0.5) + 2. * exp(-(x - 1.25) ** 2. / 0.045) + 0.5 * exp(-(x - 1.5) ** 2. / 0.0128) + \
              2. * exp(-(x - 1.6) ** 2. / 0.005) + 2.5 * exp(-(x - 1.8) ** 2. / 0.02) + \
              2.5 * exp(-(x - 2.2) ** 2. / 0.02) + 2. * exp(-(x - 2.4) ** 2. / 0.005) + \
              2. * exp(-(x - 2.75) ** 2. / 0.045) + exp(-(x - 3) ** 2. / 0.5) + 2. * exp(-(x - 6.) ** 2. / 0.32) + \
              2.2 * exp(-(x - 7.) ** 2. / 0.18) + 2.4 * exp(-(x - 8.) ** 2. / 0.5) + \
              2.3 * exp(-(x - 9.5) ** 2. / 0.5) + 3.2 * exp(-(x - 11.) ** 2. / 0.18) + 1.2 * exp(
            -(x - 12.) ** 2. / 0.18)

        return [res]


def atom_nd(width, multiplier, x: list, z: list):
    """
    Atomic function to generate an n-dimensional gaussian test function.

    multiplier: the amplitude/peak value of the function
    width: is the divider
    z: represents the zeros of the function
    x: represents the variables
    """
    res = 0
    for i in range(0, len(x)):
        res += (x[i] - z[i]) ** 2.

    res /= -width

    return exp(res) * multiplier


class Synthetic5D(BenchmarkFunction):
    """
       Evaluates a 5 dimensional Gaussian - test function

       Reference:
       ---------
       Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
       "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
       IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    def set(self, **kwargs):
        self.name = 'Synthetic5D'

        self.set_dimension(**kwargs)
        self.dimension = 5.0
        self.parameters = [{'name': 'x1', 'bounds': [0., 5.]},
                           {'name': 'x2', 'bounds': [0., 5.]},
                           {'name': 'x3', 'bounds': [0., 5.]},
                           {'name': 'x4', 'bounds': [0., 5.]},
                           {'name': 'x5', 'bounds': [0., 5.]}]

        self.global_optimum = 1.2
        self.global_optimum_coords = [3.0, 4.0, 1.3, 5.0, 5.0]

        self.robust_optimum = 1.0
        self.robust_optimum_coords = [3.0, 1.0, 3.0, 2.0, 5.0]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x = x.vector

        result = atom_nd(0.3, 0.7, x, [10., 1.0, 6.0, 7.0, 8.0])
        result += atom_nd(0.4, 0.75, x, [1.0, 3.0, 8.0, 9.5, 2.0])
        result += atom_nd(1.0, 1.0, x, [3.0, 1.0, 3.0, 2.0, 5.0])  # robust solution
        result += atom_nd(0.4, 1.2, x, [3.0, 4.0, 1.3, 5.0, 5.0])  # highest peak
        result += atom_nd(0.6, 1.0, x, [5.0, 2.0, 9.6, 7.3, 8.6])
        result += atom_nd(0.5, 0.6, x, [7.5, 8.0, 9.0, 3.2, 4.6])
        result += atom_nd(0.1, 0.5, x, [5.7, 9.3, 2.2, 8.4, 7.1])
        result += atom_nd(1.0, 0.2, x, [5.5, 7.2, 5.8, 2.3, 4.5])
        result += atom_nd(0.2, 0.4, x, [4.7, 3.2, 5.5, 7.1, 3.3])
        result += atom_nd(0.3, 0.1, x, [9.7, 8.4, 0.6, 3.2, 8.5])

        return [result]


class Synthetic10D(BenchmarkFunction):
    """
    Evaluates a 10 dimensional Gaussian - test function

    Reference:
    ---------
    Yew-Soon Ong, Member, IEEE, Prasanth B. Nair, and Kai Yew Lum
    "Max–Min Surrogate-Assisted Evolutionary Algorithm for Robust Design"
    IEEE TRANSACTIONS ON EVOLUTIONARY COMPUTATION, VOL. 10, NO. 4, AUGUST 2006
    """

    def set(self, **kwargs):
        self.name = 'Synthetic5D'

        self.set_dimension(**kwargs)
        self.dimension = 5.0
        self.parameters = [{'name': 'x1', 'bounds': [0., 5.]},
                           {'name': 'x2', 'bounds': [0., 5.]},
                           {'name': 'x3', 'bounds': [0., 5.]},
                           {'name': 'x4', 'bounds': [0., 5.]},
                           {'name': 'x5', 'bounds': [0., 5.]},
                           {'name': 'x6', 'bounds': [0., 5.]},
                           {'name': 'x7', 'bounds': [0., 5.]},
                           {'name': 'x8', 'bounds': [0., 5.]},
                           {'name': 'x9', 'bounds': [0., 5.]},
                           {'name': 'x10', 'bounds': [0., 5.]}]

        self.global_optimum = 1.2
        self.global_optimum_coords = [3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0]

        self.robust_optimum = 1.0
        self.robust_optimum_coords = [3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0]
        # single objective problem
        self.costs = [{'name': 'f_1', 'criteria': 'minimize'}]

    def evaluate(self, x):
        x = x.vector

        result = atom_nd(0.3, 0.7, x, [10., 1.0, 6.0, 7.0, 8.0, 1.0, 1.0, 6.0, 7.0, 8.0])
        result += atom_nd(0.4, 0.75, x, [1.0, 3.0, 8.0, 9.5, 2.0, 1.0, 3.0, 8.0, 9.5, 2.0])
        result += atom_nd(1.0, 1.0, x, [3.0, 1.0, 3.0, 2.0, 5.0, 3.0, 1.0, 3.0, 2.0, 5.0])  # robust solution
        result += atom_nd(0.4, 1.2, x, [3.0, 4.0, 1.3, 5.0, 5.0, 3.0, 4.0, 1.3, 5.0, 5.0])  # highest peak
        result += atom_nd(0.6, 1.0, x, [5.0, 2.0, 9.6, 7.3, 8.6, 5.0, 2.0, 9.6, 7.3, 8.6])
        result += atom_nd(0.5, 0.6, x, [7.5, 8.0, 9.0, 3.2, 4.6, 7.5, 8.0, 9.0, 3.2, 4.6])
        result += atom_nd(0.1, 0.5, x, [5.7, 9.3, 2.2, 8.4, 7.1, 5.7, 9.3, 2.2, 8.4, 7.1])
        result += atom_nd(1.0, 0.2, x, [5.5, 7.2, 5.8, 2.3, 4.5, 5.5, 7.2, 5.8, 2.3, 4.5])
        result += atom_nd(0.2, 0.4, x, [4.7, 3.2, 5.5, 7.1, 3.3, 4.7, 3.2, 5.5, 7.1, 3.3])
        result += atom_nd(0.3, 0.1, x, [9.7, 8.4, 0.6, 3.2, 8.5, 9.7, 8.4, 0.6, 3.2, 8.5])

        return [result]


if __name__ == '__main__':
    test = Synthetic2D()
    test.plot_2d()

    test = Synthetic1D()
    test.plot_1d()
