import sqlite3

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
            result = self.cursor.fetchall()
            return 'Sorgu başarıyla çalıştırıldı.', result
        except Exception as e:
            return f'Hata: {str(e)}', []

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

    def delete_data_by_row(self, row_num):
        if self.selected_table:
            try:
                self.cursor.execute(f"DELETE FROM {self.selected_table} WHERE rowid = ?", (row_num,))
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