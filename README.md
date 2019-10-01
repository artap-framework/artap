# Ārtap

Ārtap is a framework for robust design optimization in Python. It contains an integrated, multi-physical FEM solver: Agros suite, furthermore it provides simple interfaces for commercial FEM solvers (COMSOL) and meta-heuristic, bayesian or neural network based optimization algorithms surrogate modelling techniques and neural networks.

## Installation

Artap and its dependencies are available as wheel packages for Windows and Linux* distributions:
We recommend to install Artap under a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

    pip install --upgrade pip # make sure that pip is reasonably new
    pip install artap

*The Windows versions are only partially, the linux packages are fully supported at the current version.

## Basic usage

The goal of this example to show, how we can use Artap to solve a simple, bi-objective optimization problem.

The problem is defined in the following way [GDE3]:

    Minimize f1 = x1
    Minimize f2 = (1+x2) / x1

    subject to
            x1 e [0.1, 1]
            x2 e [0, 5]

The Pareto - front of the following problem is known, it is a simple hyperbola. This problem is very simple for an Evolutionary algorithm, it finds its solution within 20-30 generations.
 NSGA - II algorithm is used to solve this example.

### The Problem definition and solution with NSGA-II in Ārtap:

    class BiObjectiveTestProblem(Problem):

        def set(self):

            self.name = 'Biobjective Test Problem'
            
            self.parameters = [{'name':'x_1', 'bounds': [0.1, 1.]},
                               {'name':'x_2', 'bounds': [0.0, 5.0]}]

            self.costs = [{'name': 'f_1', 'criteria': 'minimize'},
                          {'name': 'f_2', 'criteria': 'minimize'}]

        def evaluate(self, individual):
            f1 = individual.vector[0]
            f2 = (1+individual.vector[1])/individual.vector[0]
        return [f1, f2]
 
    # Perform the optimization iterating over 100 times on 100 individuals.
    problem = BiObjectiveTestProblem()
    algorithm = NSGAII(problem)
    algorithm.options['max_population_number'] = 100
    algorithm.options['max_population_size'] = 100
    algorithm.run()

## References

* [GDE3] Saku Kukkonen, Jouni Lampinen, The third Evolution Step of Generalized Differential Evolution


## Citing

If you use Ārtap in your research, the developers would be grateful if you would cite the relevant publications:

[1] David Pánek, Tamás Orosz, Pavel Karban, Artap: Robust design optimization framework for engineering applications, in: The Third International Conference on Intelligent Computing in Data Sciences ICDS2019, IEEE, 2019, pp. 1–5, [in press]

### Applications
[2] Karban, P., Pánek, D., & Doležel, I. (2018). Model of induction brazing of nonmagnetic metals using model order reduction approach. COMPEL-The international journal for computation and mathematics in electrical and electronic engineering, 37(4), 1515-1524.

[3] Pánek, D., Orosz, T., Kropík, P., Karban, P., & Doležel, I. (2019, June). Reduced-Order Model Based Temperature Control of Induction Brazing Process. In 2019 Electric Power Quality and Supply Reliability Conference (PQ) & 2019 Symposium on Electrical Engineering and Mechatronics (SEEM) (pp. 1-4). IEEE.

[4] Pánek, D., Karban, P., & Doležel, I. (2019). Calibration of Numerical Model of Magnetic Induction Brazing. IEEE Transactions on Magnetics, 55(6), 1-4.

## Contact

If you have any questions, do not hesitate to contact us: artap.team@gmail.com

## License

Ārtap is published under [MIT license](https://en.wikipedia.org/wiki/MIT_License)
