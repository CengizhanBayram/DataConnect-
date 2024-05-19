import sys
from PyQt5.QtWidgets import QApplication,  QTableWidget,QTableWidgetItem ,QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QStackedWidget, QInputDialog, QTextEdit
from PyQt5.QtCore import Qt
import sqlite3
from DataConnect import DataConnect

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
        
        layout.addWidget(QLabel("Create a new table"))
        layout.addWidget(self.table_name_input)
        layout.addWidget(self.columns_input)
        layout.addWidget(create_table_button)
        
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
        
        columns_dict = dict(column.split() for column in columns.split(', '))
        message = self.db.create_table(table_name, **columns_dict)
        QMessageBox.information(self, "Create Table", message)
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
        
        layout.addWidget(self.operation_status)
        
        back_button = QPushButton("Back to Main")
        back_button.clicked.connect(self.back_to_main)
        
        layout.addWidget(back_button)
        
        widget.setLayout(layout)
        
        return widget
        
    def back_to_main(self):
        self.stacked_widget.setCurrentWidget(self.create_table_page)
    def table_operations_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.operation_status = QLabel("Table Operations")
        
        self.add_data_button = QPushButton("Add Data")
        self.add_data_button.clicked.connect(self.add_data_dialog)
        
        self.delete_data_button = QPushButton("Delete Data")
        self.delete_data_button.clicked.connect(self.delete_data_dialog)
        
        self.show_table_button = QPushButton("Show Table Contents")
        self.show_table_button.clicked.connect(self.show_table_contents)
        
        self.table_content_display = QTableWidget()
        
        layout.addWidget(self.operation_status)
        layout.addWidget(self.add_data_button)
        layout.addWidget(self.delete_data_button)
        layout.addWidget(self.show_table_button)
        layout.addWidget(self.table_content_display)
        
        back_button = QPushButton("Back to Main")
        back_button.clicked.connect(self.back_to_main)
        
        layout.addWidget(back_button)
        
        widget.setLayout(layout)
        
        return widget

    def show_table_contents(self):
        table_contents = self.db.show_selected_table()
        if isinstance(table_contents, list):
            num_rows = len(table_contents)
            num_cols = len(table_contents[0])
            self.table_content_display.setRowCount(num_rows)
            self.table_content_display.setColumnCount(num_cols)
            for i in range(num_rows):
                for j in range(num_cols):
                    item = QTableWidgetItem(str(table_contents[i][j]))
                    self.table_content_display.setItem(i, j, item)
        else:
            QMessageBox.warning(self, "Error", table_contents)
        
    def add_data_dialog(self):
        text, ok = QInputDialog.getText(self, "Add Data", "Enter data separated by comma:")
        if ok:
            data = text.split(',')
            message = self.db.add_data(**{self.db.selected_table_columns[i]: data[i].strip() for i in range(len(data))})
            QMessageBox.information(self, "Add Data", message)

    def update_data_dialog(self):
        id, ok = QInputDialog.getInt(self, "Update Data", "Enter ID of the row to update:")
        if ok:
            text, ok = QInputDialog.getText(self, "Update Data", f"Enter new data separated by comma for row with ID {id}:")
            if ok:
                data = text.split(',')
                message = self.db.update_data(id, **{self.db.selected_table_columns[i]: data[i].strip() for i in range(len(data))})
                QMessageBox.information(self, "Update Data", message)

    def delete_data_dialog(self):
        id, ok = QInputDialog.getInt(self, "Delete Data", "Enter ID of the row to delete:")
        if ok:
            message = self.db.delete_data(id)
            QMessageBox.information(self, "Delete Data", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    db_name = "x4sqlite1.db"
    window = MainWindow(db_name)
    window.show()
    
    sys.exit(app.exec_())
