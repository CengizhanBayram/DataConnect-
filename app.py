import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon

class DBBrowser(QWidget):
    def __init__(self):
        super().__init__()
        # SQLite veritabanı bağlantısı oluştur
        self.db_name = 'example.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # Arayüzü başlat
        self.initUI()

    def initUI(self):
        # Pencere başlığını ve simgesini ayarla
        self.setWindowTitle('SQLite DB Tarayıcı')
        self.setWindowIcon(QIcon('icon.png'))
        
        # Ana düzen oluştur
        main_layout = QVBoxLayout()

        # Sonuçları göstermek için etiket
        self.result_label = QLabel()
        main_layout.addWidget(self.result_label)

        # Sorgu girişi
        query_layout = QHBoxLayout()
        query_layout.addWidget(QLabel('SQL Sorgusu: '))
        self.query_input = QLineEdit()
        self.query_input.returnPressed.connect(self.execute_query)
        query_layout.addWidget(self.query_input)
        main_layout.addLayout(query_layout)

        # Sorguyu çalıştırma düğmesi
        execute_button = QPushButton('Sorguyu Çalıştır')
        execute_button.clicked.connect(self.execute_query)
        main_layout.addWidget(execute_button)

        # Ekleme için giriş kutusu ve düğme
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel('Ekle: İsim, Yaş'))
        self.add_input = QLineEdit()
        add_layout.addWidget(self.add_input)
        add_button = QPushButton('Ekle')
        add_button.clicked.connect(self.add_data)
        add_layout.addWidget(add_button)
        main_layout.addLayout(add_layout)

        # Güncelleme için giriş kutusu ve düğme
        update_layout = QHBoxLayout()
        update_layout.addWidget(QLabel('Güncelle: ID, Yeni İsim, Yeni Yaş'))
        self.update_input = QLineEdit()
        update_layout.addWidget(self.update_input)
        update_button = QPushButton('Güncelle')
        update_button.clicked.connect(self.update_data)
        update_layout.addWidget(update_button)
        main_layout.addLayout(update_layout)

        # Silme için giriş kutusu ve düğme
        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel('Sil: ID'))
        self.delete_input = QLineEdit()
        delete_layout.addWidget(self.delete_input)
        delete_button = QPushButton('Sil')
        delete_button.clicked.connect(self.delete_data)
        delete_layout.addWidget(delete_button)
        main_layout.addLayout(delete_layout)

        # Ana düzeni ayarla
        self.setLayout(main_layout)

    def execute_query(self):
        # Girilen sorguyu çalıştırır
        query = self.query_input.text()
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.result_label.setText(str(result))
        except Exception as e:
            QMessageBox.critical(self, 'Hata', str(e))

    def add_data(self):
        # Veri ekler
        data = self.add_input.text().split(',')
        if len(data) == 2:
            name, age = data
            try:
                self.cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name.strip(), age.strip()))
                self.conn.commit()
                QMessageBox.information(self, 'Bilgi', 'Veri başarıyla eklendi.')
            except Exception as e:
                QMessageBox.critical(self, 'Hata', str(e))
        else:
            QMessageBox.warning(self, 'Uyarı', 'Hatalı veri girişi. İsim ve yaş bilgisi girilmelidir.')

    def update_data(self):
        # Veri günceller
        data = self.update_input.text().split(',')
        if len(data) == 3:
            try:
                id, new_name, new_age = data
                self.cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (new_name.strip(), new_age.strip(), id.strip()))
                self.conn.commit()
                QMessageBox.information(self, 'Bilgi', 'Veri başarıyla güncellendi.')
            except Exception as e:
                QMessageBox.critical(self, 'Hata', str(e))
        else:
            QMessageBox.warning(self, 'Uyarı', 'Hatalı veri girişi. ID, yeni isim ve yeni yaş bilgileri girilmelidir.')

    def delete_data(self):
        # Veriyi siler
        id = self.delete_input.text()
        try:
            self.cursor.execute("DELETE FROM users WHERE id=?", (id,))
            self.conn.commit()
            QMessageBox.information(self, 'Bilgi', 'Veri başarıyla silindi.')
        except Exception as e:
            QMessageBox.critical(self, 'Hata', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DBBrowser()
    window.show()
    sys.exit(app.exec_())