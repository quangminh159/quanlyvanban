import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QCompleter
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel

class UserManagementWindow(QMainWindow):
    def __init__(self, is_admin=False):
        super().__init__()
        uic.loadUi("trangchu.ui", self) 
        self.is_admin = is_admin
        self.btnthem.clicked.connect(self.add_user)
        self.btnsua.clicked.connect(self.edit_user)
        self.btnxoa.clicked.connect(self.delete_user)
        self.btntimkiem.clicked.connect(self.search_user)
        self.tbnguoidung.cellClicked.connect(self.on_cell_clicked)
        self.update_user_table()
        self.update_permissions()
        self.setup_search_completer1()

    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def update_permissions(self):
        if self.is_admin:
            self.btnthem.setEnabled(True)
            self.btnsua.setEnabled(True)
            self.btnxoa.setEnabled(True)
        else:
            self.btnthem.setEnabled(False)
            self.btnsua.setEnabled(False)
            self.btnxoa.setEnabled(False)
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
        # Cập nhật bảng người dùng từ cơ sở dữ liệu
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute('SELECT * FROM users')
                users = cursor.fetchall()
                self.update_table_with_data(users)
            except Exception as e:
                QMessageBox.warning(self, "Thông báo", f"Lỗi khi cập nhật bảng: {e}")
            finally:
                conn.close()

    def update_table_with_data(self, users):
        self.tbnguoidung.setRowCount(0)
        for row_number, row_data in enumerate(users):
            self.tbnguoidung.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tbnguoidung.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def on_cell_clicked(self, row, column):
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

    def setup_search_completer1(self):
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_management_window = UserManagementWindow(is_admin=True)  
    user_management_window.show()
    sys.exit(app.exec_())
