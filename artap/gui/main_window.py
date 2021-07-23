# Internal imports
from .new_problem import NewProblemWizard
from .log_window import LogWindow
from .problem_widget import ProblemWidget
from .application import Application, ProblemData

from PyQt5.QtWidgets import QTextEdit
from PyQt5 import QtWidgets, QtGui

import sys


class MainWindow(QtWidgets.QMainWindow):
    """ Main Window. """

    count = 0

    def __init__(self, parent=None, qapp=None):
        super().__init__(parent)
        self.qapp = qapp
        # Create singelton responsible for application logic
        self.application = Application()
        self.problem_windows = []

        self.setWindowTitle('Artap application')
        self._create_menu()
        # self._createToolBar()
        self._create_status_bar()
        self.mdi = QtWidgets.QMdiArea()
        self.setCentralWidget(self.mdi)

        # Logging
        self.log_window = QTextEdit()
        self.log_window.setWindowTitle('Log')
        self.mdi.addSubWindow(self.log_window)
        sys.stdout = LogWindow(self.log_window, sys.stdout)
        sys.stderr = LogWindow(self.log_window, sys.stderr, QtGui.QColor(255, 0, 0))

    def _create_actions(self):
        self.newAction = QtWidgets.QAction(QtGui.QIcon('new.png'), '&New', self)
        self.newAction.setShortcut('CTRL+N')
        self.newAction.setStatusTip('New problem')
        self.newAction.triggered.connect(self.new_problem_def)

        self.openAction = QtWidgets.QAction(QtGui.QIcon('open.png'), '&Open problem', self)
        self.openAction.setShortcut('CTRL+O')
        self.openAction.setStatusTip('Open problem')
        self.openAction.triggered.connect(self.open_problem)

        self.saveAction = QtWidgets.QAction(QtGui.QIcon('save.png'), '&Save problem', self)
        self.saveAction.setShortcut('CTRL+S')
        self.saveAction.setStatusTip('Save problem')
        # self.saveAction.triggered.connect(self.save_code)

        self.runAction = QtWidgets.QAction(QtGui.QIcon('run.png'), '&Run', self)
        self.runAction.setShortcut('F5')
        self.runAction.setStatusTip('Run problem')
        self.runAction.triggered.connect(self.run_problem)

        self.openResultsAction = QtWidgets.QAction(QtGui.QIcon('open_results.png'), '&Open Results', self)
        self.openResultsAction.setShortcut('CTRL+Q')
        self.openResultsAction.setStatusTip('Open results')
        self.openResultsAction.triggered.connect(self.open_results)

    def _create_menu(self):
        self._create_actions()
        self.menu = self.menuBar().addMenu("&File")
        self.menu.addAction(self.newAction)
        self.menu.addAction(self.openAction)
        self.menu.addAction(self.saveAction)
        self.menu.addAction('&Exit', self.close)

        self.menu = self.menuBar().addMenu("Run")
        self.menu.addAction(self.runAction)

        self.menu = self.menuBar().addMenu("Results")
        self.menu.addAction(self.openResultsAction)

    def _create_tool_bar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _create_status_bar(self):
        self.status = QtWidgets.QStatusBar()
        self.status.showMessage('I am the Status Bar')
        self.setStatusBar(self.status)

    def new_problem_def(self):
        new_dialog = NewProblemWizard()
        status = new_dialog.exec()
        if status == 1:
            self.status.showMessage('OK')
        else:
            self.status.showMessage('NOK')

    def create_problem(self):
        problem_window = ProblemWidget(self.mdi)
        self.mdi.addSubWindow(problem_window)
        problem_window.showMaximized()
        self.problem_windows.append(problem_window)
        return problem_window

    def open_problem(self):
        code_file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')
        problem_window = self.create_problem()
        problem = ProblemData(problem_window)
        self.application.problems.append(problem)
        code = problem.read_problem_file(code_file_name)
        problem_window.load_problem(problem, code)

    def run_problem(self):
        active_window = self.qapp.focusWidget().parent()
        for i, window in enumerate(self.problem_windows):
            if window is active_window:
                problem = self.application.problems[i]
                problem.run_problem()
                break
        problem = self.application.problems[i]
        problem.run_problem()

    # TODO: make it working
    # def save_code(self, id=0):
    #     text = self.problem_widget.editor.text()
    #     self.code_file = open(self.code_file_name[0], 'w')
    #     self.code_file.write(text)

    def open_results(self):
        database_file = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile')
        problem_window = self.create_problem()
        problem = ProblemData(problem_window)
        problem.process_results(database_file)
