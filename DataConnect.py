import sqlite3

class DataConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.selected_table = None

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

    def search_table(self, table_name):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ?", (f'%{table_name}%',))
            result = self.cursor.fetchall()
            if result:
                return [table[0] for table in result]
            else:
                return []
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

    def add_data(self, *field_values):
        try:
            field_count = len(field_values)
            placeholders = ','.join(['?'] * field_count)
            query = f"INSERT INTO {self.selected_table} VALUES ({placeholders})"
            self.cursor.execute(query, field_values)
            self.conn.commit()
            return 'Veri başarıyla eklendi.'
        except Exception as e:
            return f'Hata: {str(e)}'

    def update_data(self, id, *field_values):
        try:
            field_count = len(field_values)
            placeholders = ','.join(['field{}=?'.format(i+1) for i in range(field_count)])
            query = f"UPDATE {self.selected_table} SET {placeholders} WHERE id=?"
            values = field_values + (id,)
            self.cursor.execute(query, values)
            self.conn.commit()
            return 'Veri başarıyla güncellendi.'
        except Exception as e:
            return f'Hata: {str(e)}'



    def delete_data(self, id):
        try:
            self.cursor.execute(f"DELETE FROM {self.selected_table} WHERE id=?", (id,))
            self.conn.commit()
            return 'Veri başarıyla silindi.'
        except Exception as e:
            return f'Hata: {str(e)}'

    def __del__(self):
        self.conn.close()
