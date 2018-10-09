import string
import os

from artap.enviroment import Enviroment
from artap.datastore import SqliteDataStore
from artap.problem import ProblemDataStore


class WebPagesWriter:

    data_dirs = ["../artap/tests/workspace/", "../artap/projects"]

    def __init__(self):
        self.table = self.read_problems()
        self.static_dir = Enviroment.artap_root + "../artap_server/static/"
        self.connection_problem = None

    def read_problems(self):
        table = [["Problem", "Description"]]
        for path in self.data_dirs:
            problems = os.listdir(path)
            i = 0
            for problem in problems:
                table.append([i, path, problem])
                i += 1
        return table

    def problems(self):
        html_page = self.table_to_html(self.table, link_column=0, page="calculation")
        return html_page

    def calculation_details(self, id):
        table = [["Problem", "Description"]]
        index = int(id) + 1
        path = self.table[index][1] + self.table[index][2] + "/"
        items = os.listdir(path)
        calculations = []

        for item in items:
            if os.path.isdir(path + item):
                calculations.append(path + item + "/")
        i = 0
        self.database_files = []
        for problem in calculations:
            file = problem + "/data.sqlite"
            self.database_files.append(file)
            data_store = SqliteDataStore(database_file=file)
            problem = ProblemDataStore(data_store)
            table.append([i, problem.name, problem.description])
            i += 1
        return self.table_to_html(table, link_column=1, page="problem")

    def problem_details(self, id):
        data_store = SqliteDataStore(database_file=self.database_files[int(id)])
        problem = ProblemDataStore(data_store)
        html_page = self.table_to_html(problem.to_table(), link_column=1, page="item")
        return html_page

    def table_to_html(self, table, link_column=None, page=None):
        table_template = string.Template(""" <table class="blueTable">
                                    $table
                                    </table> """)

        cell_header = string.Template("<th>$cell</th>")
        cell = string.Template("<td>$cell</td>")
        cell_hyperlink = string.Template('<td><a href="$link"> $cell</a></td>')
        row = string.Template("""<tr>$row</tr>""")

        table_content = ""
        row_content = ""
        header = table[0]
        for item in header:
            row_content += cell_header.substitute(cell=item)
        table_content += row.substitute(row=row_content) + "\n"

        for i in range(1, len(table)):
            row_content = ""

            line = table[i]
            for j in range(len(line)):
                if (link_column != None) and (j == link_column):
                    row_content += cell_hyperlink.substitute(cell=line[j], link= page +"?id=" + str(line[0]))
                else:
                    row_content += cell.substitute(cell=line[j], link="index?id=" + str(line[0]))
            row_content += "\n"
            table_content += row.substitute(row=row_content)

        with open('../artap_server/static/problem.tp', 'r') as file:
            page = string.Template(file.read())
            page_html = page.substitute(content=table_template.substitute(table=table_content))

        return page_html

if __name__ == "__main__":
    writer = WebPagesWriter()
    print(writer.table_to_html(writer.table))