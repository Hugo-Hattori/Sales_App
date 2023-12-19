from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests


GUI = Builder.load_file('main.kv')
class MainApp(App):

    id_usuario = 1

    def build(self):
        return GUI

    def on_start(self):
        # pegar informações do usuário
        requisicao = requests.get(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.id_usuario}.json")
        requisicao_dic = requisicao.json()

        # preencher foto de perfil
        avatar = requisicao_dic['avatar']
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        # preencher lista de vendas
        try:
            print(requisicao_dic['vendas'])
            vendas = requisicao_dic['vendas'][1:]
            for venda in vendas:
                print(venda)
        except:
            pass


    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"] #'self.root' faz referência ao arquivo main.kv
        gerenciador_telas.current = id_tela


MainApp().run()