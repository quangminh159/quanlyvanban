import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5 import uic

class DocumentInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self) 
        self.pushButton_17.clicked.connect(self.search_info)  
        self.pushButton_18.clicked.connect(self.add_info)   
        self.pushButton_19.clicked.connect(self.edit_info)  
        self.pushButton_20.clicked.connect(self.delete_info) 
        self.dateEdit_5.setDate(QDate.currentDate())  
        self.update_document_info_table()  
        self.tableWidget_5.cellClicked.connect(self.populate_fields_from_table)

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def search_info(self):
        performer = self.lineEdit_17.text().strip()
        info_type = self.lineEdit_21.text().strip()
        if not performer and not info_type:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập thông tin tìm kiếm!")
            return
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = '''
                    SELECT * 
                    FROM informationExtraction 
                    WHERE performedBy LIKE ? 
                    OR informationType LIKE ? 
                    OR result LIKE ?
                '''
                cursor.execute(query, (f'%{performer}%', f'%{info_type}%', f'%{performer}%'))
                results = cursor.fetchall()
                if results:
                    self.update_table_with_data(results)
                else:
                    QMessageBox.information(self, "Không có kết quả", "Không tìm thấy thông tin!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Tìm kiếm thất bại: {e}")
            finally:
                conn.close()

    def add_info(self):
        performer = self.lineEdit_17.text()
        info_type = self.lineEdit_21.text()
        action_date = self.dateEdit_5.date().toString('yyyy-MM-dd')
        result = self.lineEdit_23.text()
        if not performer or not info_type or not action_date or not result:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO informationExtraction (performedBy, informationType, date, result) VALUES (?, ?, ?, ?)',
                    (performer, info_type, action_date, result)
                )
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Thêm thông tin thành công!")
                self.lineEdit_17.clear()
                self.lineEdit_21.clear()
                self.dateEdit_5.setDate(QDate.currentDate())
                self.lineEdit_23.clear()
                self.update_document_info_table() 
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Thêm thông tin thất bại: {e}")
            finally:
                conn.close()

    def edit_info(self):
        selected_row = self.tableWidget_5.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn thông tin cần sửa!")
            return

        id = self.tableWidget_5.item(selected_row, 0).text() 
        performer = self.lineEdit_17.text()
        info_type = self.lineEdit_21.text()
        action_date = self.dateEdit_5.date().toString('yyyy-MM-dd')
        result = self.lineEdit_23.text()
        if not performer or not info_type or not action_date or not result:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'UPDATE informationExtraction SET performedBy = ?, informationType = ?, date = ?, result = ? WHERE extractionID = ?',
                    (performer, info_type, action_date, result, id)
                )
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Sửa thông tin thành công!")
                self.lineEdit_17.clear()
                self.lineEdit_21.clear()
                self.dateEdit_5.setDate(QDate.currentDate())
                self.lineEdit_23.clear()
                self.update_document_info_table()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Sửa thông tin thất bại: {e}")
            finally:
                conn.close()

    def delete_info(self):
        selected_row = self.tableWidget_5.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn thông tin cần xóa!")
            return

        id = self.tableWidget_5.item(selected_row, 0).text()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM informationExtraction WHERE extractionID = ?', (id,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa thông tin thành công!")
                self.update_document_info_table() 
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Xóa thông tin thất bại: {e}")
            finally:
                conn.close()

    def update_document_info_table(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM informationExtraction')
                data = cursor.fetchall()
                self.update_table_with_data(data)
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Cập nhật bảng thất bại: {e}")
            finally:
                conn.close()

    def update_table_with_data(self, data):
        self.tableWidget_5.setRowCount(0) 
        for row_number, row_data in enumerate(data):
            self.tableWidget_5.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_5.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def populate_fields_from_table(self, row, column):
        self.lineEdit_17.setText(self.tableWidget_5.item(row, 1).text())  
        self.lineEdit_21.setText(self.tableWidget_5.item(row, 2).text())  
        self.dateEdit_5.setDate(QDate.fromString(self.tableWidget_5.item(row, 3).text(), 'yyyy-MM-dd')) 
        self.lineEdit_23.setText(self.tableWidget_5.item(row, 4).text())  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DocumentInfoWindow()
    main_window.show()
    sys.exit(app.exec_())
