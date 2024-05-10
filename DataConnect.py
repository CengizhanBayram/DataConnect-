import sqlite3

class DataConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def add_data(self, name, age):
        try:
            self.cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name.strip(), age.strip()))
            self.conn.commit()
            return 'Veri başarıyla eklendi.'
        except Exception as e:
            return f'Hata: {str(e)}'

    def update_data(self, id, new_name, new_age):
        try:
            self.cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (new_name.strip(), new_age.strip(), id.strip()))
            self.conn.commit()
            return 'Veri başarıyla güncellendi.'
        except Exception as e:
            return f'Hata: {str(e)}'

    def delete_data(self, id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id=?", (id,))
            self.conn.commit()
            return 'Veri başarıyla silindi.'
        except Exception as e:
            return f'Hata: {str(e)}'
        
    def sql_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return f'Hata: {str(e)}'    

    def get_all_data(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_column_names(self):
        try:
            self.cursor.execute("PRAGMA table_info(users)")
            result = self.cursor.fetchall()
            return [col[1] for col in result]
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_user_data(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            result = self.cursor.fetchone() # Tek bir kullanıcı döndürür
            return result
        except Exception as e:
            return f'Hata: {str(e)}'

    def __del__(self):
        self.conn.close()
