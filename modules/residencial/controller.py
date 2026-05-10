from core.utils import get_menu_option, header
from modules.common.database import residencial_data
from modules.residencial.logic import get_home_battery_telemetry, calculate_home_economy_savings
from modules.residencial.view import display_home_economy, display_home_hardware_details, setup_residential_user, start_home_charging_simulation



def run_residential_module(name):
    """
    Orquestra o módulo residencial: verifica setup, exibe menu e chama funções apropriadas.
    Personaliza com o nome do usuário e garante validações para modelo do carro e dados necessários.
    """
    # Verifica se o usuário precisa de setup inicial (onboarding)
    if not residencial_data.get("configurado", False):
        setup_residential_user(name) 
    
    while True:
        header(f"PAINEL RESIDENCIAL - {residencial_data['usuario'].upper()}", 50)
        menu_text = """
1 - Visualizar Dashboard de Economia
2 - Informações Técnicas do Carregador
3 - Recarga
4 - Voltar ao Menu Anterior

Escolha uma opção: """
        
        titulo = f"PAINEL RESIDENCIAL - {residencial_data['usuario'].upper()}"
        choice = get_menu_option(titulo, menu_text)
        
        match choice:
            case 1:
                # Calcula e exibe economia (chama logic para cálculo, view para exibição)
                savings = calculate_home_economy_savings()
                display_home_economy(savings)
            case 2:
                # Exibe informações técnicas do carregador (view)
                display_home_hardware_details()
            case 3:
                # Simula recarga: obtém telemetria (logic) e inicia simulação (view)
                battery_data = get_home_battery_telemetry()
                start_home_charging_simulation(battery_data)
            case 4:
                print("Saindo do painel residencial...")
                break
            case _:
                print("\n[!] Opção inválida.")
        
        input("\nPressione Enter para continuar...")