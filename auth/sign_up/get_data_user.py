
from datetime import datetime
import database.database as db
from auth.sign_up.account_type_description import about_account_type
from database.settings import RESIDENTIAL_POWER,ESTABLISHMENT_POWER


from modules.establishment.features.total_chargers import get_total_chargers
from utils.ui import enter, error_option, header
from utils.system import reset_terminal,load
import utils.validation.common_validation as commv
import utils.validation.company_validation as comp

def get_type_account():
    while True:
        reset_terminal()
        option = commv.validate_int_value("""
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
                reset_terminal()
                return 0
            case _:
                error_option()


def get_commom_data():
    return {
        "nome": commv.get_valid_input('Nome Completo: ',commv.validate_name),
        "email": commv.get_valid_input('Email:: ',commv.validate_email),
        "telefone": commv.get_valid_input('Telefone: ',commv.validate_telephone),
        "senha": commv.get_valid_input('Senha: ',commv.validate_password),
        "cidade": commv.get_valid_input('Cidade: ',commv.validate_city),
        "status": "ativo",
        "data_cadastro": str(datetime.now().date()),
        "total_recargas": 0,
        "energia_consumida_kwh": 0
    }


def create_establishment_charger(establishment_id, number):
    return {
        "id": len(db.establishment_chargers) + 1,
        "estabelecimento_id": establishment_id,
        "numero": number,
        "modelo": "GoodWe GW-11kW",
        "status": "livre",
        "potencia_maxima": ESTABLISHMENT_POWER,
        "potencia_atual": 0,
        "total_sessoes": 0,
        "energia_fornecida_kwh": 0
    }


def create_residential_charger(user_id):
    return {
        "id": len(db.residencial_charger) + 1,
        "usuario_id": user_id,
        "modelo": "GoodWe Home 7kW",
        "status": "livre",
        "potencia_maxima": RESIDENTIAL_POWER,
        "potencia_atual": 0,
        "total_sessoes": 0,
        "energia_fornecida_kwh": 0
    }


def get_establishment_data(user):
    header("ESTABELECIMENTO")
    company=commv.get_valid_input('Nome do Estabelecimento: ',comp.validate_company_name)
    address=commv.get_valid_input('Endereço: ',comp.validate_address)
    user["empresa"] = company
    user["cnpj"] = commv.get_valid_input('CNPJ: ',comp.validate_cnpj)

    while True:
        solar = input("Usa energia solar? (S/N): ").upper()
        if solar in ["S", "N"]:
            solar = True if solar == "S" else False
            break
        else:
            print('[ERRO] Digite "S" ou "N" ')


    demanda, total_chargers = get_total_chargers()

    est_id = len(db.establishments) + 1

    new_est = {
        "id": est_id,
        "id_dono":user['id'],
        "nome": company,
        "endereco": address,
        "empresa_responsavel": user['nome'],
        "demanda_maxima_kw": demanda,
        "potencia_em_uso_kw": 0,
        "energia_total_distribuida_kwh": 0,
        "faturamento": 0,
        "status": "ativo",
        "possui_energia_solar": solar,
        "carregadores_disponiveis": total_chargers
    }

    db.establishments.append(new_est)

    for i in range(total_chargers):
        db.establishment_chargers.append(
            create_establishment_charger(est_id,i)
        )

    return new_est