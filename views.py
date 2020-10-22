from typing import Dict
from configs import GlobalVariables
from models import AccountModel


class View:
    def render(self) -> None:
        raise NotImplementedError()


class InvalidOptionView(View):
    def render(self) -> None:
        print('Opção inválida!')


class InsertAccountView(View):
    def render(self) -> None:
        service = input('Qual o nome do serviço? ')
        username = input('Qual o nome do usuário? ')
        password = input('Qual a senha? ')
        AccountModel(service, username, password).insert()


class ListAccountServicesView(View):
    def render(self) -> None:
        services = tuple(account.service for account in AccountModel.list_all())
        print(services)


class ListAccountsByServiceView(View):
    def render(self) -> None:
        service = input('Qual o nome do serviço? ')
        accounts = AccountModel.list_by_service(service)
        print(tuple((a.username, a.password) for a in accounts))


class MenuView(View):
    def __init__(self):
        AccountModel.sync()
        self.__options: Dict[str, View] = {
            'i': InsertAccountView(),
            'l': ListAccountServicesView(),
            'r': ListAccountsByServiceView()
        }

    def render(self) -> None:
        while True:
            print(30 * '*')
            print('* i : inserir nova senha     *')
            print('* l : listar serviços salvos *')
            print('* r : recuperar uma senha    *')
            print('* s : sair                   *')
            print(30 * '*')
            option = input('O que deseja fazer? ')
            if option in self.__options:
                self.__options[option].render()
            elif option == 's':
                break
            else:
                InvalidOptionView().render()


class LoginView(View):
    def render(self) -> None:
        master_password = input('Informe a senha mestre: ')
        if master_password != GlobalVariables.MASTER_PASSWORD:
            print('Senha inválida! Encerrando...')
            exit()
        else:
            MenuView().render()
