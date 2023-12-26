import requests
from kivy.app import App


class MyFirebase():
    API_KEY = "AIzaSyCWEPGNX1040n4JcK-OIZK8lVG9WRoQ0lg"

    def criar_conta(self, email, senha):
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"
        print(email, senha)
        info = {"email": email,
                "password": senha,
                "returnSecureToken": True}
        requisicao = requests.post(link, data=info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print("Usuário Criado")
            # requisicao_dic["idToken"] -> autenticação
            # requisicao_dic["refreshToken"] -> token que mantém o usuário logado
            # requisicao_dic["localId"] -> id do usuário
            refresh_token = requisicao_dic["refreshToken"]
            local_id = requisicao_dic["localId"]
            id_token = requisicao_dic["idToken"]

            meu_aplicativo = App.get_running_app()  # retorna a classe MainApp
            #salvando atributos no MainApp
            meu_aplicativo.local_id = local_id
            meu_aplicativo.id_token = id_token

            # o refresh_token é uma variável que devemos perpetuar msm depois do app ser fechado
            with open("refreshtoken.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            link = f"https://aplicativovendashash-76c33-default-rtdb.firebaseio.com/{local_id}.json"
            # dicionário com infos padrão de um usuário recém criado
            info_usuario = '{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": ""}'
            requisicao_usuario = requests.patch(link, data=info_usuario)
            meu_aplicativo.carregar_infos_usuario()
            meu_aplicativo.mudar_tela("homepage")
        else:
            mensagem_erro = requisicao_dic["error"]["message"]
            meu_aplicativo = App.get_running_app() #retorna a classe MainApp
            pagina_login = meu_aplicativo.root.ids["loginpage"]
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)
        print(requisicao_dic)

    def fazer_login(self, email, senha):
        pass