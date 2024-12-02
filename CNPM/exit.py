import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTabWidget, QMessageBox
from PyQt5 import uic

class ExitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("trangchu.ui", self) 
        self.pushButton_21.clicked.connect(self.exit_app)
        
    def exit_app(self):
        reply = QMessageBox.question(self, "Thoát", "Bạn có chắc chắn muốn thoát không?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit() 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = ExitWindow()
    main_window.show()
    sys.exit(app.exec_())
