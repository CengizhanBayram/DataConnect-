from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty
from DataConnect import DataConnect

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.db_backend = DataConnect('example.db')
        self.data = []

    def show_all_data(self):
        result = self.db_backend.get_all_data()
        self.data = [{'text': str(item)} for item in result]

    def search_data(self, name):
        result = self.db_backend.get_user_data(name)
        self.data = [{'text': str(result)}]

    def add_data(self, name, age):
        result = self.db_backend.add_data(name, age)
        self.show_all_data()

class DBBrowser(App):
    def build(self):
        self.title = 'SQLite DB Tarayıcı'
        root = BoxLayout(orientation='vertical')

        self.result_label = Label(text='')
        root.add_widget(self.result_label)

        self.query_input = TextInput(hint_text='Veri Arama:')
        root.add_widget(self.query_input)

        search_button = Button(text='Ara')
        search_button.bind(on_press=self.search_data)
        root.add_widget(search_button)

        self.rv = RV()
        self.rv.show_all_data()
        root.add_widget(self.rv)

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
        root.add_widget(add_layout)

        return root

    def search_data(self, instance):
        name = self.query_input.text
        self.rv.search_data(name)

    def add_data(self, instance):
        name = self.add_name_input.text
        age = self.add_age_input.text
        self.rv.add_data(name, age)

if __name__ == '__main__':
    DBBrowser().run()
