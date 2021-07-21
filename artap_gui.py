from PyQt5 import QtWidgets
import sys

if __name__ == "__main__" and __package__ is None:
    __package__ = "artap"

from artap.gui.main_window import MainWindow


app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow(None, app)
main_window.showMaximized()
sys.exit(app.exec_())
