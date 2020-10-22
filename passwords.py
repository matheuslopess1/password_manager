from views import LoginView


class Passwords:
    @staticmethod
    def main() -> None:
        LoginView().render()


if __name__ == '__main__':
    Passwords.main()
