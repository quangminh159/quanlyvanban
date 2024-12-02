import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QCompleter, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate
import os

class IncomingDocumentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self)
        self.ngaynhan.setDate(QDate.currentDate())
        self.btnthem_2.clicked.connect(self.add_document1)
        self.btnsua_2.clicked.connect(self.edit_document1)
        self.btnxoa_2.clicked.connect(self.delete_document1)
        self.pushButton.clicked.connect(self.search_document1)
        self.loadfile.clicked.connect(self.load_file1)
        self.btntimkiem_2.clicked.connect(self.search_document1)
        self.ngaynhan.setDate(QDate.currentDate())
        self.update_document_table1()
        self.setup_search_completer1()
        self.tableWidget.cellClicked.connect(self.on_table_item_clicked1)

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def add_document1(self):
        doc_number = self.shvb.text()
        title = self.tieude.text()
        sender = self.noigui.text()
        file_attachment = self.filedinhkem.text()
        content = self.noidung.toPlainText()
        status = self.trangthai.currentText()
        receive_date = self.ngaynhan.date().toString('yyyy-MM-dd')

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO incomingDocuments (documentNumber, title, sender, receivedDate, content, attachment, status) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                               (doc_number, title, sender, receive_date, content, file_attachment, status))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Thêm văn bản thành công!")
                self.shvb.clear()
                self.tieude.clear()
                self.noigui.clear()
                self.filedinhkem.clear()
                self.noidung.clear()
                self.trangthai.setCurrentIndex(0)
                self.ngaynhan.setDate(QDate.currentDate())

                self.update_document_table() 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Thêm văn bản thất bại: {e}")
            finally:
                conn.close()

    def edit_document1(self):
        doc_number = self.shvb.text()
        title = self.tieude.text()
        sender = self.noigui.text()
        file_attachment = self.filedinhkem.text()
        content = self.noidung.toPlainText()
        status = self.trangthai.currentText()
        receive_date = self.ngaynhan.date().toString('yyyy-MM-dd')

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE incomingDocuments SET title = ?, sender = ?, receivedDate = ?, content = ?, attachment = ?, status = ? WHERE documentNumber = ?', 
                               (title, sender, receive_date, content, file_attachment, status, doc_number))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Sửa văn bản thành công!")
                self.shvb.clear()
                self.tieude.clear()
                self.noigui.clear()
                self.filedinhkem.clear()
                self.noidung.clear()
                self.trangthai.setCurrentIndex(0)
                self.ngaynhan.setDate(QDate.currentDate())
                self.update_document_table()  
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Sửa văn bản thất bại: {e}")
            finally:
                conn.close()

    def delete_document1(self):
        doc_number = self.shvb.text()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM incomingDocuments WHERE documentNumber = ?', (doc_number,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa văn bản thành công!")
                self.update_document_table() 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Xóa văn bản thất bại: {e}")
            finally:
                conn.close()

    def search_document1(self):
        search_query = self.lntimkeim.text().strip() 
        if not search_query:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập thông tin tìm kiếm!")
            return
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                'SELECT * FROM incomingDocuments WHERE documentNumber LIKE ? OR title LIKE ? OR sender LIKE ? OR content LIKE ? OR attachment LIKE ? OR status LIKE ?', 
                (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
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

    def update_document_table1(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM incomingDocuments') 
                documents = cursor.fetchall()
                self.update_in_table_with_data(documents)
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi cập nhật bảng: {e}")
            finally:
                conn.close()

    def update_in_table_with_data(self, documents):
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(documents):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def load_file1(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Mở file đính kèm", "", "All Files (*);;Text Files (*.txt)")
        if file_name:
            file_name = os.path.basename(file_name)
            self.filedinhkem.setText(file_name)

    def setup_search_completer1(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT documentNumber FROM incomingDocuments')
                doc_numbers = [row[0] for row in cursor.fetchall()]
                completer = QCompleter(doc_numbers)
                completer.setCaseSensitivity(0) 
                self.lntimkeim.setCompleter(completer) 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi thiết lập gợi ý: {e}")
            finally:
                conn.close()

    def on_table_item_clicked1(self, row, column):
        doc_number = self.tableWidget.item(row, 1).text()  
        title = self.tableWidget.item(row, 2).text()  
        sender = self.tableWidget.item(row, 3).text() 
        receive_date = self.tableWidget.item(row, 4).text()  
        content = self.tableWidget.item(row, 5).text() 
        file_attachment = self.tableWidget.item(row, 6).text()  
        status = self.tableWidget.item(row, 7).text() 
        self.shvb.setText(doc_number)
        self.tieude.setText(title)
        self.noigui.setText(sender)
        self.ngaynhan.setDate(QDate.fromString(receive_date, 'yyyy-MM-dd'))
        self.noidung.setPlainText(content)
        self.filedinhkem.setText(file_attachment)
        self.trangthai.setCurrentText(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = IncomingDocumentWindow() 
    main_window.show()
    sys.exit(app.exec_())
