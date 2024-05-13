from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from DataConnect import DataConnect

class AndroidApp(App):
    def __init__(self, **kwargs):
        super(AndroidApp, self).__init__(**kwargs)
        self.db_backend = DataConnect('example.db')

    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.result_label = Label(text='', size_hint_y=None, height=40)
        layout.add_widget(self.result_label)

        query_layout = BoxLayout(orientation='horizontal')
        query_layout.add_widget(Label(text='Veri Arama:'))
        self.query_input = TextInput()
        query_layout.add_widget(self.query_input)
        search_button = Button(text='Ara')
        search_button.bind(on_press=self.search_data)
        query_layout.add_widget(search_button)
        layout.add_widget(query_layout)

        self.table_label = Label(text='Sonuçlar:', size_hint_y=None, height=40)
        layout.add_widget(self.table_label)

        self.table = BoxLayout(orientation='vertical')
        layout.add_widget(self.table)

        add_layout = BoxLayout(orientation='horizontal')
        add_layout.add_widget(Label(text='İsim:'))
        self.add_name_input = TextInput()
        add_layout.add_widget(self.add_name_input)
        add_layout.add_widget(Label(text='Yaş:'))
        self.add_age_input = TextInput()
        add_layout.add_widget(self.add_age_input)
        add_button = Button(text='Ekle')
        add_button.bind(on_press=self.add_data)
        add_layout.add_widget(add_button)
        layout.add_widget(add_layout)

        update_layout = BoxLayout(orientation='horizontal')
        update_layout.add_widget(Label(text='Güncelle ID:'))
        self.update_id_input = TextInput()
        update_layout.add_widget(self.update_id_input)
        update_layout.add_widget(Label(text='Yeni İsim:'))
        self.update_name_input = TextInput()
        update_layout.add_widget(self.update_name_input)
        update_layout.add_widget(Label(text='Yeni Yaş:'))
        self.update_age_input = TextInput()
        update_layout.add_widget(self.update_age_input)
        update_button = Button(text='Güncelle')
        update_button.bind(on_press=self.update_data)
        update_layout.add_widget(update_button)
        layout.add_widget(update_layout)

        delete_layout = BoxLayout(orientation='horizontal')
        delete_layout.add_widget(Label(text='Sil ID:'))
        self.delete_id_input = TextInput()
        delete_layout.add_widget(self.delete_id_input)
        delete_button = Button(text='Sil')
        delete_button.bind(on_press=self.delete_data)
        delete_layout.add_widget(delete_button)
        layout.add_widget(delete_layout)

        sql_layout = BoxLayout(orientation='horizontal')
        sql_layout.add_widget(Label(text='SQL Sorgusu:'))
        self.sql_input = TextInput()
        sql_layout.add_widget(self.sql_input)
        sql_button = Button(text='Sorgula')
        sql_button.bind(on_press=self.execute_sql)
        sql_layout.add_widget(sql_button)
        layout.add_widget(sql_layout)

        self.show_all_data()

        return layout

    def show_all_data(self):
        self.table.clear_widgets()
        result = self.db_backend.get_all_data()
        self.display_result(result)

    def search_data(self, instance):
        user_id = self.query_input.text
        result = self.db_backend.get_user_data(user_id)
        self.display_result([result])

    def add_data(self, instance):
        name = self.add_name_input.text
        age = self.add_age_input.text
        result = self.db_backend.add_data(name, age)
        self.show_all_data()

    def update_data(self, instance):
        id = self.update_id_input.text
        new_name = self.update_name_input.text
        new_age = self.update_age_input.text
        result = self.db_backend.update_data(id, new_name, new_age)
        self.show_all_data()

    def delete_data(self, instance):
        id = self.delete_id_input.text
        result = self.db_backend.delete_data(id)
        self.show_all_data()

    def execute_sql(self, instance):
        query = self.sql_input.text
        result = self.db_backend.sql_query(query)
        self.display_result(result)

    def display_result(self, result):
        self.table.clear_widgets()
        if not result:
            self.table.add_widget(Label(text='Sonuç Bulunamadı'))
        else:
            for row in result:
                row_layout = BoxLayout(orientation='horizontal')
                for item in row:
                    row_layout.add_widget(Label(text=str(item)))
                self.table.add_widget(row_layout)

if __name__ == '__main__':
    AndroidApp().run()
    #insan yalnız doğarda yalnız ölmezmiş naber bizden uzak olsun keder
