import os
from artap.executor import LocalAnsysExecutor
from artap.problem import Problem
from artap.algorithm_scipy import ScipyOpt
from artap.results import Results
from artap.algorithm_genetic import NSGAII

class AnsysProblem(Problem):
    """ Describe simple one objective optimization problem."""

    def set(self):
        self.name = "AnsysProblem"

        # Parameters must be defined in the Ansys model
        self.parameters = [{'name': 'pp', 'initial_value': 0.8, 'bounds': [0.5, 0.9]},
                           {'name': 'p_offset', 'initial_value': 0.8, 'bounds': [0.5, 0.9]}]

        self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
        self.output_files = ["output.txt"]

        # Executor serves for calling the Ansys
        self.executor = LocalAnsysExecutor(self,
                                          script_file="example_conductor.py",
                                          output_files=["output.txt"])

    # Calculate the value of the objective function
    def evaluate(self, individual):
        cog = self.executor.eval(individual)[0]  # method evaluate must return list
        return [cog]

    # This method processes files generated by 3rd party software, depends on files format
    def parse_results(self, output_files, individual):
        with open(output_files[0]) as file:
            content = file.readlines()
            content = content[0]
            content = content.split(',')
            content = [float(i) for i in content[:-1]]
            cogging_torque = max(content) - min(content)
            print('cogging:', cogging_torque)
        return [cogging_torque]


problem = AnsysProblem()        # Creating problem
algorithm  = NSGAII(problem)
algorithm.options['max_population_number'] = 5
algorithm.options['max_population_size'] = 4
algorithm.run()


# Post - processing the results
results = Results(problem)

res_individual = results.find_optimum()
print(res_individual.vector)
for i in range(len(problem.parameters)):
    print("{} : {}".format(problem.parameters[i].get("name"), res_individual.vector[i]))
