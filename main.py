import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from db_connect import db, cursor

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    uic.loadUi('car.ui', self)
    self.id = 0

    self.tb_car.setColumnWidth(0, 50)
    self.tb_car.setColumnWidth(1, 150)
    self.tb_car.setColumnWidth(2, 150)
    self.tb_car.setColumnWidth(3, 120)
    self.tb_car.setColumnWidth(4, 150)

    self.show_all_cars()
    self.btn_add.clicked.connect(self.insert_car)
    self.btn_clear.clicked.connect(self.clear_text)
    self.tb_car.cellClicked.connect(self.selected_row)

  def clear_text(self):
    self.txt_brand.setText('')
    self.txt_model.setText('')
    self.txt_year.setText('')
    self.txt_price.setText('')

    self.btn_add.setEnabled(True)
    self.btn_update.setEnabled(False)
    self.btn_delete.setEnabled(False)
    
    self.tb_car.clearSelection()

  def selected_row(self):
    row = self.tb_car.currentRow()
    self.id = self.tb_car.item(row, 0).text()
    brand = self.tb_car.item(row, 1).text()
    model = self.tb_car.item(row, 2).text()
    year = self.tb_car.item(row, 3).text()
    price = self.tb_car.item(row, 4).text()

    self.txt_brand.setText(brand)
    self.txt_model.setText(model)
    self.txt_year.setText(year)
    self.txt_price.setText(price)

    self.btn_add.setEnabled(False)
    self.btn_delete.setEnabled(True)
    self.btn_update.setEnabled(True)

  def show_all_cars(self):
    sql = 'select * from car'
    cars = cursor.execute(sql).fetchall()

    self.all_cars(cars)

  def all_cars(self, cars):
      self.tb_car.setRowCount(len(cars))

      row = 0
      for car in cars:
        self.tb_car.setItem(row, 0, QTableWidgetItem(str(car[0])))
        self.tb_car.setItem(row, 1, QTableWidgetItem(car[1]))
        self.tb_car.setItem(row, 2, QTableWidgetItem(car[2]))
        self.tb_car.setItem(row, 3, QTableWidgetItem(str(car[3])))
        self.tb_car.setItem(row, 4, QTableWidgetItem(str(car[4])))

        row += 1

  def insert_car(self):
    brand = self.txt_brand.text()
    model = self.txt_model.text()
    year = self.txt_year.text()
    price = self.txt_price.text()

    sql = 'insert into car(brand, model, year, price) values(?, ?, ?, ?)'
    values = (brand, model, year, price)

    rs = cursor.execute(sql, values)
    db.commit()

    if rs.rowcount>0:
      QMessageBox.information(self, 'Information', 'Insert car successful!')
    else:
      QMessageBox.warning(self, 'Warning', 'Unable to insert car!')

    self.show_all_cars()
    self.clear_text()

  def delete_car(self):
    sql = 'delete from car where id = ?'
    values = (int(self.id), )

    rs = cursor.execute(sql, values)
    db.commit()
    if rs.rowcount>0:
      QMessageBox.information(self, 'Informaition', 'Delete car successful!')
    else:
      QMessageBox.information(self, 'Informaition', 'Unable to delete car!')
    self.show_all_cars()
    self.clear_text()

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()