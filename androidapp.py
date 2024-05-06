from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import sqlite3

class DBBrowser(App):
    def __init__(self, **kwargs):
        super(DBBrowser, self).__init__(**kwargs)
        self.db_name = 'example.db'  # SQLite veritabanı adı
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Sonuçları göstermek için etiket
        self.result_label = Label(text='', size_hint_y=None, height=40)
        layout.add_widget(self.result_label)

        # Sorgu girişi
        self.query_input = TextInput(text='', size_hint_y=None, height=40)
        self.query_input.bind(on_text_validate=self.execute_query)  # Sorguyu çalıştır
        layout.add_widget(self.query_input)

        # Sorguyu çalıştırma düğmesi
        execute_button = Button(text='Sorguyu Çalıştır', size_hint_y=None, height=40)
        execute_button.bind(on_press=self.execute_query)  # Düğmeye tıklanarak da sorguyu çalıştır
        layout.add_widget(execute_button)

        # Ekleme için giriş kutusu ve düğme
        self.add_input = TextInput(hint_text='Ekle: İsim, Yaş', size_hint_y=None, height=40)
        layout.add_widget(self.add_input)
        add_button = Button(text='Ekle', size_hint_y=None, height=40)
        add_button.bind(on_press=self.add_data)
        layout.add_widget(add_button)

        # Güncelleme için giriş kutusu ve düğme
        self.update_input = TextInput(hint_text='Güncelle: ID, Yeni İsim, Yeni Yaş', size_hint_y=None, height=40)
        layout.add_widget(self.update_input)
        update_button = Button(text='Güncelle', size_hint_y=None, height=40)
        update_button.bind(on_press=self.update_data)
        layout.add_widget(update_button)

        # Silme için giriş kutusu ve düğme
        self.delete_input = TextInput(hint_text='Sil: ID', size_hint_y=None, height=40)
        layout.add_widget(self.delete_input)
        delete_button = Button(text='Sil', size_hint_y=None, height=40)
        delete_button.bind(on_press=self.delete_data)
        layout.add_widget(delete_button)

        return layout

    def execute_query(self, instance):
        # Girilen sorguyu çalıştırır
        query = self.query_input.text
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.result_label.text = str(result)
        except Exception as e:
            self.result_label.text = f'Hata: {str(e)}'

    def add_data(self, instance):
        # Veri ekler
        data = self.add_input.text.split(',')
        if len(data) == 2:
            name, age = data
            try:
                self.cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name.strip(), age.strip()))
                self.conn.commit()
                self.result_label.text = 'Veri başarıyla eklendi.'
            except Exception as e:
                self.result_label.text = f'Hata: {str(e)}'
        else:
            self.result_label.text = 'Hatalı veri girişi. İsim ve yaş bilgisi girilmelidir.'

    def update_data(self, instance):
        # Veri günceller
        data = self.update_input.text.split(',')
        if len(data) == 3:
            try:
                id, new_name, new_age = data
                self.cursor.execute("UPDATE users SET name=?, age=? WHERE id=?", (new_name.strip(), new_age.strip(), id.strip()))
                self.conn.commit()
                self.result_label.text = 'Veri başarıyla güncellendi.'
            except Exception as e:
                self.result_label.text = f'Hata: {str(e)}'
        else:
            self.result_label.text = 'Hatalı veri girişi. ID, yeni isim ve yeni yaş bilgileri girilmelidir.'

    def delete_data(self, instance):
        # Veriyi siler
        id = self.delete_input.text
        try:
            self.cursor.execute("DELETE FROM users WHERE id=?", (id,))
            self.conn.commit()
            self.result_label.text = 'Veri başarıyla silindi.'
        except Exception as e:
            self.result_label.text = f'Hata: {str(e)}'

if __name__ == '__main__':
    DBBrowser().run()
