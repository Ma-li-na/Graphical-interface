#  Лабораторная работа №3. Таблицы и SQL в PyQt5.
#  Меню (Set/Close connection), кнопки bt1-bt3, QComboBox с колонками и QTabWidget с пятью QTableView.

import os
import sys
import PyQt5

pyqt_dir = os.path.dirname(PyQt5.__file__)
plugins_root = os.path.join(pyqt_dir, "Qt5", "plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(plugins_root, "platforms")
os.environ['QT_PLUGIN_PATH'] = plugins_root

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QComboBox, QTabWidget, QTableView, QVBoxLayout, QHBoxLayout,
    QFileDialog, QMessageBox, QAction, QDialog,
    QTextEdit, QDialogButtonBox
)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt


class QueryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SQL Query (bonus)")
        self.resize(520, 300)

        self.editor = QTextEdit()
        self.editor.setPlainText("SELECT name FROM sqlite_master")

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите SQL-запрос:"))
        layout.addWidget(self.editor)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_query(self):
        return self.editor.toPlainText().strip()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная №3 — таблицы и SQL")
        self.resize(1100, 650)

        self.db = None          
        self.views = []         

        menu = self.menuBar().addMenu("Menu")

        act_open = QAction("Set connection", self)
        act_open.triggered.connect(self.set_connection)
        menu.addAction(act_open)

        act_close = QAction("Close connection", self)
        act_close.triggered.connect(self.close_connection)
        menu.addAction(act_close)

        self.btn1 = QPushButton('Имена объектов БД')
        self.btn1.setToolTip("SELECT name FROM sqlite_master  →  Tab2")
        self.btn1.clicked.connect(self.query_bt1)

        self.btn2 = QPushButton('Свой SQL-запрос…')
        self.btn2.setToolTip("Откроется диалог ввода произвольного SQL  →  Tab4")
        self.btn2.clicked.connect(self.query_bt2)

        self.btn3 = QPushButton('Список таблиц')
        self.btn3.setToolTip("Показать все таблицы базы данных  →  Tab5")
        self.btn3.clicked.connect(self.query_bt3)

        self.combo = QComboBox()
        self.combo.setMinimumWidth(260)
        self.combo.setToolTip("Выберите колонку — её значения появятся в Tab3")
        self.combo.addItem("-- Columns --")
        self.combo.currentIndexChanged.connect(self.on_column_selected)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(self.btn1)
        toolbar_layout.addWidget(self.btn2)
        toolbar_layout.addWidget(self.btn3)
        toolbar_layout.addStretch()           
        toolbar_layout.addWidget(self.combo)

        self.tabs = QTabWidget()
        for i in range(1, 6):
            view = QTableView()
            self.views.append(view)
            self.tabs.addTab(view, f"Tab{i}")

        central = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)   # один ряд с кнопками и combo
        layout.addWidget(self.tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.set_controls_enabled(False)

    def set_controls_enabled(self, enabled):
        for w in (self.btn1, self.btn2, self.btn3, self.combo):
            w.setEnabled(enabled)

    def set_connection(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл базы данных", "",
            "SQLite DB (*.db *.sqlite *.sqlite3);;All files (*.*)"
        )
        if not path:
            return

        self.close_connection()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(path)

        if not self.db.open():
            QMessageBox.critical(
                self, "Ошибка соединения",
                "Не удалось открыть БД:\n" + self.db.lastError().text()
            )
            self.db = None
            return

        self.set_controls_enabled(True)

        self.run_query(0, "SELECT * FROM sqlite_master")

        self.fill_columns()


    def close_connection(self):
        if self.db is not None:
            name = self.db.connectionName()
            self.db.close()
            QSqlDatabase.removeDatabase(name)
            self.db = None

        for view in self.views:
            view.setModel(None)

        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItem("-- Columns --")
        self.combo.blockSignals(False)

        self.set_controls_enabled(False)

    def run_query(self, tab_index, sql):
        if self.db is None:
            QMessageBox.warning(
                self, "Нет соединения",
                "Сначала установите соединение: Menu → Set connection."
            )
            return

        model = QSqlQueryModel()
        model.setQuery(sql, self.db)

        if model.lastError().isValid():
            QMessageBox.warning(
                self, "Ошибка SQL",
                model.lastError().text() + "\n\nЗапрос:\n" + sql
            )
            return

        view = self.views[tab_index]
        view.setModel(model)
        view.resizeColumnsToContents()
        self.tabs.setCurrentIndex(tab_index)

    def query_bt1(self):
        self.run_query(1, "SELECT name FROM sqlite_master")

    def query_bt2(self):
        dlg = QueryDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            sql = dlg.get_query()
            if sql:
                self.run_query(3, sql)


    def query_bt3(self):
        self.run_query(
            4,
            "SELECT name, type FROM sqlite_master "
            "WHERE type='table' ORDER BY name"
        )

    def fill_columns(self):
        self.combo.blockSignals(True)
        self.combo.clear()
        self.combo.addItem("-- Columns --")

        if self.db is None:
            self.combo.blockSignals(False)
            return

        # Список таблиц
        q = QSqlQuery(self.db)
        q.exec_("SELECT name FROM sqlite_master WHERE type='table'")
        tables = []
        while q.next():
            tables.append(q.value(0))

        # Для каждой таблицы — её колонки через PRAGMA
        for table in tables:
            q.exec_(f'PRAGMA table_info("{table}")')
            while q.next():
                column = q.value(1)                 
                self.combo.addItem(f"{table}.{column}")

        self.combo.blockSignals(False)

    def on_column_selected(self, index):
        if index <= 0:
            return
        text = self.combo.currentText()
        if "." not in text:
            return
        table, column = text.split(".", 1)
        self.run_query(2, f'SELECT "{column}" FROM "{table}"')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())