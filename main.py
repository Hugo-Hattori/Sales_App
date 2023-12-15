from kivy.app import App
from kivy.lang import Builder


GUI = Builder.load_file('main.kv')


class MainApp(App):

    def build(self):
        return GUI


MainApp().run()