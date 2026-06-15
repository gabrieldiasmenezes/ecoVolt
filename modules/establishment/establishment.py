from modules.establishment.features.chargers import chargers_service
from modules.establishment.features.dashboard import operational_dashboard
from modules.establishment.features.demand_control import demand_control
from modules.establishment.features.ocpp import ocpp_integration
from modules.establishment.features.pricing import pricing_service
from modules.establishment.features.reports import reports
from modules.sessions.rechard_sessions import rechard_sessions
from utils.helpers import get_establishment_data_by_id
from utils.system import load, reset_terminal
from utils.ui import enter, error_option, header
from utils.validation.common_validation import validate_int_value

MENU="""
1 - Dashboard Operacional
2 - Sessões de Recarga
3 - Carregadores
4 - Controle de Demanda
5 - Tarifação
6 - Integração OCPP
7 - Relatórios
0 - Sair

Opção: """

def establishment_service(id):
    data = get_establishment_data_by_id(id)
    while True:
        reset_terminal()
        header('PAINEL DO ESTABELECIMENTO')
        options = validate_int_value(MENU)

        match options:

            case 1:
                load("Carregando dashboard operacional")
                reset_terminal()
                operational_dashboard(
                    data['establishment'],
                    data['chargers'],
                    data['sessions']
                )
                enter()
            case 2:
                load("Buscando sessões de recarga")
                rechard_sessions(data['sessions'])
                enter()
            case 3:
                load("Consultando carregadores")
                chargers_service(data['chargers'])
                enter()
            case 4:
                load("Analisando controle de demanda")
                demand_control(data['establishment'],data['chargers'])
            case 5:
                load("Calculando tarifação")
                pricing_service(data['sessions'])
            case 6:
                load("Conectando ao gateway OCPP")
                ocpp_integration(data['sessions'])
            case 7:
                load("Gerando relatórios")
                reports(data['establishment'],data['sessions'])
            case 0:
                load('Voltando à página principal')
                break
            case _:
                error_option()
