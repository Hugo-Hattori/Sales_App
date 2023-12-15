from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


GUI = Builder.load_file('main.kv')


class Homepage(Screen):
    pass


class MainApp(App):

    def build(self):
        return GUI


MainApp().run()