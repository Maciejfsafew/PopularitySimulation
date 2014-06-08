from PySide import QtCore

__author__ = 'mjjaniec'


def remove_margins(layout):
    layout.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))


def clear_layout(layout):
    while True:
        component = layout.takeAt(0)
        if not component: return
        component.widget().deleteLater()


class SimpleTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        if len(self.mylist) > 0:
            return len(self.mylist[0])
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        pass