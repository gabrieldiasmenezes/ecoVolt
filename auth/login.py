from database.database import users
from utils.system import load, reset_terminal
from utils.ui import enter

def login():
    load('inicializando login')
    while True:
        reset_terminal()
        try:
            email = input("Digite seu Email: ")
            password = input("Digite sua senha: ")
            autenticado = False

            for user in users:
                if user["email"] == email.strip() and user["senha"] == password.strip():
                    print(f'Bem-vindo, {user["nome"]}!')
                    autenticado = True
                    userInfo=user
                    break

            if autenticado:
                break
            else:
                print('Email e/ou senha incorretos! Tente novamente.')
                enter()

        except Exception as e:
            print("Erro no sistema!!", e)
            continue
    return userInfo