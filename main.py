from kivy.lang import Builder
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
import requests
from kivy.utils import platform
import json

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

selected_item = []
class myApp(MDApp):
    auth_key = 'CHAVE DO FIREBASE'
    firebase_url = "URL DO BANCO"

    def build(self):
        self.theme_cls.primary_palette='Green'
        self.theme_cls.theme_style="Dark"
        return Builder.load_file("my.kv")

    def dados(self):
        try:
            res = requests.get(f'{self.firebase_url}/login/.json' + '?auth=' + self.auth_key)
            dic_login = res.json()
            try:

                lgemail = self.root.ids.email.text
                lgsenha = self.root.ids.senha.text

                for id_venda in dic_login:
                    vendedor = dic_login[id_venda]['email']
                    if lgemail == "" and lgsenha == "":
                        Snackbar(
                            text="Preencha os campos!",
                            snackbar_x="25dp",
                            snackbar_y="50dp",
                            size_hint_x=.9).open()
                    else:
                        lgsenha=int(lgsenha)

                        if lgemail in vendedor and lgsenha == dic_login[id_venda]['senha']:
                            idvendedora = dic_login[id_venda]['senha']
                            self.root.current = 'second'
                            self.root.ids.Vendedora.text= f"Vendedora: {dic_login[id_venda]['vendedora']}"
                            self.root.ids.Vendas.text = str(f"Vendas: {dic_login[id_venda]['vendas']}")


                        else:

                            Snackbar(
                                text="Senha incorreta, tente novamente!",
                                snackbar_x="25dp",
                                snackbar_y="50dp" ,
                                size_hint_x=.9  ).open()
            except:
                Snackbar(
                    text="Ops, houve erros internos!",
                    snackbar_x="25dp",
                    snackbar_y="50dp",
                    size_hint_x=.9).open()
        except:
            Snackbar(
                text="Não foi possivel consultar o banco de dados.",
                snackbar_x="25dp",
                snackbar_y="50dp",
                size_hint_x=.9).open()


    def voltar(self):
        self.root.current = 'second'

    def cadastro(self):
        self.root.current='cadastro'


    def cadastrar(self):

        try:
            if self.root.ids.cpf.text == "" and self.root.ids.nome.text == "":
                Snackbar(
                    text="Preencha os campos!",
                    snackbar_x="25dp",
                    snackbar_y="50dp",
                    size_hint_x=.9).open()
            else:
                dados = {'cpf': self.root.ids.cpf.text,'formapg':selected_item, 'nome': self.root.ids.nome.text}
                requisicao = requests.post(f'{self.firebase_url}/Cadastro/.json', data=json.dumps(dados))
        except:
            Snackbar(
                text="Não foi possivel salvar dados, tente novamente mais tarde!",
                snackbar_x="25dp",
                snackbar_y="50dp",
                size_hint_x=.9).open()


    def save_checked(self, checkbox,value, a):
        global selected_item
        if value == True:
            selected_item.append(a)

        else:
            selected_item.clear()



myApp().run()