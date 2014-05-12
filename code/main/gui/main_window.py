import sys

from PySide import QtGui, QtCore, QtUiTools

from code.main import commons


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        loader = QtUiTools.QUiLoader()
        layout_file = QtCore.QFile(commons.get_resource_path("main_window.xml"))

        layout_file.open(QtCore.QFile.ReadOnly)
        content = loader.load(layout_file, self)
        layout_file.close()
        self.setWindowTitle("Web content popularity")
        self.setGeometry(0, 0, 640, 480)


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()