
from modules.residential.features.charger import residential_charger_view
from modules.residential.features.dashboard import residential_dashboard
from modules.residential.features.history import residential_history
from modules.residential.features.schedule import schedule_service
from modules.sessions.residential_session import residential_session
from modules.vehicles.vehicle_meneger import vehicle_manager
from utils.system import load, reset_terminal
from utils.ui import error_option, header
from utils.validation.common_validation import validate_int_value


MENU="""
1 - Dashboard de Economia
2 - Meu Veículo
3 - Meu Carregador
4 - Iniciar Recarga
5 - Encerrar Recarga
6 - Agendamento Inteligente
7 - Histórico de Consumo
0 - Sair

Opção: """
def residencial_service(user):
    while True:
        reset_terminal()
        header('ÁREA DO CLIENTE RESIDENCIAL')
        print(f"\nOlá, {user['nome'].split()[0]}! Bem-vindo ao ChargeGrid Home.\n")

        options = validate_int_value(MENU)

        match options:
            case 1:
                load("Carregando dashboard de economia")
                residential_dashboard(user)
            case 2:
                load("Consultando carregador residencial")
                vehicle_manager(user)
            case 3:
                load("Consultando carregador residencial")
                residential_charger_view(user)
            case 4:
                load("Iniciando recarga")
                residential_session(user, action='iniciar')
            case 5:
                load("Encerrando recarga")
                residential_session(user, action='encerrar')
            case 6:
                load("Abrindo agendamento inteligente")
                schedule_service(user)
            case 7:
                load("Carregando histórico de consumo")
                residential_history(user)
            case 0:
                load("Saindo")
                break
            case _:
                error_option()