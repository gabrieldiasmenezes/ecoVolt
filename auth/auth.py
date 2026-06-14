from auth.login import login
from auth.signUp import signUp
from utils.system import load,reset_terminal
from utils.ui import error_option, header
from utils.validate.mutual_data import validate_option



def auth():
    reset_terminal()

    while True:
        header("ÁREA DE AUTENTICAÇÃO")

        option = validate_option("""
1 - Login
2 - Cadastro
0 - Encerrar Sistema

Opção: """)

        if option == 1:
            user = login()
            if user:
                return user

        elif option == 2:
            user = signUp()
            if user:
                return user

        elif option == 0:
            load("Encerrando sistema")
            return None

        else:
            error_option()
