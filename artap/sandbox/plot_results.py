
from artap.problem import ProblemDataStore
from artap.results import GraphicalResults


database_name = "data_kibaszott_jo.sqlite"
problem = ProblemDataStore(database_name=database_name)

results = GraphicalResults(problem)
results.plot_convergence_chart('F_1')
