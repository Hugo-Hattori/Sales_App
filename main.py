from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os


GUI = Builder.load_file('main.kv')
class MainApp(App):

    id_usuario = 1

    def build(self):
        return GUI

    def on_start(self):
        # carregar as fotos de perfil (isso independe do usuário)
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos_perfil = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=self.mudar_foto_perfil)
            lista_fotos_perfil.add_widget(imagem)
        # executa funções que dependem do usuário
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
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
            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            for venda in vendas:
                banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                     produto=venda['produto'], foto_produto=venda['foto_produto'],
                                     preco=venda['preco'], data=venda['data'], unidade=venda['unidade'],
                                     quantidade=venda['quantidade'])
                lista_vendas.add_widget(banner)  #adicionar um item na lista de vendas
        except:
            pass

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"] #'self.root' faz referência ao arquivo main.kv
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, *args): #por padrão on_release manda vários argumentos, por isso o *args
        print("Mudar foto perfil")

MainApp().run()