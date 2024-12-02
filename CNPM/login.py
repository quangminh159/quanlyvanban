import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dangnhap.ui", self) 
        self.password.setEchoMode(2)  
        self.btndangnhap.clicked.connect(self.login)
        self.btnthoat.clicked.connect(self.close)
        self.cbpass.stateChanged.connect(self.toggle_password_visibility)

        self.is_admin = False 
    def connect_db(self):
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=QUANGMINH;DATABASE=qlvanban;UID=sa;PWD=sa'
        try:
            conn = pyodbc.connect(conn_str)
            return conn
        except Exception as e:
            print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            return None

    def check_credentials(self, username, password):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()
            return user
        return None

    def toggle_password_visibility(self):
        if self.cbpass.isChecked():
            self.password.setEchoMode(0)
        else:
            self.password.setEchoMode(2) 

    def login(self):
        username = self.namelogin.text()
        password = self.password.text()

        user = self.check_credentials(username, password)
        
        if user:
            if user[4] == 'Admin': 
                self.is_admin = True 
                QMessageBox.information(self, "Thông báo", "Đăng nhập thành công với quyền Admin!")
            else:
                self.is_admin = False
                QMessageBox.information(self, "Thông báo", "Đăng nhập thành công với quyền nhân viên!")
            self.close()  
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc mật khẩu")
    
    def open_main_window(self):
        from main_window import MainWindow 
        self.main_window = MainWindow(is_admin=self.is_admin)
        self.main_window.show()
