import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from DataConnect import DataConnect

class DBBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.db_backend = DataConnect('example.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SQLite DB Tarayıcı')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        self.result_label = QLabel()
        main_layout.addWidget(self.result_label)

        query_layout = QHBoxLayout()
        query_layout.addWidget(QLabel('Veri Arama: '))
        self.query_input = QLineEdit()
        query_layout.addWidget(self.query_input)
        search_button = QPushButton('Ara')
        search_button.clicked.connect(self.search_data)
        query_layout.addWidget(search_button)
        main_layout.addLayout(query_layout)

        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel('İsim:'))
        self.add_name_input = QLineEdit()
        add_layout.addWidget(self.add_name_input)
        add_layout.addWidget(QLabel('Yaş:'))
        self.add_age_input = QLineEdit()
        add_layout.addWidget(self.add_age_input)
        add_button = QPushButton('Ekle')
        add_button.clicked.connect(self.add_data)
        add_layout.addWidget(add_button)
        main_layout.addLayout(add_layout)

        update_layout = QHBoxLayout()
        update_layout.addWidget(QLabel('Güncelle ID:'))
        self.update_id_input = QLineEdit()
        update_layout.addWidget(self.update_id_input)
        update_layout.addWidget(QLabel('Yeni İsim:'))
        self.update_name_input = QLineEdit()
        update_layout.addWidget(self.update_name_input)
        update_layout.addWidget(QLabel('Yeni Yaş:'))
        self.update_age_input = QLineEdit()
        update_layout.addWidget(self.update_age_input)
        update_button = QPushButton('Güncelle')
        update_button.clicked.connect(self.update_data)
        update_layout.addWidget(update_button)
        main_layout.addLayout(update_layout)

        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel('Sil ID:'))
        self.delete_id_input = QLineEdit()
        delete_layout.addWidget(self.delete_id_input)
        delete_button = QPushButton('Sil')
        delete_button.clicked.connect(self.delete_data)
        delete_layout.addWidget(delete_button)
        main_layout.addLayout(delete_layout)

        self.setLayout(main_layout)

    def show_all_data(self):
        result = self.db_backend.get_all_data()
        self.display_result(result)

    def search_data(self):
        name = self.query_input.text()
        result = self.db_backend.get_user_data(name)
        self.display_result([result])

    def add_data(self):
        name = self.add_name_input.text()
        age = self.add_age_input.text()
        result = self.db_backend.add_data(name, age)
        QMessageBox.information(self, 'Bilgi', result)
        self.show_all_data()

    def update_data(self):
        id = self.update_id_input.text()
        new_name = self.update_name_input.text()
        new_age = self.update_age_input.text()
        result = self.db_backend.update_data(id, new_name, new_age)
        QMessageBox.information(self, 'Bilgi', result)
        self.show_all_data()

    def delete_data(self):
        id = self.delete_id_input.text()
        result = self.db_backend.delete_data(id)
        QMessageBox.information(self, 'Bilgi', result)
        self.show_all_data()

    def display_result(self, result):
        self.table.clear()
        column_names = self.db_backend.get_column_names()  # Doğrudan DataConnect sınıfından sütun adlarını alın
        self.table.setColumnCount(len(column_names))
        self.table.setRowCount(len(result))

        # Sütun adları listesini dize listesi olarak ayarlayın
        self.table.setHorizontalHeaderLabels([str(name) for name in column_names])

        for i, row in enumerate(result):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                self.table.setItem(i, j, item)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DBBrowser()
    window.show()
    window.show_all_data()
    sys.exit(app.exec_())
