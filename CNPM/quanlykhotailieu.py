import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate
import os

class DocumentManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self)
        self.pushButton_15.clicked.connect(self.load_file3)
        self.pushButton_16.clicked.connect(self.search_file)
        self.pushButton.clicked.connect(self.add_file)
        self.pushButton_2.clicked.connect(self.edit_file)
        self.pushButton_3.clicked.connect(self.delete_file)
        self.dateEdit_4.setDate(QDate.currentDate())
        self.tableWidget_4.cellClicked.connect(self.on_table_item_clicked3)
        self.update_document_table3()

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def add_file(self):
        document_name = self.lineEdit_15.text()
        description = self.lineEdit_16.text()
        upload_date = self.dateEdit_4.date().toString('yyyy-MM-dd')
        uploaded_by = self.lineEdit_18.text()
        file_attachment = self.lineEdit_19.text()

        if not document_name or not description or not upload_date or not file_attachment or not uploaded_by:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO sharedDocuments (documentName, description, uploadedDate, documentFile, uploadedBy) VALUES (?, ?, ?, ?, ?)',
                    (document_name, description, upload_date, file_attachment, uploaded_by)
                )
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Tải tài liệu thành công!")
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
                self.dateEdit_4.setDate(QDate.currentDate())
                self.lineEdit_18.clear()
                self.lineEdit_19.clear()
                self.update_document_table3()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Tải tài liệu thất bại: {e}")
            finally:
                conn.close()

    def load_file3(self):
        file_name = self.lineEdit_12.text()
        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(self, "Mở file đính kèm", "", "All Files (*);;Text Files (*.txt)")
        if file_name:
            file_name = os.path.basename(file_name)
            self.lineEdit_19.setText(file_name)

    def edit_file(self):
        selected_row = self.tableWidget_4.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn tài liệu cần sửa!")
            return
        document_name = self.lineEdit_15.text()
        description = self.lineEdit_16.text()
        upload_date = self.dateEdit_4.date().toString('yyyy-MM-dd')
        uploaded_by = self.lineEdit_18.text()
        file_attachment = self.lineEdit_19.text()
        doc_id = self.tableWidget_4.item(selected_row, 0).text()

        if not document_name or not description or not upload_date or not file_attachment or not uploaded_by:
            QMessageBox.warning(self, "Thông báo", "Vui lòng điền đầy đủ thông tin!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'UPDATE sharedDocuments SET documentName = ?, description = ?, uploadedDate = ?, documentFile = ?, uploadedBy = ? WHERE documentID = ?',
                    (document_name, description, upload_date, file_attachment, uploaded_by, doc_id)
                )
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Sửa tài liệu thành công!")
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
                self.dateEdit_4.setDate(QDate.currentDate())
                self.lineEdit_18.clear()
                self.lineEdit_19.clear()
                self.update_document_table3()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Sửa tài liệu thất bại: {e}")
            finally:
                conn.close()

    def delete_file(self):
        selected_row = self.tableWidget_4.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn tài liệu cần xóa!")
            return
        doc_id = self.tableWidget_4.item(selected_row, 0).text()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM sharedDocuments WHERE documentID = ?', (doc_id,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa tài liệu thành công!")
                self.update_document_table3()
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Xóa tài liệu thất bại: {e}")
            finally:
                conn.close()

    def search_file(self):
        search_query = self.lineEdit_20.text().strip()
        if not search_query:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'SELECT * FROM sharedDocuments WHERE documentName LIKE ? OR description LIKE ? OR uploadedDate LIKE ? OR uploadedBy LIKE ?',
                    (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
                )
                documents = cursor.fetchall()
                if documents:
                    self.update_file_table_with_data(documents)
                else:
                    QMessageBox.information(self, "Không có kết quả", "Không tìm thấy tài liệu!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Tìm kiếm thất bại: {e}")
            finally:
                conn.close()

    def update_document_table3(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM sharedDocuments')
                documents = cursor.fetchall()
                if documents:
                    self.update_file_table_with_data(documents)
                else:
                    QMessageBox.information(self, "Không có dữ liệu", "Không có tài liệu nào trong cơ sở dữ liệu!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Cập nhật bảng thất bại: {e}")
            finally:
                conn.close()

    def update_file_table_with_data(self, documents):
        self.tableWidget_4.setRowCount(0)
        for row_number, row_data in enumerate(documents):
            self.tableWidget_4.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_4.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def on_table_item_clicked3(self, row, column):
        document_name = self.tableWidget_4.item(row, 1).text()
        description = self.tableWidget_4.item(row, 2).text()
        upload_date = self.tableWidget_4.item(row, 3).text()
        file_attachment = self.tableWidget_4.item(row, 4).text()
        uploaded_by = self.tableWidget_4.item(row, 5).text()
        self.lineEdit_15.setText(document_name)
        self.lineEdit_16.setText(description)
        self.lineEdit_18.setText(uploaded_by)
        self.dateEdit_4.setDate(QDate.fromString(upload_date, 'yyyy-MM-dd'))
        self.lineEdit_19.setText(file_attachment)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = DocumentManagementWindow()
    main_window.show()
    sys.exit(app.exec_())
