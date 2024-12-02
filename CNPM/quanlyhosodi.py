import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QCompleter, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate
import os

class OutgoingDocumentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self) 
        self.pushButton_6.clicked.connect(self.add_document2)
        self.pushButton_7.clicked.connect(self.edit_document2)
        self.pushButton_8.clicked.connect(self.delete_document2)
        self.pushButton_9.clicked.connect(self.search_document2)
        self.pushButton_10.clicked.connect(self.load_file2)
        self.tableWidget_2.itemClicked.connect(self.on_item_clicked2)
        self.dateEdit_2.setDate(QDate.currentDate())
        self.update_document_table2()
        self.setup_search_completer2()

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def add_document2(self):
        doc_number = self.lineEdit_7.text()
        title = self.lineEdit_9.text()
        recipient = self.lineEdit_10.text()
        send_date = self.dateEdit_2.date().toString('yyyy-MM-dd')
        content = self.lineEdit_11.text()
        file_attachment = self.lineEdit_12.text()
        status = self.comboBox_2.currentText()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO outgoingDocuments (documentNumber, title, recipient, sentDate, content, attachment, status) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                               (doc_number, title, recipient, send_date, content, file_attachment, status))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Thêm văn bản đi thành công!")
                self.lineEdit_7.clear()
                self.lineEdit_9.clear()
                self.lineEdit_10.clear()
                self.dateEdit_2.setDate(QDate.currentDate())
                self.lineEdit_11.clear()
                self.lineEdit_12.clear()
                self.comboBox_2.setCurrentIndex(0)
                self.update_document_table() 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Thêm văn bản thất bại: {e}")
            finally:
                conn.close()

    def edit_document2(self):
        doc_number = self.lineEdit_7.text()
        title = self.lineEdit_9.text()
        recipient = self.lineEdit_10.text()
        send_date = self.dateEdit_2.date().toString('yyyy-MM-dd')
        content = self.lineEdit_11.text()
        file_attachment = self.lineEdit_12.text()
        status = self.comboBox_2.currentText()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE outgoingDocuments SET title = ?, recipient = ?, sentDate = ?, content = ?, attachment = ?, status = ? WHERE documentNumber = ?', 
                               (title, recipient, send_date, content, file_attachment, status, doc_number))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Sửa văn bản thành công!")
                self.lineEdit_7.clear()
                self.lineEdit_9.clear()
                self.lineEdit_10.clear()
                self.dateEdit_2.setDate(QDate.currentDate())
                self.lineEdit_11.clear()
                self.lineEdit_12.clear()
                self.comboBox_2.setCurrentIndex(0)
                self.update_document_table()
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Sửa văn bản thất bại: {e}")
            finally:
                conn.close()

    def delete_document2(self):
        doc_number = self.lineEdit_7.text()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM outgoingDocuments WHERE documentNumber = ?', (doc_number,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa văn bản thành công!")
                self.update_document_table()
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Xóa văn bản thất bại: {e}")
            finally:
                conn.close()

    def search_document2(self):
        search_query = self.lineEdit_5.text().strip() 
        if not search_query:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập thông tin tìm kiếm!")
            return

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'SELECT * FROM outgoingDocuments WHERE documentNumber LIKE ? OR title LIKE ? OR recipient LIKE ? OR content LIKE ?', 
                    (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
                )
                documents = cursor.fetchall()
                if documents:
                    self.update_table_with_data(documents)
                else:
                    QMessageBox.information(self, "Kết quả", "Không tìm thấy văn bản phù hợp!")
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Tìm kiếm thất bại: {e}")
            finally:
                conn.close()

    def update_document_table2(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM outgoingDocuments')
                documents = cursor.fetchall()
                self.update_out_table_with_data(documents)
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi cập nhật bảng: {e}")
            finally:
                conn.close()

    def update_out_table_with_data(self, documents):
        self.tableWidget_2.setRowCount(0)
        for row_number, row_data in enumerate(documents):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def load_file2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Mở file đính kèm", "", "All Files (*);;Text Files (*.txt)")
        if file_name:
            file_name = os.path.basename(file_name)
            self.lineEdit_12.setText(file_name)

    def setup_search_completer2(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT documentNumber FROM outgoingDocuments')
                doc_numbers = [row[0] for row in cursor.fetchall()]
                completer = QCompleter(doc_numbers)
                completer.setCaseSensitivity(0)  
                self.lineEdit_5.setCompleter(completer)  
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi thiết lập gợi ý: {e}")
            finally:
                conn.close()

    def on_item_clicked2(self, item):
        row = item.row()
        doc_number = self.tableWidget_2.item(row, 1).text()  
        title = self.tableWidget_2.item(row, 2).text()  
        recipient = self.tableWidget_2.item(row, 3).text()  
        send_date = self.tableWidget_2.item(row, 4).text()  
        content = self.tableWidget_2.item(row, 5).text()  
        file_attachment = self.tableWidget_2.item(row, 6).text()  
        status = self.tableWidget_2.item(row, 7).text()  
        self.lineEdit_7.setText(doc_number)
        self.lineEdit_9.setText(title)
        self.lineEdit_10.setText(recipient)
        self.dateEdit_2.setDate(QDate.fromString(send_date, 'yyyy-MM-dd'))
        self.lineEdit_11.setText(content)
        self.lineEdit_12.setText(file_attachment)
        self.comboBox_2.setCurrentText(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = OutgoingDocumentWindow() 
    main_window.show()
    sys.exit(app.exec_())
