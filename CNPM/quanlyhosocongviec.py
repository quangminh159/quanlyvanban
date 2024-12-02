import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QComboBox, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate

class WorkFileManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self)
        self.pushButton_11.clicked.connect(self.search_work_file)
        self.pushButton_12.clicked.connect(self.add_work_file)
        self.pushButton_13.clicked.connect(self.edit_work_file)
        self.pushButton_14.clicked.connect(self.delete_work_file)
        self.dateEdit_3.setDate(QDate.currentDate())
        self.tableWidget_3.itemClicked.connect(self.on_item_clicked1)
        self.update_work_file_table()

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def add_work_file(self):
        file_name = self.lineEdit_3.text()
        content = self.lineEdit_13.text()
        create_date = self.dateEdit_3.date().toString('yyyy-MM-dd')
        status = self.comboBox_3.currentText()

        if not file_name or not content or not status:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO taskFiles (fileName, description, createdDate, status) VALUES (?, ?, ?, ?)', 
                               (file_name, content, create_date, status))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Thêm hồ sơ công việc thành công!")
                self.lineEdit_3.clear()
                self.lineEdit_13.clear()
                self.dateEdit_3.setDate(QDate.currentDate())
                self.comboBox_3.setCurrentIndex(0)
                self.update_work_file_table()  
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Thêm hồ sơ thất bại: {e}")
            finally:
                conn.close()

    def edit_work_file(self):
        file_name = self.lineEdit_3.text()
        content = self.lineEdit_13.text()
        create_date = self.dateEdit_3.date().toString('yyyy-MM-dd')
        status = self.comboBox_3.currentText()

        if not file_name or not content or not status:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE taskFiles SET description = ?, createdDate = ?, status = ? WHERE fileName = ?', 
                               (content, create_date, status, file_name))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Cập nhật hồ sơ thành công!")
                self.lineEdit_3.clear()
                self.lineEdit_13.clear()
                self.dateEdit_3.setDate(QDate.currentDate())
                self.comboBox_3.setCurrentIndex(0)
                self.update_work_file_table() 
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Sửa hồ sơ thất bại: {e}")
            finally:
                conn.close()

    def delete_work_file(self):
        file_name = self.lineEdit_3.text()

        if not file_name:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tên hồ sơ để xóa!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM taskFiles WHERE fileName = ?', (file_name,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa hồ sơ công việc thành công!")
                self.update_work_file_table() 
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Xóa hồ sơ thất bại: {e}")
            finally:
                conn.close()

    def search_work_file(self):
        search_query = self.lineEdit_14.text().strip() 
        if not search_query:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'SELECT * FROM taskFiles WHERE fileName LIKE ? OR description LIKE ?', 
                    (f'%{search_query}%', f'%{search_query}%')
                )
                work_files = cursor.fetchall()
                if work_files:
                    self.update_table_with_data(work_files)
                else:
                    QMessageBox.information(self, "Không có kết quả", "Không tìm thấy hồ sơ công việc nào!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Tìm kiếm thất bại: {e}")
            finally:
                conn.close()

    def update_work_file_table(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM taskFiles')
                work_files = cursor.fetchall()
                self.update_work_table_with_data(work_files)
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Cập nhật bảng thất bại: {e}")
            finally:
                conn.close()

    def update_work_table_with_data(self, work_files):
        self.tableWidget_3.setRowCount(0)
        for row_number, row_data in enumerate(work_files):
            self.tableWidget_3.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    def on_item_clicked1(self, item):
        row = item.row()
        file_name = self.tableWidget_3.item(row, 0).text()  
        description = self.tableWidget_3.item(row, 1).text()  
        created_date = self.tableWidget_3.item(row, 2).text()  
        status = self.tableWidget_3.item(row, 3).text()  
        self.lineEdit_3.setText(file_name)
        self.lineEdit_13.setText(description)
        self.dateEdit_3.setDate(QDate.fromString(created_date, 'yyyy-MM-dd'))
        self.comboBox_3.setCurrentText(status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WorkFileManagementWindow()
    main_window.show()
    sys.exit(app.exec_())
