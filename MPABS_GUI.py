import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from UI.HomePage import HomePage

class MPABS_GUI(QMainWindow):
    def __init__(self):
        self.home_page = HomePage()
        self.home_page.show()

app = QApplication(sys.argv)
win = MPABS_GUI()
sys.exit(app.exec_())