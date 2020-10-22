from typing import Tuple
from configs import GlobalVariables


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