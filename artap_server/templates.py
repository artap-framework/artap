import string
import sqlite3

from artap.enviroment import Enviroment
from artap.datastore import SqliteDataStore
from artap.problem import ProblemDataStore


class WebPagesWriter:

    def __init__(self):

        self.problems_db = Enviroment.artap_root + "problems.db"
        self.table = self.read_problems_db()
        self.static_dir = Enviroment.artap_root + "../artap_server/static/"
        self.connection_problem = None

    def read_problem_db(self, database):
        self.connection_problem = sqlite3.connect(database)
        cursor = self.connection_problem.cursor()
        table_info = cursor.execute("PRAGMA table_info(problem)").fetchall()
        table = []
        line = []

        for item in table_info:
            line.append(item[1])
        table.append(line)

        table_content = cursor.execute("SELECT * FROM problem").fetchall()

        for item in table_content:
            table.append(list(item))

        cursor.close()
        self.connection_problem.close()
        return table

    def read_problems_db(self):
        self.connection_problem = sqlite3.connect(self.problems_db)
        cursor = self.connection_problem.cursor()
        table_info = cursor.execute("PRAGMA table_info(problem)").fetchall()
        table = []
        line = []

        for item in table_info:
            line.append(item[1])
        table.append(line)

        table_content = cursor.execute("SELECT * FROM problem").fetchall()

        for item in table_content:
            table.append(list(item))

        cursor.close()
        self.connection_problem.close()
        return table

    def problems(self):
        self.table_to_html(self.table, link_column=1)
        file = open(self.static_dir + 'problem.html', 'r')
        html_page = file.readlines()
        return html_page

    def problem_details(self, id):
        datastore = SqliteDataStore(new_database=False, problem_id=id)
        problem = ProblemDataStore(datastore)
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
    table = writer.read_problems_db()
    writer.table_to_html(table)
