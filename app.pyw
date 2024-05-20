import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QStackedWidget, QInputDialog, QHBoxLayout

class DataConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.selected_table = None

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return 'Sorgu başarıyla çalıştırıldı.'
        except Exception as e:
            return f'Hata: {str(e)}'

    def select_table(self, table_name):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = self.cursor.fetchone()
            if result:
                self.selected_table = table_name
                return f"'{table_name}' tablosu seçildi."
            else:
                return f"'{table_name}' adında bir tablo bulunamadı."
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_all_tables(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result = self.cursor.fetchall()
            return [table[0] for table in result]
        except Exception as e:
            return f'Hata: {str(e)}'

    def show_selected_table(self):
        if self.selected_table:
            try:
                self.cursor.execute(f"SELECT * FROM {self.selected_table}")
                result = self.cursor.fetchall()
                return result
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def add_data(self, **field_values):
        if self.selected_table:
            try:
                columns = ', '.join(field_values.keys())
                placeholders = ', '.join(['?'] * len(field_values))
                query = f"INSERT INTO {self.selected_table} ({columns}) VALUES ({placeholders})"
                self.cursor.execute(query, tuple(field_values.values()))
                self.conn.commit()
                return 'Veri başarıyla eklendi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def update_data(self, id, **field_values):
        if self.selected_table:
            try:
                placeholders = ', '.join([f"{k} = ?" for k in field_values.keys()])
                query = f"UPDATE {self.selected_table} SET {placeholders} WHERE id = ?"
                values = tuple(field_values.values()) + (id,)
                self.cursor.execute(query, values)
                self.conn.commit()
                return 'Veri başarıyla güncellendi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def delete_data(self, id):
        if self.selected_table:
            try:
                self.cursor.execute(f"DELETE FROM {self.selected_table} WHERE id = ?", (id,))
                self.conn.commit()
                return 'Veri başarıyla silindi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def create_table(self, table_name, **columns):
        try:
            columns_def = ', '.join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])
            self.cursor.execute(f"CREATE TABLE {table_name} ({columns_def})")
            self.conn.commit()
            return f"'{table_name}' tablosu başarıyla oluşturuldu."
        except Exception as e:
            return f'Hata: {str(e)}'

    def delete_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
            return f"'{table_name}' tablosu başarıyla silindi."
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_table_columns(self, table_name):
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            result = self.cursor.fetchall()
            return [column[1] for column in result]
        except Exception as e:
            return f'Hata: {str(e)}'

    def __del__(self):
        self.conn.close()

class MainWindow(QWidget):
    def __init__(self, db_name):
        super().__init__()
        self.setWindowTitle("SQLite Database Browser")
        self.setGeometry(100, 100, 600, 400)

        self.db = DataConnect(db_name)

        self.main_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()

        self.create_table_page = self.create_table_ui()
        self.table_operations_page = self.table_operations_ui()

        self.stacked_widget.addWidget(self.create_table_page)
        self.stacked_widget.addWidget(self.table_operations_page)

        self.main_layout.addWidget(self.stacked_widget)

        self.setLayout(self.main_layout)

    def create_table_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.table_name_input = QLineEdit()
        self.table_name_input.setPlaceholderText("Table Name")

        self.columns_input = QLineEdit()
        self.columns_input.setPlaceholderText("Columns (e.g. id INTEGER PRIMARY KEY, name TEXT)")

        create_table_button = QPushButton("Create Table")
        create_table_button.clicked.connect(self.create_table)

        delete_table_button = QPushButton("Delete Table")
        delete_table_button.clicked.connect(self.delete_table)

        layout.addWidget(QLabel("Create a new table"))
        layout.addWidget(self.table_name_input)
        layout.addWidget(self.columns_input)
        layout.addWidget(create_table_button)
        layout.addWidget(delete_table_button)

        self.table_list = QListWidget()
        self.table_list.itemClicked.connect(self.select_table)

        layout.addWidget(QLabel("Existing Tables"))
        layout.addWidget(self.table_list)

        show_tables_button = QPushButton("Show Tables")
        show_tables_button.clicked.connect(self.show_tables)

        layout.addWidget(show_tables_button)

        widget.setLayout(layout)

        return widget

    def create_table(self):
        table_name = self.table_name_input.text()
        columns = self.columns_input.text()

        if not table_name or not columns:
            QMessageBox.warning(self, "Input Error", "Table name and columns are required")
            return

        columns_dict = {col.split()[0]: col.split()[1] for col in columns.split(', ')}
        message = self.db.create_table(table_name, **columns_dict)
        QMessageBox.information(self, "Create Table", message)
        self.show_tables()

    def delete_table(self):
        table_name = self.table_name_input.text()

        if not table_name:
            QMessageBox.warning(self, "Input Error", "Table name is required")
            return

        message = self.db.delete_table(table_name)
        QMessageBox.information(self, "Delete Table", message)
        self.show_tables()

    def show_tables(self):
        tables = self.db.get_all_tables()
        self.table_list.clear()
        if isinstance(tables, list):
            self.table_list.addItems(tables)
        else:
            QMessageBox.warning(self, "Error", tables)

    def select_table(self, item):
        table_name = item.text()
        message = self.db.select_table(table_name)
        QMessageBox.information(self, "Select Table", message)
        self.stacked_widget.setCurrentWidget(self.table_operations_page)

    def table_operations_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.operation_status = QLabel("Table Operations")

        self.add_data_button = QPushButton("Add Data")
        self.add_data_button.clicked.connect(self.add_data_dialog)

        self.show_table_button = QPushButton("Show Table Contents")
        self.show_table_button.clicked.connect(self.show_table_contents)

        self.update_data_button = QPushButton("Update Data")
        self.update_data_button.clicked.connect(self.update_data_dialog)

        self.delete_data_button = QPushButton("Delete Data")
        self.delete_data_button.clicked.connect(self.delete_data_dialog)

        self.table_content_display = QTableWidget()

        layout.addWidget(self.operation_status)
        layout.addWidget(self.add_data_button)
        layout.addWidget(self.update_data_button)
        layout.addWidget(self.delete_data_button)
        layout.addWidget(self.show_table_button)
        layout.addWidget(self.table_content_display)

        back_button = QPushButton("Back to Main")
        back_button.clicked.connect(self.back_to_main)

        layout.addWidget(back_button)

        widget.setLayout(layout)

        return widget

    def add_data_dialog(self):
        column_names = self.db.get_table_columns(self.db.selected_table)
        if column_names:
            rows, ok = QInputDialog.getInt(self, "Add Data", "Enter number of rows:")
            if ok:
                cols, ok = QInputDialog.getInt(self, "Add Data", "Enter number of columns:")
                if ok:
                    self.data_input_table = QTableWidget(rows, cols)
                    self.data_input_table.setHorizontalHeaderLabels(column_names[:cols])
                    
                    save_button = QPushButton("Save Data")
                    save_button.clicked.connect(self.save_data)

                    layout = QVBoxLayout()
                    layout.addWidget(self.data_input_table)
                    layout.addWidget(save_button)

                    data_input_dialog = QWidget()
                    data_input_dialog.setLayout(layout)
                    data_input_dialog.setGeometry(150, 150, 400, 300)
                    data_input_dialog.show()
                    self.data_input_dialog = data_input_dialog
        else:
            QMessageBox.warning(self, "Error", "No table selected")

    def update_data_dialog(self):
        column_names = self.db.get_table_columns(self.db.selected_table)
        if column_names:
            id, ok = QInputDialog.getInt(self, "Update Data", "Enter ID of the row to update:")
            if ok:
                self.data_input_table = QTableWidget(1, len(column_names))
                self.data_input_table.setHorizontalHeaderLabels(column_names)
                
                save_button = QPushButton("Update Data")
                save_button.clicked.connect(lambda: self.update_data(id))

                layout = QVBoxLayout()
                layout.addWidget(self.data_input_table)
                layout.addWidget(save_button)

                data_input_dialog = QWidget()
                data_input_dialog.setLayout(layout)
                data_input_dialog.setGeometry(150, 150, 400, 300)
                data_input_dialog.show()
                self.data_input_dialog = data_input_dialog
        else:
            QMessageBox.warning(self, "Error", "No table selected")

    def delete_data_dialog(self):
        id, ok = QInputDialog.getInt(self, "Delete Data", "Enter ID of the row to delete:")
        if ok:
            message = self.db.delete_data(id)
            QMessageBox.information(self, "Delete Data", message)
            self.show_table_contents()

    def save_data(self):
        rows = self.data_input_table.rowCount()
        cols = self.data_input_table.columnCount()
        data = []
        for row in range(rows):
            row_data = {}
            for col in range(cols):
                item = self.data_input_table.item(row, col)
                if item is not None:
                    row_data[self.data_input_table.horizontalHeaderItem(col).text()] = item.text()
            data.append(row_data)

        for row_data in data:
            message = self.db.add_data(**row_data)
            QMessageBox.information(self, "Add Data", message)

        self.data_input_dialog.close()
        self.show_table_contents()

    def update_data(self, id):
        cols = self.data_input_table.columnCount()
        row_data = {}
        for col in range(cols):
            item = self.data_input_table.item(0, col)
            if item is not None:
                row_data[self.data_input_table.horizontalHeaderItem(col).text()] = item.text()

        message = self.db.update_data(id, **row_data)
        QMessageBox.information(self, "Update Data", message)

        self.data_input_dialog.close()
        self.show_table_contents()

    def show_table_contents(self):
        table_contents = self.db.show_selected_table()
        if isinstance(table_contents, list):
            num_rows = len(table_contents)
            if num_rows > 0:
                num_cols = len(table_contents[0])
                self.table_content_display.setRowCount(num_rows)
                self.table_content_display.setColumnCount(num_cols)
                for i in range(num_rows):
                    for j in range(num_cols):
                        item = QTableWidgetItem(str(table_contents[i][j]))
                        self.table_content_display.setItem(i, j, item)
            else:
                self.table_content_display.setRowCount(0)
                self.table_content_display.setColumnCount(0)
        else:
            QMessageBox.warning(self, "Error", table_contents)

    def back_to_main(self):
        self.stacked_widget.setCurrentWidget(self.create_table_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_name = "x4sqlite1.db"
    window = MainWindow(db_name)
    window.show()

    sys.exit(app.exec_())