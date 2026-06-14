from datetime import datetime
from utils.system import load, reset_terminal
from utils.ui import enter, error_option, header
import utils.validate.mutual_data as mu
import utils.validate.company_data as co
from database.database import users, establishments, establishment_chargers
from service.total_charger import get_total_chargers


def about_account_type():
    return """
CLIENTE COMERCIAL
• Localizar estações
• Iniciar recargas
• Acompanhar sessões
• Consultar custos

CLIENTE RESIDENCIAL
• Gerenciar carregador residencial
• Consultar histórico
• Simular economia de energia

DONO DE ESTABELECIMENTO
• Monitorar carregadores
• Visualizar faturamento
• Gerenciar demanda energética
• Acompanhar sessões ativas

ADMINISTRADOR GOODWE
• Perfil interno da plataforma
• Não disponível para cadastro
========================================
"""


def get_type_account():
    while True:
        reset_terminal()
        option = mu.validate_option("""
Escolha o perfil desejado:

1 - Cliente Comercial
2 - Cliente Residencial
3 - Dono de Estabelecimento
4 - Conhecer os perfis
0 - Voltar

Opção: """)

        match option:
            case 1:
                return "cliente_comercial"
            case 2:
                return "cliente_residencial"
            case 3:
                return "dono_estabelecimento"
            case 4:
                header("TIPOS DE PERFIL")
                print(about_account_type())
                enter()
            case 0:
                load('Voltando a tela inicial')
                return 0
            case _:
                error_option()


def get_mutual_info():
    while True:
        name = input("Nome completo: ")
        if mu.validate_name(name):
            break

    while True:
        email = input("Email: ")
        if mu.validate_email(email):
            break

    while True:
        phone = input("Telefone: ")
        if mu.validade_telephone(phone):
            break

    while True:
        password = input("Senha: ")
        if mu.validate_password(password):
            break

    while True:
        city = input("Cidade: ")
        if mu.validate_city(city):
            break

    return {
        "nome": name,
        "email": email,
        "telefone": phone,
        "senha": password,
        "cidade": city,
        "status": "ativo",
        "data_cadastro": str(datetime.now().date()),
        "total_recargas": 0,
        "energia_consumida_kwh": 0
    }


def register_charger(est_id, power,number):
    return {
        "id": len(establishment_chargers) + 1,
        "estabelecimento_id": est_id,
        'numero':number,
        "modelo": "GoodWe GW-11kW",
        "status": "livre",
        "potencia_maxima": power,
        "potencia_atual": 0,
        "total_sessoes": 0,
        "energia_fornecida_kwh": 0
    }


def get_establishment_data(owner_id, company_name):
    header("ESTABELECIMENTO")

    while True:
        name = input("Nome do estabelecimento: ")
        if mu.validate_name(name):
            break

    while True:
        address = input("Endereço: ")
        if co.validate_address(address):
            break

    while True:
        solar = input("Usa energia solar? (S/N): ").upper()
        if solar in ["S", "N"]:
            solar = True if solar == "S" else False
            break

    demanda, total_chargers = get_total_chargers()

    est_id = len(establishments) + 1

    new_est = {
        "id": est_id,
        "id_dono": owner_id,
        "nome": name,
        "endereco": address,
        "empresa_responsavel": company_name,
        "demanda_maxima_kw": demanda,
        "potencia_em_uso_kw": 0,
        "energia_total_distribuida_kwh": 0,
        "faturamento": 0,
        "status": "ativo",
        "possui_energia_solar": solar,
        "carregadores_disponiveis": total_chargers
    }

    establishments.append(new_est)

    for i in range(total_chargers):
        establishment_chargers.append(
            register_charger(est_id, 11,i)
        )

    return new_est


def signUp():
    reset_terminal()
    header("CRIAR CONTA")

    type_account = get_type_account()
    if type_account ==0:
        return

    user_id = max(u["id"] for u in users) + 1

    user = get_mutual_info()
    user["id"] = user_id
    user["perfil"] = type_account

    if type_account == "dono_estabelecimento":

        while True:
            company = input("Nome da empresa: ")
            if co.validate_company_name(company):
                break

        while True:
            cnpj = input("CNPJ: ")
            if co.validate_cnpj(cnpj):
                break

        user["empresa"] = company
        user["cnpj"] = cnpj

        get_establishment_data(user_id, company)

    users.append(user)
    load("Processando todos os dados")

    print("\nConta criada com sucesso!")
    print(f'Bem-vindo, {user["nome"]}!')
    enter()
    return user