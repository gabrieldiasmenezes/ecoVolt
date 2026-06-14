from service.residencial.dashboard import residential_dashboard
from service.residencial.charger import residential_charger_view
from service.residencial.session import residential_session
from service.residencial.schedule import schedule_service
from service.residencial.history import residential_history
from utils.system import load, reset_terminal
from utils.ui import error_option, header
from utils.validate.mutual_data import validate_option



def residencial_service(user):
    while True:
        reset_terminal()
        header('ÁREA DO CLIENTE RESIDENCIAL')
        print(f"\nOlá, {user['nome'].split()[0]}! Bem-vindo ao ChargeGrid Home.\n")

        options = validate_option("""
1 - Dashboard de Economia
2 - Meu Carregador
3 - Iniciar Recarga
4 - Encerrar Recarga
5 - Agendamento Inteligente
6 - Histórico de Consumo
0 - Sair

Opção: """)

        match options:
            case 1:
                load("Carregando dashboard de economia")
                residential_dashboard(user)
            case 2:
                load("Consultando carregador residencial")
                residential_charger_view(user)
            case 3:
                load("Iniciando recarga")
                residential_session(user, action='iniciar')
            case 4:
                load("Encerrando recarga")
                residential_session(user, action='encerrar')
            case 5:
                load("Abrindo agendamento inteligente")
                schedule_service(user)
            case 6:
                load("Carregando histórico de consumo")
                residential_history(user)
            case 0:
                load("Saindo")
                break
            case _:
                error_option()