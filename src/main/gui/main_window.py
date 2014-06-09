from keyring.backend import abc
import re
import sys

import pygal
from pygal.style import LightGreenStyle
from PySide import QtGui, QtCore, QtSvg

from src.main.core import datamodel
from src.main.core.dao import ContentDao, PersonDao, HitDao
from src.main.gui import gui_utils
from src.main.gui.gui_utils import SimpleTableModel


class SearchableTab(QtGui.QFrame):
    def __init__(self, status_bar):
        QtGui.QFrame.__init__(self)
        self.items = QtGui.QVBoxLayout()
        self.query_field = QtGui.QLineEdit()
        self.query_field.returnPressed.connect(lambda: SearchableTab._set_query(self, self.query_field.text()))
        self.search = QtGui.QPushButton("Search")
        self.search.clicked.connect(lambda: SearchableTab._set_query(self, self.query_field.text()))
        self.items_widget = QtGui.QWidget()
        self.status_bar = status_bar

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self._create_query_field())
        scroll_widget = QtGui.QScrollArea()
        scroll_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        #  scroll_widget.setLayout(self.items)
        self.items_widget.setLayout(self.items)
        scroll_widget.setWidget(self.items_widget)
        layout.addWidget(scroll_widget)
        layout.setStretch(0, 0)
        self.setLayout(layout)
        self._set_query("")

    @abc.abstractmethod
    def _do_query(self, query):
        pass

    @abc.abstractmethod
    def _create_item(self, query):
        pass

    def _set_query(self, query):
        gui_utils.clear_layout(self.items)
        results = self._do_query(query)
        count = results.count()
        page = 20
        for item in results.limit(page).sort("hits", -1):
            self.items.addWidget(self._create_item(item))
        self.items_widget.setFixedSize(740, 90 * min(page, count))
        self.status_bar.showMessage("Shown {} results of {} found.".format((min(page, count)), count))

    def _create_query_field(self):
        result = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        gui_utils.remove_margins(layout)
        layout.addWidget(self.query_field)
        layout.addWidget(self.search)
        result.setLayout(layout)
        return result

    def _create_categories(self, categories):
        result = QtGui.QWidget()
        result.setObjectName("categories")
        layout = QtGui.QGridLayout()

        layout.setColumnStretch(0, 0)
        row = 0
        for (name, value) in datamodel.sort_categories(categories):
            name_label = QtGui.QLabel(name)
            name_label.setFixedWidth(60)
            layout.addWidget(name_label, row, 0)
            layout.addWidget(self.create_quality(value), row, 1)
            row += 1
            if row == 3:
                break
        result.setLayout(layout)

        return result

    def create_quality(self, quality):
        result = QtGui.QWidget()
        layout = QtGui.QHBoxLayout()
        gui_utils.remove_margins(layout)
        max_value = 100
        progress = QtGui.QProgressBar()
        progress.setTextVisible(False)
        progress.setMinimum(0)
        progress.setMaximum(max_value)
        progress.setValue(int(quality * max_value))
        value = QtGui.QLabel('%.3f' % (quality))
        value.setFixedWidth(40)
        layout.addWidget(progress)
        layout.addWidget(value)
        result.setLayout(layout)
        return result


class SearchableContentsTab(SearchableTab):
    def __init__(self, status_bar):
        self.dao = ContentDao()
        self.popup = None
        SearchableTab.__init__(self, status_bar)

    def _do_query(self, query):
        return self.dao.find(
            {
                "$or": [
                    {"name": {"$regex": re.compile(".*{0}.*".format(query), re.IGNORECASE)}},
                    {"categories.{}".format(query): {"$gt": 0.5}}
                ]
            })

    def _create_item(self, content):
        main_layout = QtGui.QHBoxLayout()
        gui_utils.remove_margins(main_layout)

        layout = QtGui.QGridLayout()

        name_label = QtGui.QLabel(content.name)
        name_label.setWordWrap(True)
        layout.addWidget(QtGui.QLabel("Name:"), 0, 0, QtCore.Qt.AlignTop)
        layout.addWidget(name_label, 0, 1, 1, 5, QtCore.Qt.AlignTop)
        layout.addWidget(QtGui.QLabel("Quality:"), 1, 0)
        layout.addWidget(self.create_quality(content.quality), 1, 1)
        layout.addWidget(QtGui.QLabel("Hits:"), 1, 2)
        layout.addWidget(QtGui.QLabel(str(content.hits)), 1, 3)
        layout.addWidget(QtGui.QLabel(""), 1, 4)
        show_hits = QtGui.QPushButton("Show hits")
        show_hits.clicked.connect(lambda: self.show_hits(content.name))
        layout.addWidget(show_hits, 1, 5)
        layout.setColumnStretch(4, 1)
        left = QtGui.QWidget()
        left.setLayout(layout)
        main_layout.addWidget(left)

        main_layout.addWidget(self._create_categories(content.categories))

        result = QtGui.QFrame()
        result.setObjectName("tile")

        result.setStyleSheet("""
            QWidget#tile {
                border: 1px solid gray;
                border-radius: 3px;
            }
            QProgressBar {
                width: 48px;
                max-width: 48px;
                height: 6px;
                border: 2px solid grey;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 1px;
            }
        """)

        result.setFixedSize(720, 80)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)
        result.setLayout(main_layout)
        return result

    def show_hits(self, name):
        self.popup = QtGui.QTableView()
        self.popup.setGeometry(QtCore.QRect(100, 100, 400, 200))
        layout = QtGui.QHBoxLayout()
        self.popup.setLayout(layout)

        headers = ["Who", "When"]
        data_list = []
        chart_data = []
        dao = HitDao()
        value = 0
        for hit in dao.find({"what": name}).limit(1000).sort("when", -1):
            data_list.append((hit.who, hit.when))
            value += 1
            chart_data.append((100 - hit.when, value))

        table_model = SimpleTableModel(self, data_list, headers)
        table = QtGui.QTableView()
        table.setModel(table_model)
        table.setFixedSize(280, 600)
        table.setColumnWidth(0, 150)
        table.setColumnWidth(2, 80)
        layout.addWidget(table)
        layout.addWidget(self.create_chart(chart_data))

        self.popup.show()

    def create_chart(self, data):
        view = QtSvg.QSvgWidget()
        view.setFixedSize(700, 600)

        xy_chart = pygal.XY(style=LightGreenStyle, show_legend=False, show_dots=False, stroke=True, fill=True, zero=0)
        xy_chart.title = 'Hits in time'
        xy_chart.add('', data)

        xy_chart.add('', [])
        chart = xy_chart.render()
        view.load(QtCore.QByteArray(chart))
        return view


class SearchablePersonsTab(SearchableTab):
    def __init__(self, status_bar):
        self.dao = PersonDao()
        self.popup = None
        SearchableTab.__init__(self, status_bar)

    def _do_query(self, query):
        return self.dao.find(
            {
                "$or": [
                    {"person_name": {"$regex": re.compile(".*{0}.*".format(query), re.IGNORECASE)}},
                    {"interests.{}".format(query): {"$gt": 0.5}}
                ]
            })

    def _create_item(self, person):
        main_layout = QtGui.QHBoxLayout()
        gui_utils.remove_margins(main_layout)

        layout = QtGui.QGridLayout()

        name_label = QtGui.QLabel("Watch frequency:")
        layout.addWidget(QtGui.QLabel("Name:"), 0, 0, QtCore.Qt.AlignTop)
        layout.addWidget(QtGui.QLabel(person.person_name), 0, 1, 1, 5, QtCore.Qt.AlignTop)
        layout.addWidget(name_label, 1, 0)
        layout.addWidget(self.create_quality(person.watch_frequency / 5), 1, 1)
        layout.addWidget(QtGui.QLabel("Watches:"), 1, 2)
        layout.addWidget(QtGui.QLabel(str(person.hits)), 1, 3)
        layout.addWidget(QtGui.QLabel(""), 1, 4)
        show_watches = QtGui.QPushButton("Show watches")
        show_watches.clicked.connect(lambda: self.show_hits(person.person_name))
        layout.addWidget(show_watches, 1, 5)

        layout.addWidget(QtGui.QLabel("Position:"), 2, 0)
        layout.addWidget(QtGui.QLabel("[%.5g, %.5g]" % (person.longitude, person.latitude)), 2, 1, 1, 2)
        layout.addWidget(QtGui.QLabel("Friends:"), 2, 3)
        layout.addWidget(QtGui.QLabel(str(len(person.friends))), 2, 4)
        show_friends = QtGui.QPushButton("Show friends")
        show_friends.clicked.connect(lambda: self.show_friends(person.friends))
        layout.addWidget(show_friends, 2, 5)
        layout.setColumnStretch(4, 1)
        left = QtGui.QWidget()
        left.setLayout(layout)
        main_layout.addWidget(left)

        main_layout.addWidget(self._create_categories(person.interests))

        result = QtGui.QFrame()
        result.setObjectName("tile")

        result.setStyleSheet("""
            QWidget#tile {
                border: 1px solid gray;
                border-radius: 3px;
            }
            QProgressBar {
                width: 48px;
                max-width: 48px;
                height: 6px;
                border: 2px solid grey;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                width: 1px;
            }
        """)

        result.setFixedSize(720, 80)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 0)
        result.setLayout(main_layout)
        return result

    def show_hits(self, name):
        self.popup = QtGui.QTableView()
        self.popup.setGeometry(QtCore.QRect(100, 100, 680, 320))
        layout = QtGui.QHBoxLayout()
        self.popup.setLayout(layout)

        headers = ["What", "When"]
        data_list = []
        dao = HitDao()
        for hit in dao.find({"who": name}).limit(1000).sort("when", -1):
            data_list.append((hit.what, hit.when))
        table_model = SimpleTableModel(self, data_list, headers)
        table = QtGui.QTableView()
        table.setModel(table_model)
        table.setFixedSize(640, 300)
        table.setColumnWidth(0, 500)
        table.setColumnWidth(2, 80)
        layout.addWidget(table)

        self.popup.show()

    def show_friends(self, friends):
        self.popup = QtGui.QTableView()
        self.popup.setGeometry(QtCore.QRect(100, 100, 680, 320))
        layout = QtGui.QHBoxLayout()
        self.popup.setLayout(layout)

        friends = [[friend] for friend in friends]
        headers = ["Name"]
        table_model = SimpleTableModel(self, friends, headers)
        table = QtGui.QTableView()
        table.setModel(table_model)
        table.setFixedSize(640, 300)
        table.setColumnWidth(0, 500)
        table.setColumnWidth(2, 80)
        layout.addWidget(table)

        self.popup.show()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        tabs = QtGui.QTabWidget(self)
        self.setCentralWidget(tabs)

        self.setWindowTitle("Web content popularity")
        self.setGeometry(0, 0, 780, 480)

        status_bar = self.statusBar()
        tabs.addTab(SearchableContentsTab(status_bar), "Contents")
        tabs.addTab(SearchablePersonsTab(status_bar), "Persons")
        tabs.addTab(self.create_hits_tab(), "Hits")

    def create_hits_tab(self):
        headers = ["Who", "What", "When"]
        data_list = []
        dao = HitDao()
        value = 0
        for hit in dao.find().limit(1000).sort("when", -1):
            data_list.append((hit.who, hit.what, hit.when))
            value += 1
        table_model = SimpleTableModel(self, data_list, headers)
        table = QtGui.QTableView()
        table.setModel(table_model)
        table.setFixedWidth(760)
        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 500)
        table.setColumnWidth(2, 80)

        return table


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()