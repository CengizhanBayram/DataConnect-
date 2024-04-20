from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
import sys
from PyQt5 import QtWidgets

class app:
    def __init__(self) -> None:
        pass


    def window(self):

        app = QApplication(sys.argv)
        wind = QMainWindow()
        wind.setWindowTitle('Data-Connect')
        wind.setWindowIcon(QIcon('icon.png'))

        lbl_name = QtWidgets.QLabel(wind)
        lbl_name.setText("name:")
        lbl_name.move(50,30)

        lbl_surname = QtWidgets.QLabel(wind)
        lbl_surname.setText("surname:")
        lbl_surname.move(50,70)

        txt_name = QtWidgets.QLineEdit(wind)
        txt_name.move(100,30)

        txt_surname = QtWidgets.QLineEdit(wind)
        txt_surname.move(100,70)


        def clicked(self):
            print("kaydedildi")
        btn_save = QtWidgets.QPushButton(wind)
        btn_save.setText('giriniz')
        btn_save.move(100, 120)

        btn_save.clicked.connect(clicked)

        wind.show()
        sys.exit(app.exec_())
         
if __name__ == "__main__":
    app = app()
    app.window()
