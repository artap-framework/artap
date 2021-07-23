from PyQt5 import QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import QModelIndex

# TODO: this must be moved out
# -----------------------------------------------------------------------------------------------------
from .antenna import AntennaArray
# -----------------------------------------------------------------------------------------------------

from .editor import Editor


class ProblemWidget(QtWidgets.QWidget):

    def __init__(self, mdi):
        super().__init__()
        self.editor = Editor()
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addWidget(self.editor, 0, 0)
        self.setWindowTitle('Problem')
        self.tree_view = QtWidgets.QTreeView()  # Instantiate the View
        self.layout.addWidget(self.tree_view, 0, 1)
        self.tree_view.clicked.connect(self.onItemClicked)
        self.tree_view.doubleClicked.connect(self.onItemDoubleClicked)
        self.show()
        self.tree_view.show()
        self.custom_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.custom_plot, 1, 0)
        self.custom_plot.show()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout.addWidget(self.sc, 1, 1)
        self.sc.show()

        self.problem = None

    def load_problem(self, problem, code: str):
        self.problem = problem
        self.editor.setText(code)
        self.editor.show()

    def show_results(self, results):
        self.results = results
        self.layout.addChildWidget(self.tree_view)
        self.tree_view.show()
        # self.custom_plot = MplCanvas(self, width=5, height=4, dpi=100)
        self.custom_plot.show()
        # self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.show()
        self.show()

    # ToDo: Make universal from problem script
    def plot_custom_plot(self, canvas, vector, clear=True):
        if clear:
            canvas.axes.cla()

        for fun in self.problem.plot_functions:
            fun(vector)

        canvas.draw()

    def onItemDoubleClicked(self, signal: QModelIndex):
        data = signal.data().split()
        if data[0] == 'vector':
            vector = []
            vector_str = signal.siblingAtColumn(1).data()
            vector_str = vector_str[1:-1]
            vector_list = vector_str.split(',')
            for item in vector_list:
                vector.append(float(item))

            for i in range(1, 7, 1):
                vector_copy = vector.copy()
                for j, number in enumerate(vector_copy):
                    vector_copy[j] = round(number * 2**i) / 2**i
                self.plot_custom_plot(self.custom_plot, vector_copy, clear=False)

    def onItemClicked(self, signal: QModelIndex):
        if type(signal.data()) is str:
            data = signal.data().split()
            if data[0] == 'Individual':
                self.sc.axes.cla()
                item_index = int(data[1])
                population_index = int(signal.parent().data().split()[1])
                for individual in self.results.population(population_index):
                    self.sc.axes.plot(individual.costs[0], individual.costs[1], 'ok')
                    if individual.features['front_number'] == 1:
                        self.sc.axes.plot(individual.costs[0], individual.costs[1], 'or', markersize=12)
                individual = self.results.population(population_index)[item_index]
                self.sc.axes.plot(individual.costs[0], individual.costs[1], 'og', markersize=12)

            elif data[0] == 'Population':
                self.sc.axes.cla()
                population_index = int(data[1])
                for individual in self.results.population(population_index):
                    self.sc.axes.plot(individual.costs[0], individual.costs[1], 'ok')
                    if individual.features['front_number'] == 1:
                        self.sc.axes.plot(individual.costs[0], individual.costs[1], 'or', markersize=12)

            if data[0] == 'vector':
                vector = []
                vector_str = signal.siblingAtColumn(1).data()
                vector_str = vector_str[1:-1]
                vector_list = vector_str.split(',')
                for item in vector_list:
                    vector.append(float(item))
                self.plot_custom_plot(self.custom_plot, vector)
        else:
            pass

        self.sc.axes.grid(True)
        self.sc.draw()


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)