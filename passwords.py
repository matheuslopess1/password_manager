from sqlite3 import connect, Connection, Cursor

MASTER_PASSWORD = 'TiXftTP0ady62T6fIX'


def menu() -> None:
    print(30 * '*')
    print('* i : inserir nova senha     *')
    print('* l : listar serviços salvos *')
    print('* r : recuperar uma senha    *')
    print('* s : sair                   *')
    print(30 * '*')


def get_password(cursor: Cursor, service: str) -> None:
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}';
    ''')
    if cursor.rowcount == 0:
        print('Serviço não cadastrado (use \'l\' para verificar os serviços).')
    else:
        for user in cursor.fetchall():
            print(user)


def insert_password(cursor: Cursor, conn: Connection, service: str, username: str, password: str) -> None:
    cursor.execute(f'''
        INSERT INTO users (service, username, password)
        VALUES ('{service}', '{username}', '{password}');
    ''')
    conn.commit()


def show_services(cursor: Cursor) -> None:
    cursor.execute('''
        SELECT service FROM users;
    ''')
    for service in cursor.fetchall():
        print(service)


def main() -> None:
    master_password = input('Informe a senha mestre: ')
    if master_password != MASTER_PASSWORD:
        print('Senha inválida! Encerrando...')
        exit()

    with connect('passwords.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')

        while True:
            menu()
            option = input('O que deseja fazer? ')
            if option not in ['i', 'l', 'r', 's']:
                print('Opção inválida!')
                continue
            if option == 's':
                break

            if option == 'i':
                service = input('Qual o nome do serviço? ')
                username = input('Qual o nome do usuário? ')
                password = input('Qual a senha? ')
                insert_password(cursor, conn, service, username, password)

            if option == 'l':
                show_services(cursor)

            if option == 'r':
                service = input('Qual o nome do serviço? ')
                get_password(cursor, service)


if __name__ == '__main__':
    main()
