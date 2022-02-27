import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Coffee List')
        self.show_result()
        self.red = Redactor()
        self.pushButton.clicked.connect(self.open_redactor)
        self.titles = None

    def show_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def open_redactor(self):
        self.hide()
        self.red = Redactor()
        self.red.show()


class Redactor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Redactor')
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.save_results)
        self.pushButton_2.clicked.connect(self.new_coffee)
        self.modified = {}
        self.titles = None
        self.show_result()

    def show_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += f" WHERE ID = {self.modified['ID']}"
            cur.execute(que)
            self.con.commit()
            self.modified.clear()

    def new_coffee(self):
        ID = self.lineEdit_1.text()
        name = self.lineEdit_2.text()
        roast = self.lineEdit_3.text()
        processing = self.lineEdit_4.text()
        description = self.lineEdit_5.text()
        price = self.lineEdit_6.text()
        volume = self.lineEdit_7.text()
        if ID and name and roast and processing and description and price and volume:
            cur = self.con.cursor()
            cur.execute(f"INSERT INTO coffee VALUES({ID}, '{name}', '{roast}', '{processing}', '{description}', {price}, {volume})")
            self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
