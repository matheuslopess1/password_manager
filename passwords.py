from sqlite3 import connect, Connection, Cursor
from typing import Tuple, Dict


class SQLiteHelper:
    def __init__(self, database: str) -> None:
        self.__connection = connect(database)
        self.__cursor = self.__connection.cursor()

    def disconnect(self):
        self.__connection.close()

    @property
    def conenction(self) -> Connection:
        return self.__connection

    @property
    def cursor(self) -> Cursor:
        return self.__cursor


class GlobalVariables:
    MASTER_PASSWORD = 'TiXftTP0ady62T6fIX'
    DATABASE = SQLiteHelper('passwords.db')


class AccountModel:
    def __init__(self, service: str, username: str, password: str) -> None:
        self.__service = service
        self.__username = username
        self.__password = password

    @property
    def service(self) -> str:
        return self.__service

    @property
    def username(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    def insert(self) -> None:
        GlobalVariables.DATABASE.cursor.execute(
            'INSERT INTO accounts VALUES (?, ?, ?)',
            [self.__service, self.__username, self.__password]
        )
        GlobalVariables.DATABASE.conenction.commit()

    @staticmethod
    def sync() -> None:
        cursor = GlobalVariables.DATABASE.cursor
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')

    @staticmethod
    def list_by_service(service: str) -> Tuple['AccountModel']:
        cursor = GlobalVariables.DATABASE.cursor
        cursor.execute('SELECT * FROM accounts WHERE service = ?;', [service])
        return tuple(AccountModel(s, u, p) for s, u, p in cursor.fetchall())

    @staticmethod
    def list_all() -> Tuple['AccountModel']:
        cursor = GlobalVariables.DATABASE.cursor
        cursor.execute('SELECT * FROM accounts;')
        return tuple(AccountModel(s, u, p) for s, u, p in cursor.fetchall())


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


class Passwords:
    @staticmethod
    def main() -> None:
        LoginView().render()


if __name__ == '__main__':
    Passwords.main()
