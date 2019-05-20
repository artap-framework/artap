
from artap.problem import ProblemSqliteDataStore
from artap.results import GraphicalResults


database_name = "data_kibaszott_jo.sqlite"
problem = ProblemSqliteDataStore(database_name=database_name)

results = GraphicalResults(problem)
results.plot_convergence_chart('F_1')
