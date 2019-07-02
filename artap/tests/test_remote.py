# import os
# import unittest
#
# from artap.executor import RemoteSSHExecutor
# from artap.problem import Problem
#
#
# class RemoteProblem(Problem):
#     """ Describe simple one objective optimization problem. """
#     def __init__(self, name):
#         parameters = {'x_1': {'initial_value': 10},
#                       'x_2': {'initial_value': 10}}
#         costs = ['F1']
#
#         super().__init__(name, parameters, costs,
#                          working_dir="." + os.sep + "workspace" + os.sep + "remote")
#
#     def evaluate(self, x):
#         return self.executor.eval(x)
#
#     def parse_results(self, content):
#         return [float(content)]
#
#
# class TestRemoteSSHExecutor(unittest.TestCase):
#     """ Tests simple optimization problem where calculation of
#         goal function is performed on remote machine.
#     """
#     def test_remote_python_exec(self):
#         problem = RemoteProblem("TestPythonProblem")
#         problem.executor = RemoteSSHExecutor(problem,
#                                              command="python3",
#                                              model_file="run_exec.py",
#                                              output_file="output.txt")
#
#         result = problem.evaluate([1, 2])
#
#         self.assertAlmostEqual(result[0], 5.0)
#
#     def test_remote_python_input(self):
#         problem = RemoteProblem("TestPythonProblem")
#         problem.executor = RemoteSSHExecutor(problem,
#                                              command="python3",
#                                              model_file="run_input.py",
#                                              input_file="input.txt",  # file is created in eval with specific parameters
#                                              output_file="output.txt")
#
#         result = problem.evaluate([1, 2])
#
#         self.assertAlmostEqual(result[0], 5.0)
#
#     def xtest_remote_octave_exec(self):
#         problem = RemoteProblem("TestOctaveProblem")
#         problem.executor = RemoteSSHExecutor(problem,
#                                              command="octave --no-gui",
#                                              model_file="run_input.m",
#                                              input_file="input.txt", # file is created in eval with specific parameters
#                                              output_file="output.txt")
#
#         result = problem.evaluate([1, 2])
#
#         self.assertAlmostEqual(result[0], 5.0)
#
#     def xtest_remote_matlab_run(self):
#         problem = RemoteProblem("TestMatlabProblem")
#
#         # TODO: for matlab it must be without .m extension
#         problem.executor = RemoteSSHExecutor(problem,
#                                              command="/opt/matlab-R2018b/bin/matlab -nodisplay -nosplash -nodesktop -r",
#                                              model_file="run_input.m",
#                                              input_file="input.txt",  # file is created in eval with specific parameters
#                                              output_file="output.txt")
#
#         result = problem.evaluate([])
#
#         self.assertAlmostEqual(result[0], 5.0)
#
#
# if __name__ == '__main__':
#     unittest.main()
