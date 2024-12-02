import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QCompleter, QFileDialog
from PyQt5 import uic
from PyQt5.QtCore import QDate
import os
from PyQt5.QtCore import QStringListModel

class MainWindow(QMainWindow):
    def __init__(self, is_admin=False):
        super().__init__()
        uic.loadUi("trangchu.ui", self)
        # quản lý người dùng
        self.is_admin = is_admin
        self.btnthem.clicked.connect(self.add_user)
        self.btnsua.clicked.connect(self.edit_user)
        self.btnxoa.clicked.connect(self.delete_user)
        self.btntimkiem.clicked.connect(self.search_user)
        self.tbnguoidung.cellClicked.connect(self.on_cell_clicked1)
        self.update_user_table()
        self.update_permissions()
        self.setup_search_completer2()
        #quản lý hồ sơ công việc
        self.pushButton_11.clicked.connect(self.search_work_file)
        self.pushButton_12.clicked.connect(self.add_work_file)
        self.pushButton_13.clicked.connect(self.edit_work_file)
        self.pushButton_14.clicked.connect(self.delete_work_file)
        self.dateEdit_3.setDate(QDate.currentDate())
        self.tableWidget_3.itemClicked.connect(self.on_item_clicked1)
        self.update_work_file_table()
        # quản lý hồ sơ đến
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
        # quản lý hồ sơ đi
        self.pushButton_6.clicked.connect(self.add_document2)
        self.pushButton_7.clicked.connect(self.edit_document2)
        self.pushButton_8.clicked.connect(self.delete_document2)
        self.pushButton_9.clicked.connect(self.search_document2)
        self.pushButton_10.clicked.connect(self.load_file2)
        self.tableWidget_2.itemClicked.connect(self.on_item_clicked2)
        self.dateEdit_2.setDate(QDate.currentDate())
        self.update_document_table2()
        self.setup_search_completer2()
        # quản lý kho tài liệu
        self.pushButton_15.clicked.connect(self.load_file3)
        self.pushButton_16.clicked.connect(self.search_file)
        self.pushButton.clicked.connect(self.add_file)
        self.pushButton_2.clicked.connect(self.edit_file)
        self.pushButton_3.clicked.connect(self.delete_file)
        self.dateEdit_4.setDate(QDate.currentDate())
        self.tableWidget_4.cellClicked.connect(self.on_table_item_clicked3)
        self.update_document_table3()
        # thông tin văn bản
        self.pushButton_17.clicked.connect(self.search_info)  
        self.pushButton_18.clicked.connect(self.add_info)   
        self.pushButton_19.clicked.connect(self.edit_info)  
        self.pushButton_20.clicked.connect(self.delete_info) 
        self.dateEdit_5.setDate(QDate.currentDate())  
        self.update_document_info_table()  
        self.tableWidget_5.cellClicked.connect(self.populate_fields_from_table)
        # thoát ứng dụng
        self.pushButton_21.clicked.connect(self.exit_app)

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None
# quản lý ngươi dùng
    def update_permissions(self):
        if self.is_admin:
            self.btnthem.setEnabled(True)
            self.btnsua.setEnabled(True)
            self.btnxoa.setEnabled(True)
        else:
            self.btnthem.setEnabled(True)
            self.btnsua.setEnabled(True) 
            self.btnxoa.setEnabled(True) 
            self.btnthem.setStyleSheet('background-color: lightgrey;')
            self.btnsua.setStyleSheet('background-color: lightgrey;') 
            self.btnxoa.setStyleSheet('background-color: lightgrey;') 

    def add_user(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Thông báo", "Bạn không có quyền thực hiện hành động này.")
            return
        
        username = self.tdn.text()
        password = self.mk.text()
        fullname = self.hvt_3.text()
        role = self.cn.currentText()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)', 
                               (username, password, fullname, role))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Thêm người dùng thành công!")
                self.update_user_table() 
                self.tdn.clear()
                self.mk.clear()
                self.hvt_3.clear()
                self.cn.setCurrentIndex(0)
                self.clear_line_edits()  
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Thêm người dùng thất bại: {e}")
            finally:
                conn.close()

    def edit_user(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Thông báo", "Bạn không có quyền thực hiện hành động này.")
            return
        
        username = self.tdn.text()
        password = self.mk.text()
        fullname = self.hvt_3.text()
        role = self.cn.currentText()

        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE users SET password = ?, full_name = ?, role = ? WHERE username = ?', 
                               (password, fullname, role, username))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Sửa người dùng thành công!")
                self.update_user_table() 
                self.tdn.clear()
                self.mk.clear()
                self.hvt_3.clear()
                self.cn.setCurrentIndex(0)
                self.clear_line_edits() 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Sửa người dùng thất bại: {e}")
            finally:
                conn.close()

    def delete_user(self):
        if not self.is_admin:
            QMessageBox.warning(self, "Thông báo", "Bạn không có quyền thực hiện hành động này.")
            return
        username = self.tdn.text()
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('DELETE FROM users WHERE username = ?', (username,))
                conn.commit()
                QMessageBox.information(self, "Thông báo", "Xóa người dùng thành công!")
                self.update_user_table()  
                self.clear_line_edits()  
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Xóa người dùng thất bại: {e}")
            finally:
                conn.close()

    def search_user(self):
     search_query = self.timkiem.text().strip() 
     if not search_query: 
        QMessageBox.warning(self, "Thông báo", "Vui lòng nhập thông tin tìm kiếm!")
        return

     conn = self.connect_db()
     if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'SELECT * FROM users WHERE username LIKE ? OR full_name LIKE ?', 
                (f'%{search_query}%', f'%{search_query}%')
            )
            users = cursor.fetchall()
            if users:
                self.update_table_with_data(users)
            else:
                QMessageBox.information(self, "Kết quả", "Không tìm thấy người dùng phù hợp!")
        except Exception as e:
            QMessageBox.warning(self, "Thông báo", f"Tìm kiếm thất bại: {e}")
        finally:
            conn.close()


    def update_user_table(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM users')
                users = cursor.fetchall()
                self.update_user_table_with_data(users)
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi cập nhật bảng: {e}")
            finally:
                conn.close()

    def update_user_table_with_data(self, users):
        self.tbnguoidung.setRowCount(0)
        for row_number, row_data in enumerate(users):
            self.tbnguoidung.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tbnguoidung.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def on_cell_clicked1(self, row, column):
        username = self.tbnguoidung.item(row, 1).text()
        password = self.tbnguoidung.item(row, 2).text()
        fullname = self.tbnguoidung.item(row, 3).text()
        role = self.tbnguoidung.item(row, 4).text()

        self.tdn.setText(username)
        self.mk.setText(password)
        self.hvt_3.setText(fullname)
        self.cn.setCurrentText(role)

    def clear_line_edits(self):
        self.tdn.clear()
        self.mk.clear()
        self.hvt_3.clear()
        self.cn.setCurrentIndex(0) 

    def setup_search_completer2(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT username FROM users')
                usernames = [row[0] for row in cursor.fetchall()]
                completer = QCompleter(usernames)
                completer.setCaseSensitivity(0) 
                self.timkiem.setCompleter(completer) 
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi thiết lập gợi ý: {e}")
            finally:
                conn.close()
# quản lý hồ sơ công việc
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
# quản lý hồ sơ đến
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
# quản lý hồ sơ đi
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
# quản lý kho tài liệu
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
# thông tin văn bản
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
# thoát ứng dụng
    def exit_app(self):
            reply = QMessageBox.question(self, "Thoát", "Bạn có chắc chắn muốn thoát không?", 
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QApplication.quit()     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(is_admin=False) 
    main_window.show()
    sys.exit(app.exec_())
