import string
import sqlite3
import os

from artap.enviroment import Enviroment
from artap.datastore import SqliteDataStore
from artap.problem import ProblemDataStore


class WebPagesWriter:

    def __init__(self):
        self.table = self.read_problems()
        self.static_dir = Enviroment.artap_root + "../artap_server/static/"
        self.connection_problem = None

    def read_problems(self):
        table = [["Problem", "Description"]]
        problems = os.listdir("../artap/projects/")
        for problem in problems:
            table.append([problem, ""])

        return table

    def problems(self):
        html_page = self.table_to_html(self.table, link_column=0)
        return html_page

    def problem_details(self, id):
        data_store = SqliteDataStore(new_database=False, problem_id=id)
        problem = ProblemDataStore(data_store)
        html_page = self.table_to_html(problem.to_table())

        return html_page

    def table_to_html(self, table, link_column=None):
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
                    row_content += cell_hyperlink.substitute(cell=line[j], link="problem?id=" + str(line[0]))
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