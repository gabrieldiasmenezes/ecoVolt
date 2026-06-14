from service.admin.kpis import kpis_dashboard
from service.admin.tariffs import tariff_manager
from service.admin.royalties import royalties_report
from service.admin.failures import failure_monitor
from service.admin.firmware import firmware_manager
from service.admin.syndic import virtual_syndic
from utils.system import load, reset_terminal
from utils.ui import error_option, header
from utils.validate.mutual_data import validate_option


def admin_service(user):
    while True:
        reset_terminal()
        header('ADMINISTRADOR GOODWE — PAINEL MASTER')
        print(f"\nBem-vindo, {user['nome'].split()[0]}. Acesso total à rede.\n")

        options = validate_option("""
1 - KPIs e Disponibilidade da Rede
2 - Ajuste Global de Tarifas
3 - Relatório de Royalties
4 - Monitor de Falhas Críticas
5 - Gestão de Firmware
6 - Síndico Virtual (IA)
0 - Sair

Opção: """)

        match options:
            case 1:
                load("Consolidando dados da rede")
                kpis_dashboard()
            case 2:
                load("Carregando painel de tarifas")
                tariff_manager()
            case 3:
                load("Gerando relatório de royalties")
                royalties_report()
            case 4:
                load("Escaneando falhas críticas")
                failure_monitor()
            case 5:
                load("Verificando versões de firmware")
                firmware_manager()
            case 6:
                load("Iniciando Síndico Virtual")
                virtual_syndic()
            case 0:
                load("Saindo")
                break
            case _:
                error_option()