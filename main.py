from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *
import requests
from bannervenda import BannerVenda
import os
from functools import partial
from myFirebase import MyFirebase
from bannervendedor import BannerVendedor


GUI = Builder.load_file('main.kv')
class MainApp(App):

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self):
        # carregar as fotos de perfil (isso independe do usuário)
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos_perfil = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos_perfil.add_widget(imagem)
        # executa funções que dependem do usuário
        self.carregar_infos_usuario()

    def carregar_infos_usuario(self):
        try:
            #perpetuando login com refreshtoken
            with open("refreshtoken.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            # pegar informações do usuário
            requisicao = requests.get(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}.json")
            requisicao_dic = requisicao.json()

            # preencher foto de perfil
            avatar = requisicao_dic['avatar']
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher o ID único
            id_vendedor = requisicao_dic["id_vendedor"]
            pagina_config = self.root.ids["configpage"]
            pagina_config.ids["label_id_vendedor"].text = f"Seu ID Único: {id_vendedor}"

            # preencher o total de vendas
            total_vendas = requisicao_dic["total_vendas"]
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

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

            # preencher a equipe (vendedores que acompanha)
            equipe = requisicao_dic["equipe"]
            lista_equipe = equipe.split(",")

            pagina_lista_vendedores = self.root.ids["listagemvendedorespage"]
            lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)

            self.mudar_tela("homepage")
        except:
            pass

    def mudar_tela(self, id_tela):
        gerenciador_telas = self.root.ids["screen_manager"] #'self.root' faz referência ao arquivo main.kv
        gerenciador_telas.current = id_tela

    def mudar_foto_perfil(self, foto, *args): #por padrão on_release manda vários argumentos, por isso o *args
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        # realizando um update no banco de dados
        info = f'{{"avatar": "{foto}"}}' # passar dicionário formatado como texto
        requisicao = requests.patch(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}.json",
                                    data = info)
        # print(requisicao.json())
        self.mudar_tela("configpage")

MainApp().run()