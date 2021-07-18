from PyQt5 import QtWidgets
import sys
from artap.gui.main_window import MainWindow


app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.showMaximized()
sys.exit(app.exec_())
