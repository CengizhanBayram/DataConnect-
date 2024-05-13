import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QMessageBox
from DataConnect import DataConnect

class TableView(QDialog):
    def __init__(self, data, data_connector):
        super().__init__()

        self.setWindowTitle("Tablo Görünümü")
        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(item)))

        self.layout.addWidget(self.table_widget)

        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_data_dialog)
        self.update_button = QPushButton("Güncelle")
        self.update_button.clicked.connect(self.update_data_dialog)
        self.delete_button = QPushButton("Sil")
        self.delete_button.clicked.connect(self.delete_data)
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.update_button)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.data_connector = data_connector

    def add_data_dialog(self):
        dialog = AddDataDialog(self, self.data_connector)
        if dialog.exec_():
            self.update_table()

    def update_data_dialog(self):
        selected_items = self.table_widget.selectedItems()
        if len(selected_items) == 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen güncellemek için bir satır seçin.")
            return
        row_index = selected_items[0].row()
        row_id = self.table_widget.item(row_index, 0).text()  # Assuming the first column is ID
        row_data = [self.table_widget.item(row_index, i).text() for i in range(1, self.table_widget.columnCount())]
        dialog = UpdateDataDialog(self, row_id, row_data, self.data_connector)
        if dialog.exec_():
            self.update_table()

    def delete_data(self):
        selected_items = self.table_widget.selectedItems()
        if len(selected_items) == 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir satır seçin.")
            return
        row_index = selected_items[0].row()
        id = self.table_widget.item(row_index, 0).text()  # Assuming the first column is ID
        confirm = QMessageBox.question(self, "Onay", "Seçilen veriyi silmek istediğinize emin misiniz?",
                                        QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.data_connector.delete_data(id)
            self.update_table()

    def update_table(self):
        data = self.data_connector.show_selected_table()
        if data:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data[0]))
            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(item)))

class AddDataDialog(QDialog):
    def __init__(self, parent=None, data_connector=None):
        super().__init__(parent)

        self.setWindowTitle("Veri Ekle")
        self.layout = QVBoxLayout()

        self.name_label = QLabel("İsim:")
        self.name_edit = QLineEdit()
        self.age_label = QLabel("Yaş:")
        self.age_edit = QLineEdit()

        self.add_button = QPushButton("Ekle")
        self.add_button.clicked.connect(self.add_data)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(self.age_label)
        self.layout.addWidget(self.age_edit)
        self.layout.addWidget(self.add_button)

        self.setLayout(self.layout)

        self.data_connector = data_connector

    def add_data(self):
        name = self.name_edit.text()
        age = self.age_edit.text()
        if name and age:
            self.data_connector.add_data(name, age)
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen isim ve yaş alanlarını doldurun.")

class UpdateDataDialog(QDialog):
    def __init__(self, parent=None, row_id=None, row_data=None, data_connector=None):
        super().__init__(parent)

        self.setWindowTitle("Veri Güncelle")
        self.layout = QVBoxLayout()

        self.fields = []
        self.field_labels = []
        self.field_edits = []

        # Assuming row_data contains field values, and row_id is the ID of the row to be updated
        for i, field_value in enumerate(row_data):
            field_label = QLabel(f"Field {i+2}:")
            field_edit = QLineEdit(field_value)
            self.field_labels.append(field_label)
            self.field_edits.append(field_edit)
            field_layout = QHBoxLayout()
            field_layout.addWidget(field_label)
            field_layout.addWidget(field_edit)
            self.layout.addLayout(field_layout)
            self.fields.append((field_label, field_edit))

        self.update_button = QPushButton("Güncelle")
        self.update_button.clicked.connect(self.update_data)

        self.layout.addWidget(self.update_button)

        self.setLayout(self.layout)

        self.row_id = row_id
        self.data_connector = data_connector

    def update_data(self):
        # Collect field values from QLineEdit widgets
        field_values = [field_edit.text() for field_edit in self.field_edits]

        if all(field_values):
            # Assuming row_id is the first column (ID) of the table
            result = self.data_connector.update_data(self.row_id, *field_values)
            QMessageBox.information(self, "Bilgi", result)
            self.accept()
        else:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun.")

class MainWidget(QWidget):
    def __init__(self, data_connector):
        super().__init__()

        self.data_connector = data_connector

        self.layout = QVBoxLayout()

        self.search_label = QLabel("Tablo Arama:")
        self.search_edit = QLineEdit()
        self.search_edit.textChanged.connect(self.search_tables)

        self.table_combo_box = QComboBox()
        self.table_combo_box.addItems(self.data_connector.get_all_tables())
        self.table_combo_box.currentIndexChanged.connect(self.show_table)

        self.show_table_button = QPushButton("Tabloyu Göster")
        self.show_table_button.clicked.connect(self.show_table)

        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_edit)
        self.layout.addWidget(QLabel("Lütfen bir tablo seçin:"))
        self.layout.addWidget(self.table_combo_box)
        self.layout.addWidget(self.show_table_button)

        self.setLayout(self.layout)

    def search_tables(self):
        search_text = self.search_edit.text()
        if search_text:
            tables = self.data_connector.search_table(search_text)
            self.table_combo_box.clear()
            self.table_combo_box.addItems(tables)
        else:
            self.table_combo_box.clear()
            self.table_combo_box.addItems(self.data_connector.get_all_tables())

    def show_table(self):
        selected_table = self.table_combo_box.currentText()
        if selected_table:
            self.data_connector.select_table(selected_table)
            data = self.data_connector.show_selected_table()
            if data:
                self.table_view = TableView(data, self.data_connector)
                self.table_view.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    data_connector = DataConnect("x4sqlite1.db")
    main_widget = MainWidget(data_connector)
    main_widget.show()
    sys.exit(app.exec_())
