import string

from artap.datastore import SqliteDataStore
from artap.problem import ProblemDataStore
from artap.enviroment import Enviroment

from artap.utils import flatten

table =  string.Template(""" <table class="blueTable">
$table
</table> """)

cell_header =  string.Template("<th>$cell</th>")
cell = string.Template("<td>$cell</td>")
cell_hyperlink = string.Template('<td><a href="$link"> $cell</a></td>')
row = string.Template("""<tr>$row</tr>""")

datastore = SqliteDataStore(working_dir = Enviroment.tests_root, new_database= False, filename="datastore.sqlite")
problem = ProblemDataStore(datastore)

population = problem.populations[-1]
n_individuals = len(population.individuals)

table_content = ""

row_content = ""
table_header = []
header = ["ID", "Population ID", "X_1", "F_1"]
for item in header:
        row_content += cell_header.substitute(cell =  item)
table_content += row.substitute(row = row_content) + "\n"

for individual in population.individuals:
    row_content = ""           
    
    individual_list = individual.to_list()    
    merged = flatten(individual_list)
    
    for i in range(len(merged)):
        if i == 0:
            row_content += cell_hyperlink.substitute(cell =  merged[i], link = "index.html")
        else:
            row_content += cell.substitute(cell = merged[i])
    row_content += "\n"
    table_content += row.substitute(row = row_content)

with open('../artap_server/static/problem.tp','r') as file:
    page = string.Template(file.read())
    page_html = page.substitute(content = table.substitute(table = table_content)) 

with open('../artap_server/static/problem.html', 'w') as ofile:
    ofile.write(page_html)
