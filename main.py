from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class HomePage(Screen):
    pass


GUI = Builder.load_file('main.kv')
class MainApp(App):

    def build(self):
        return GUI


MainApp().run()