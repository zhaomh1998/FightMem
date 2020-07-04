import sys
from PyQt5.QtWidgets import *
from ui.FightMemPCUI import *


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == "__main__":
    sys.argv += ['--ignore-gpu-blacklist']  # Fix OpenGL Error for QWebEngineView on MacOS
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
