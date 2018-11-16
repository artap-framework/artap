import string
import os

from artap.enviroment import Enviroment
from artap.datastore import SqliteDataStore
from artap.problem import ProblemDataStore


class WebPagesWriter:

    '''
    data_dirs = [".." + os.sep + "artap" + os.sep + "tests" + os.sep + "workspace" + os.sep,
                 ".." + os.sep + "artap" + os.sep + "projects"]
    '''

    data_dirs = [".." + os.sep + "artap" + os.sep + "tests" + os.sep + "workspace" + os.sep]

    def __init__(self):
        self.table = self.read_problems()
        self.static_dir = Enviroment.artap_root + ".." + os.sep + "artap_server" + os.sep + "static" + os.sep
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
        html_page = self.table_to_html(self.table, link_column=[0], page=["calculation"])
        return html_page

    def calculation_details(self, id):
        table = [["Problem", "Description"]]
        index = int(id) + 1
        path = self.table[index][1] + self.table[index][2] + os.sep
        items = os.listdir(path)
        calculations = []

        for item in items:
            if os.path.isdir(path + item):
                calculations.append(path + item + os.sep)
        i = 0
        self.database_files = []
        for problem in calculations:
            file = problem + os.sep + "data.sqlite"
            self.database_files.append(file)
            data_store = SqliteDataStore(database_file=file)
            problem = ProblemDataStore(data_store)
            table.append([i, problem.name, problem.description])
            i += 1
        return self.table_to_html(table, link_column=[1, 2], page=["problem", "problemfig"])

    def problem_details(self, id):
        data_store = SqliteDataStore(database_file=self.database_files[int(id)])
        problem = ProblemDataStore(data_store)
        # html_page = self.table_to_html(problem.to_table(), link_column=[1], page=["item"])
        html_page = self.table_to_html(problem.to_table())
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
                if (link_column != None) and (j in link_column):
                    createLink = {
                        'problems': lambda:  cell_hyperlink.substitute(cell=line[j], link=page[0] + "?id=" + str(line[0])),
                        'calculation': lambda:  cell_hyperlink.substitute(cell=line[j], link=page[0] + "?id=" + str(line[0])),
                        'problem': lambda:  cell_hyperlink.substitute(cell=line[j], link=page[0] + "?id=" + str(line[0])),
                        'problemfig': lambda: cell_hyperlink.substitute(cell=line[j] + " Figure", link=page[1] + "?id=" + str(line[0])),
                    }

                    for currPage in page:
                        funcCreateLink = createLink.get(currPage, lambda: "")
                        row_content += funcCreateLink()

                    # row_content += cell_hyperlink.substitute(cell=line[j], link= page +"?id=" + str(line[0]))
                else:
                    row_content += cell.substitute(cell=line[j], link="index?id=" + str(line[0]))
            row_content += "\n"
            table_content += row.substitute(row=row_content)

        with open(".." + os.sep + "artap_server" + os.sep + "static" + os.sep + "problem.tp", 'r') as file:
            page = string.Template(file.read())
            page_html = page.substitute(content=table_template.substitute(table=table_content))

        return page_html

    '''
    TODO: Generating figures using plotly
    '''

    def problem_figure(self, id):
        data_store = SqliteDataStore(database_file=self.database_files[int(id)])
        problem = ProblemDataStore(data_store)
        html_page = self.table_to_fig(problem.to_table())
        return html_page

    def table_to_fig(self, table, link_column=None, page=None):

        fig_par = string.Template('x_data="$x_axis_vals" y_data="$y_axis_vals" x_label="$x_label_vals" y_label="$y_label_vals"')

        figure_template = string.Template(""" <div id="figure" style="width:1024px;height:720px; "
                                    $fig_params
                                    "></div> """)
        x_axis_data = ''
        y_axis_data = ''

        line = table[0]
        x_label_data = line[1]
        y_label_data = line[2]

        for i in range(1, len(table)):
            line = table[i]
            # for j in range(len(line)):
            x_axis_data += str(line[1]) + ','
            y_axis_data += str(line[2]) + ','

        with open(".." + os.sep + "artap_server" + os.sep + "static" + os.sep + "problem_fig.tp", 'r') as file:
            page = string.Template(file.read())
            page_html = page.substitute(content=figure_template.substitute(fig_params=fig_par.substitute(x_axis_vals=x_axis_data, y_axis_vals=y_axis_data, x_label_vals=x_label_data, y_label_vals=y_label_data)))

        return page_html

if __name__ == "__main__":
    writer = WebPagesWriter()
    print(writer.table_to_html(writer.table))