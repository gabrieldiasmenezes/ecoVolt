from .view import display_financial_report, display_devices_status, update_device_status
from .logic import get_yield_ranking
from modules.common.database import financial_mock,devices_mock
from core.utils import header,get_menu_option

admin_choice="""
Olá, Administrador! O que deseja gerir hoje?

1 - Relatórios Financeiros (Faturamento)
2 - Status de Dispositivos (Monitoramento em Tempo Real)
3 - Ranking de Rendimento (Melhor vs Pior desempenho)
4 - Alterar Status de Dispositivo (Manutenção)
5 - Voltar ao Menu Anterior

Escolha uma opção: """

def run_establishment_module():
    while True:
        choice = get_menu_option("PAINEL DE GESTÃO DO ESTABELECIMENTO",admin_choice)

        match choice:
            case 1:
                display_financial_report(financial_mock)
            case 2:
                display_devices_status(devices_mock)
            case 3:
                # Usando a Logic para processar e a View para mostrar
                ranking = get_yield_ranking(devices_mock)
                header("RANKING DE RENDIMENTO", 50)
                for i, dev in enumerate(ranking, 1):
                    print(f"{i}º - {dev['id']:<10} | R$ {dev['rendimento']:>10.2f}")
            case 4:
                # Agora chamamos a função que você acabou de criar!
                update_device_status(devices_mock)
            case 5:
                print("Voltando ao menu de acesso...")
                break
            case _:
                print("\n[!] Opção inválida.")
        
        input("\nPressione Enter para continuar...")