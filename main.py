from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


class HomePage(Screen):
    pass


class ConfigPage(Screen):
    pass


GUI = Builder.load_file('main.kv')
class MainApp(App):

    def build(self):
        return GUI

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"] #'self.root' faz referência ao arquivo main.kv
        gerenciador_telas.current = id_tela


MainApp().run()