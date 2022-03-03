Algorithms
==========

==========
CMA_ES
==========
The Covariance Matrix Adaptation Evolution Strategy (CMA-ES) [1] is one of the most effective approaches
for black-box optimization, in which objective functions cannot be specified explicitly in general.
CMA-ES outperformed over 100 black-box optimization approaches for a variety of benchmark problems [2].

The CMA-ES algorithm selects solutions from a multivariate gaussian distribution. Following the evaluation of
all solutions, the solutions are sorted by evaluation values, and the distribution parameters
(i.e., the mean vector and the covariance matrix) are updated depending on the ranking of evaluation values.

==========
EXAMPLE:
==========
1) Importing the necessary packages:

    .. code-block::
        import pylab as plt
        import numpy as np
        from artap.problem import Problem
        from artap.results import Results
        from artap.algorithm_cmaes import CMA_ES
        from artap.benchmark_functions import Sphere

2) Define the problem and it's parameters. Also, specify the goal function.
The problem class, has two methods: a) set, and b) evaluate.


a) set: the main goal of this method is to define the number of parameters and costs.

b) evaluate: this method should be written to define the optimization task.
the evaluate method should give back a list of the calculated objective values.

    .. code-block::
        class Schwefel(Problem):

            def set(self, **kwargs):
                self.name = "Schwefel function"
                self.parameters = [{'name': 'x_1', 'initial_value': 0.1, 'bounds': [0.0, 1.0]}]
                self.costs = [{'name': 'f_1'}]
                self.dimension = kwargs['dimension']
                self.global_optimum = 0.
                self.global_optimum_coords = [0.0 for x in range(self.dimension)]

            def evaluate(self, individual):
                x = individual.vector
                # the goal function
                F1 = 418.9829 - np.sum(x[0] * np.sin(np.sqrt(np.abs(x[0]))))

                return [F1]

3) Initialize the problem and the algorithm, then run the optimization.

    .. code-block::
        # Initialization of the problem
        problem = Schwefel(**{'dimension': 1})

        # Perform the optimization iterating over 100 times on 100 individuals.
        algorithm = CMA_ES(problem)
        algorithm.options['max_population_number'] = 100
        algorithm.options['max_population_size'] = 100
        algorithm.run()

        # Post - processing the results
        # reads in the result values into the b, results class
        results = Results(problem)
        pareto = results.pareto_values()
        print(f'pareto_values : {pareto}')

        # Convergence plot on a selected goal function and parameter
        slice = results.goal_on_parameter('x_1', 'f_1')
        # plot the results
        x = np.array(slice[0]).reshape(-1, 1)
        plt.plot(x, slice[1])
        plt.show()

4) Results:

    .. code-block::
        pareto_values : [[418.9128931874121], [418.9543047341564], [418.9604104187953], [418.9320425054846],\
        [418.9493241466993], [418.77765497251664], [418.89335447765325], [418.91188432398894],\
        [418.9751406800616], [418.6580068445781], [418.91885561383674], [418.7193056797898],\
        [418.975524307711], [418.7676672664302], [418.9829], [418.91307403521546], [418.7888501876938],\
        [418.5941687859346], [418.8699079216806], [418.7633111405555], [418.819782759507], [418.87548299436224],\
        [418.89328582108647], [418.8071808506206], [418.6559433359101], [418.72960587144524], [418.7891015497556],\
        [418.673904937795], [418.7878140561378], [418.88062825953966], [418.72288216054824], [418.54527423945615],\
        [418.97036567413267], [418.6379836234306], [418.8695623784099], [418.72090373604885], [418.96960998091055],\
        [418.83613786351873], [418.81132039741146], [418.8804598278856], [418.9299507415512], [418.7066954166395],\
        [418.8636212091493], [418.9199973280145], [418.89320076658663], [418.9329626460527], [418.92384658258896],\
        [418.8144784406817], [418.8585058572752], [418.8161338371995], [418.8179118543061], [418.846475856013],\
        [418.8419658981732], [418.9829], [418.8557284024206], [418.96380016110874], [418.7269639224331],\
        [418.5165757917205], [418.78617465461974], [418.67240750675705], [418.8334485581726], [418.90529635266483],\
        [418.8510280025222], [418.9640143555625], [418.5736356860878], [418.7824046706408], [418.68321290328265],\
        [418.8524424866185], [418.8656221090973], [418.96298676559616], [418.84048429061176], [418.8452781933185],\
        [418.96501393261275], [418.7877788237759], [418.8399912105109], [418.9829], [418.9829], [418.8191608340117],\
        [418.78773029120543], [418.799725587753], [418.8919996324637], [418.8769635534159], [418.8166426711464], \
        [418.61773534979716], [418.8724637443203], [418.89878556423616], [418.93422429533314], [418.77238523271154],\
        [418.9335760983132], [418.7739139032565], [418.97732353453625], [418.7065928170687], [418.9406470254013],\
        [418.96548485783677], [418.89343306616746], [418.7900723531225],\
        [418.81299238260914], [418.98285850693867], [418.8729931463588], [418.9361634600147]]

        .. figures:: ../figures/schwefel.png

==========
References:
==========
[1] Nikolaus Hansen and Andreas Ostermeier. Completely derandomized self-adaptation in evolution strategies.
Evol. Comput., 9(2):159–195, June 2001. DOI: http://dx.doi.org/10.1162/106365601750190398.

[2] Nikolaus Hansen. The CMA Evolution Strategy: A Comparing Review, pages 75–102. Springer Berlin Heidelberg,
Berlin, Heidelberg, 2006. DOI: https://doi.org/10.1007/3-540-32494-1_4.