
import auth.sign_up.get_data_user as sg
from utils.system import load, reset_terminal
from utils.ui import enter, header
from database.database import users,residencial_charger


def signUp():
    reset_terminal()
    header("CRIAR CONTA")

    type_account = sg.get_type_account()
    if type_account ==0:
        return

    user = sg.get_commom_data()
    user["id"] = max(u["id"] for u in users) + 1
    user["perfil"] = type_account

    if type_account == "dono_estabelecimento":
        sg.get_establishment_data(user)
    if type_account == 'cliente_residencial':
        load('Adicionando ao banco o seu carregador')
        residencial_charger.append(sg.create_residential_charger(user['id']))

    users.append(user)
    load("Processando todos os dados")

    print("\nConta criada com sucesso!")
    print(f'Bem-vindo, {user["nome"]}!')
    enter()
    return user