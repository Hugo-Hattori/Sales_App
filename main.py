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
from datetime import date


GUI = Builder.load_file('main.kv')
class MainApp(App):
    cliente = None
    produto = None
    unidade = None

    def build(self):
        self.firebase = MyFirebase()
        return GUI

    def on_start(self): # carregar infos que independe do usuário estar logado
        # carregar fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids["fotoperfilpage"]
        lista_fotos_perfil = pagina_fotoperfil.ids["lista_fotos_perfil"]
        for foto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil, foto))
            lista_fotos_perfil.add_widget(imagem)

        # carregar fotos dos clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]
        for foto_cliente in arquivos:
            imagem = ImageButton(source=f"icones/fotos_clientes/{foto_cliente}",
                                 on_release=partial(self.selecionar_cliente, foto_cliente))
            label = LabelButton(text=foto_cliente.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_cliente, foto_cliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)

        # carregar fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]
        for foto_produto in arquivos:
            imagem = ImageButton(source=f"icones/fotos_produtos/{foto_produto}",
                                 on_release=partial(self.selecionar_produto, foto_produto))
            label = LabelButton(text=foto_produto.replace(".png", "").capitalize(),
                                on_release=partial(self.selecionar_produto, foto_produto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)

        # carregar data
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        label_data = pagina_adicionar_vendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

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
            self.avatar = avatar
            foto_perfil = self.root.ids["foto_perfil"]
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # preencher o ID único
            id_vendedor = requisicao_dic["id_vendedor"]
            self.if_vendedor = id_vendedor
            pagina_config = self.root.ids["configpage"]
            pagina_config.ids["label_id_vendedor"].text = f"Seu ID Único: {id_vendedor}"

            # preencher o total de vendas
            total_vendas = requisicao_dic["total_vendas"]
            self.total_vendas = total_vendas
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

            # preencher lista de vendas
            try:
                vendas = requisicao_dic['vendas']
                self.vendas = vendas
                pagina_homepage = self.root.ids["homepage"]
                lista_vendas = pagina_homepage.ids["lista_vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    banner = BannerVenda(cliente=venda['cliente'], foto_cliente=venda['foto_cliente'],
                                         produto=venda['produto'], foto_produto=venda['foto_produto'],
                                         preco=venda['preco'], data=venda['data'], unidade=venda['unidade'],
                                         quantidade=venda['quantidade'])
                    lista_vendas.add_widget(banner)  #adicionar um item na lista de vendas
            except Exception as erro:
                print(erro)

            # preencher a equipe (vendedores que acompanha)
            equipe = requisicao_dic["equipe"]
            self.equipe = equipe
            lista_equipe = equipe.split(",")

            pagina_lista_vendedores = self.root.ids["listagemvendedorespage"]
            lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]

            # preenchendo os banneres de acordo com as infos da equipe deste usuário
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
        self.mudar_tela("configpage")

    def adicionar_vendedor(self, id_vendedor_add):
        link = f'https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_add}"'
        requisicao = requests.get(link)
        requisicao_dic = requisicao.json()

        pagina_add_vendedor = self.root.ids["adicionarvendedorpage"]
        mensagem_aviso = pagina_add_vendedor.ids["mensagem_adicionar_vendedor"]

        if requisicao_dic == {}:
            mensagem_aviso.text = "Usuário não encontrado"
        else:
            equipe = self.equipe.split(',')
            if id_vendedor_add in equipe:
                mensagem_aviso.text = "Vendedor já faz parte da equipe"
            else:
                self.equipe = self.equipe + f",{id_vendedor_add}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requests.patch(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}.json",
                               data=info)
                mensagem_aviso.text = "Vendedor adicionado com sucesso!"

                #adicionar um novo banner na lista de vendedores
                pagina_lista_vendedores = self.root.ids["listagemvendedorespage"]
                lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]
                banner_vendedor = BannerVendedor(id_vendedor=id_vendedor_add)
                lista_vendedores.add_widget(banner_vendedor)

    def selecionar_cliente(self, foto, *args):
        self.cliente = foto.replace(".png", "")
        # pintar de branco todos os outros itens
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]
        pagina_adicionar_vendas.ids["label_selecionar_cliente"].color = (1, 1, 1, 1)

        for item in list(lista_clientes.children): #pegando todos os widgets dentro do item de id lista_clientes
            item.color = (1, 1, 1, 1) #pintando de branco
            # pintar de azul o texto do item selecionado
            # foto -> carrefour.png / Label -> Carrefour -> carrefour.png
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_produto(self, foto, *args):
        self.produto = foto.replace(".png", "")
        # pintar de branco todos os outros itens
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]
        pagina_adicionar_vendas.ids["label_selecionar_produto"].color = (1, 1, 1, 1)

        for item in list(lista_produtos.children): #pegando todos os widgets dentro do item de id lista_clientes
            item.color = (1, 1, 1, 1) #pintando de branco
            # pintar de azul o texto do item selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255, 1)
            except:
                pass

    def selecionar_unidade(self, id_label, *args):
        self.unidade = id_label.replace("unidades_", "")
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]

        # pintar de branco todos os outros itens
        pagina_adicionar_vendas.ids["unidades_kg"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidades_unidades"].color = (1, 1, 1, 1)
        pagina_adicionar_vendas.ids["unidades_litro"].color = (1, 1, 1, 1)

        # pintar de azul o texto do item selecionado
        pagina_adicionar_vendas.ids[id_label].color = (0, 207/255, 219/255, 1)

    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade
        pagina_adicionar_vendas = self.root.ids["adicionarvendaspage"]
        data = pagina_adicionar_vendas.ids["label_data"].text.replace("Data: ", "")
        preco = pagina_adicionar_vendas.ids["preco_total"].text
        quantidade = pagina_adicionar_vendas.ids["quantidade"].text

        # destaca de vermelho caso o campo não esteja selecionado
        if not cliente:
            pagina_adicionar_vendas.ids["label_selecionar_cliente"].color = (1, 0, 0, 1)
        if not produto:
            pagina_adicionar_vendas.ids["label_selecionar_produto"].color = (1, 0, 0, 1)
        if not unidade:
            pagina_adicionar_vendas.ids["unidades_kg"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidades_unidades"].color = (1, 0, 0, 1)
            pagina_adicionar_vendas.ids["unidades_litro"].color = (1, 0, 0, 1)
        if not preco:
            pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionar_vendas.ids["label_preco"].color = (1, 0, 0, 1)
        if not quantidade:
            pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionar_vendas.ids["label_quantidade"].color = (1, 0, 0, 1)

        # dado que o usuário preencheu tudo
        if cliente and produto and unidade and (type(quantidade)) == float and (type(preco)) == float:
            preco = preco*quantidade
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png"

            # adicionar a venda no BD
            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}",' \
                   f' "foto_produto": "{foto_produto}","data": "{data}", "unidade": "{unidade}",' \
                   f' "preco": "{preco}", "quantidade": "{quantidade}"}}'
            requests.post(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}/vendas.json",
                          data=info)

            # criar o banner na instância atual do usuário logado
            banner = BannerVenda(cliente=cliente, produto=produto, foto_cliente=foto_cliente, foto_produto=foto_produto,
                                 data=data, preco=preco, quantidade=quantidade, unidade=unidade)
            pagina_homepage = self.root.ids["homepage"]
            lista_vendas = pagina_homepage.ids["lista_vendas"]
            lista_vendas.add_widget(banner)

            # atualizar o valor de total de vendas
            requisicao = requests.get(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}"
                                      f"/total_vendas.json")
            total_vendas = float(requisicao.json())
            total_vendas += preco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{self.local_id}.json",
                           data=info)

            # atualizar o label de total de vendas
            homepage = self.root.ids["homepage"]
            homepage.ids["label_total_vendas"].text = f"[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

            self.mudar_tela("homepage")

        # resetando parâmetros
        self.cliente = None
        self.produto = None
        self.unidade = None

        # pintar de branco todos os itens de branco
        lista_clientes = pagina_adicionar_vendas.ids["lista_clientes"]
        lista_produtos = pagina_adicionar_vendas.ids["lista_produtos"]
        for itens1, itens2 in zip(lista_clientes.children, lista_produtos.children):
            itens1.color = (1, 1, 1, 1)
            itens2.color = (1, 1, 1, 1)

    def carregar_todas_vendas(self):
        pagina_todas_vendas = self.root.ids["todasvendaspage"]
        lista_vendas = pagina_todas_vendas.ids["lista_vendas"]

        # revomendo itens duplicados
        for item in list(lista_vendas.children):
            lista_vendas.remove_widget(item)

        # preencher a página todasvendaspage.kv
        # pegar informações da empresa
        requisicao = requests.get(
            f'https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"')
        requisicao_dic = requisicao.json()

        # preencher foto de perfil da empresa
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = "icones/fotos_perfil/hash.png"

        # preencher total de vendas da empresa
        total_vendas = 0
        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]["vendas"]
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    total_vendas += float(venda["preco"]) #adicionando o valor da venda no total
                    banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"],
                                         foto_cliente=venda["foto_cliente"],foto_produto=venda["foto_produto"],
                                         data=venda["data"], preco=venda["preco"], quantidade=venda["quantidade"],
                                         unidade=venda["unidade"])
                    lista_vendas.add_widget(banner)
            except:
                pass

        # preencher o total de vendas
        pagina_todas_vendas.ids["label_total_vendas"].text =\
            f"[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

        # redirecionar para a página todasvendaspage.kv
        self.mudar_tela("todasvendaspage")

    def sair_todas_vendas(self):
        # retorna a foto de perfil do usuário
        foto_perfil = self.root.ids["foto_perfil"]
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"
        # volta para configpage
        self.mudar_tela("configpage")

    def carregar_outro_vendedor(self, dic_info_vendedor, *args):
        total_vendas = dic_info_vendedor["total_vendas"]
        pagina_vendas_outro_vendedor = self.root.ids["vendasoutrovendedorpage"]
        lista_vendas = pagina_vendas_outro_vendedor.ids["lista_vendas"]

        try:
            vendas = dic_info_vendedor["vendas"]
            for id_venda in vendas:
                venda = vendas[id_venda]
                banner = BannerVenda(cliente=venda["cliente"], produto=venda["produto"],
                                     foto_cliente=venda["foto_cliente"],foto_produto=venda["foto_produto"],
                                     data=venda["data"], preco=venda["preco"], quantidade=venda["quantidade"],
                                     unidade=venda["unidade"])
                lista_vendas.add_widget(banner)
        except:
            pass

        # preencher o total de vendas
        pagina_vendas_outro_vendedor.ids["label_total_vendas"].text = \
            f"[color=#000000<color>]Total de Vendas:[/color] [b]R${total_vendas}[/b]"

        # preencher foto de perfil do outro usuário
        foto_perfil = self.root.ids["foto_perfil"]
        avatar = dic_info_vendedor["avatar"]
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        self.mudar_tela("vendasoutrovendedorpage")


MainApp().run()