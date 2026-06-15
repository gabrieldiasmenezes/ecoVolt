

from modules.comercial.feature.establishments import find_establishments
from modules.comercial.feature.history import session_history
from modules.sessions.session_menager import session_manager
from modules.vehicles.vehicle_meneger import vehicle_manager
from utils.system import load, reset_terminal
from utils.ui import error_option, header
from utils.validation.common_validation import validate_int_value



def comercial_service(user):
    while True:
        reset_terminal()
        header('ÁREA DO CLIENTE')

        print(f"\nOlá, {user['nome'].split()[0]}! Bem-vindo ao ChargeGrid.\n")

        options = validate_int_value("""
1 - Localizar Estabelecimentos
2 - Meu Veículo
3 - Iniciar Recarga
4 - Encerrar Recarga
5 - Histórico de Sessões
0 - Sair

Opção: """)

        match options:
            case 1:
                load("Buscando estabelecimentos próximos")
                find_establishments()
            case 2:
                load("Carregando dados do veículo")
                vehicle_manager(user)
            case 3:
                load("Verificando carregadores disponíveis")
                session_manager(user, action='iniciar')
            case 4:
                load("Buscando sua sessão ativa")
                session_manager(user, action='encerrar')
            case 5:
                load("Carregando histórico de sessões")
                session_history(user)
            case 0:
                load("Saindo")
                break
            case _:
                error_option()