from sqlite3 import connect, Connection, Cursor


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
