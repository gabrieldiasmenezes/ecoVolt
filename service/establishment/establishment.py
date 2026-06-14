from service.establishment.charger import chargers_service
from service.establishment.dashboard import most_operational_dashboard
from service.establishment.dataEstablishment import get_data_establishment
from service.establishment.demand_control import demand_control
from service.establishment.ocpp_integration import ocpp_integration
from service.establishment.pricing_service import pricing_service
from service.establishment.reports import reports
from service.sessions.rechard_session import rechard_sessions
from utils.system import load, reset_terminal
from utils.ui import error_option, header
from utils.validate.mutual_data import validate_option


def establishment_service(id):
    data = get_data_establishment(id)
    while True:
        reset_terminal()
        header('PAINEL DO ESTABELECIMENTO')
        options = validate_option("""
1 - Dashboard Operacional
2 - Sessões de Recarga
3 - Carregadores
4 - Controle de Demanda
5 - Tarifação
6 - Integração OCPP
7 - Relatórios
0 - Sair

Opção: """)

        match options:
            case 1:
                load("Carregando dashboard operacional")
                most_operational_dashboard(data['establishment'], data['chargers'], data['sessions'])
            case 2:
                load("Buscando sessões de recarga")
                rechard_sessions(data['sessions'])
            case 3:
                load("Consultando carregadores")
                chargers_service(data['chargers'])
            case 4:
                load("Analisando controle de demanda")
                demand_control(data['establishment'], data['chargers'])
            case 5:
                load("Calculando tarifação")
                pricing_service(data['sessions'])
            case 6:
                load("Conectando ao gateway OCPP")
                ocpp_integration(data['sessions'])
            case 7:
                load("Gerando relatórios")
                reports(data['establishment'], data['sessions'])
            case 0:
                load('Voltando à página principal')
                break
            case _:
                error_option()
                continue