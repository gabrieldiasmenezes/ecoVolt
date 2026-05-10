from core.utils import get_menu_option
from .view import (display_global_dashboard,update_global_fees,
    display_royalties_report,display_network_health)
admin_master_menu = """
BEM-VINDO, GOODWE MASTER ADMIN

1 - Dashboard Global (Status da Rede)
2 - Ajustar Tarifas do Sistema (Preço kWh)
3 - Relatório de Royalties (Receita B2B)
4 - Relatório de Saúde da Rede
5 - Voltar ao Menu Anterior

Escolha uma opção: """


def run_admin_module():
    while True:
        choice = get_menu_option("PAINEL DE CONTROLE MASTER - GOODWE", admin_master_menu, 65)

        match choice:
            case 1:
                display_global_dashboard()
            case 2:
                update_global_fees()
            case 3:
                display_royalties_report()
            case 4:
                display_network_health()
            case 5:
                print("Voltando ao menu de acesso...")
                break
            case _:
                print("\n[!] Opção inválida.")

        input("\nPressione Enter para continuar...")