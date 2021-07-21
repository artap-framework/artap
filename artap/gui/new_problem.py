from PyQt5 import QtWidgets


class NewProblemWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(NewProblemWizard, self).__init__(parent)
        self.addPage(NewProblemPage1(self))
        self.addPage(NewProblemPage2(self))
        self.setWindowTitle("New Problem Wizard")
        self.button(QtWidgets.QWizard.NextButton).clicked.connect(self.next)

    def next(self):
        msg = QtWidgets.QMessageBox()
        msg.setText(str(self.page(0).project_combo_box.currentText()))
        msg.exec()


class NewProblemPage1(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parameter_widgets = []
        self.parameters_number = 1

        self.setTitle('New Problem')
        self.layout = QtWidgets.QGridLayout()

        self.name_label = QtWidgets.QLabel('Name:')
        self.layout.addWidget(self.name_label, 0, 0)

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setFixedWidth(100)
        self.layout.addWidget(self.name_edit, 0, 1)

        self.parameters_number_label = QtWidgets.QLabel('Number of parameters:')
        self.layout.addWidget(self.parameters_number_label, 1, 0)

        self.parameters_spin_box = QtWidgets.QSpinBox()
        self.parameters_spin_box.setValue(1)
        self.layout.addWidget(self.parameters_spin_box, 1, 1)
        self.layout.addChildWidget(self.parameters_spin_box)

        self.goals_label = QtWidgets.QLabel('Number of goal functions:')
        self.layout.addWidget(self.goals_label, 3, 0)

        self.goals_spin_box = QtWidgets.QSpinBox()
        self.goals_spin_box.setValue(1)
        self.layout.addWidget(self.goals_spin_box, 3, 1)
        self.layout.addChildWidget(self.goals_spin_box)

        self.project_label = QtWidgets.QLabel('Problem type:')
        self.layout.addWidget(self.project_label, 4, 0)

        self.project_combo_box = QtWidgets.QComboBox()
        project_types = ['Analytical', 'Comsol', 'Matlab', 'Python', 'Agros', 'CST']
        self.project_combo_box.addItems(project_types)
        self.layout.addWidget(self.project_combo_box, 4, 1)

        self.setLayout(self.layout)
        self.adjustSize()

        self.show()

    def parameters_number_change(self):
        self.parameters_number = self.parameters_spin_box.value()
        self.buttonBox.close()

        for item in self.parameter_widgets:
            item.close()

        for i in range(self.parameters_number):
            parameter_widget = QtWidgets.QLabel('x_{}'.format(i + 1))
            self.parameter_widgets.append(parameter_widget)

            self.layout.addWidget(parameter_widget, 3 + i, 0)

        self.add_buttons()
        self.adjustSize()
        self.show()


class NewProblemPage2(QtWidgets.QWizardPage):
    pass
