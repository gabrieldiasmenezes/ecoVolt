from .view import get_charge_power, get_battery_data,start_charging_simulation
from .logic import get_fee_per_kwh
from core.utils import get_separator, header

station_menu = """
Defina qual carregador deseja utilizar:
  1 - 7kW  (Carga Lenta)
  2 - 11kW (Carga Padrão)
  3 - 22kW (Carga Rápida)
  4 - Saiba qual o melhor para você
  5 - Voltar ao Menu Anterior
  
  Opção: """

def run_commercial_module():
    """
    Orquestra o módulo comercial:
    1. Seleção de carregador
    2. Coleta de dados da bateria
    3. Cálculo de energia, tempo e custo
    4. Confirmação
    5. Simulação
    6. Registro da sessão
    """
    header("MÓDULO COMERCIAL - GOODWE", 50)

    charger_power = get_charge_power()
    if charger_power is None:
        return
    battery_data = get_battery_data()

    energy_to_add = ((battery_data["target"] - battery_data["current"]) / 100) * battery_data["capacity"]
    fee_per_kwh = get_fee_per_kwh()
    estimated_cost = energy_to_add * fee_per_kwh
    charging_time_hours = energy_to_add / charger_power
    charging_time_minutes = charging_time_hours * 60


    print(f"""
{get_separator(30)}
RESUMO DA OPERAÇÃO
- Energia necessária: {energy_to_add:.2f} kWh
- Tempo estimado: {charging_time_minutes:.0f} minutos
- Custo total: R$ {estimated_cost:.2f}
{get_separator(30)}
    """)

    confirm = input("\nDeseja iniciar a recarga com estes valores? (s/n): ").lower().strip()
    
    if confirm != "s":
        print("\n[!] Operação cancelada. Retornando ao menu.")
        return
    
    start_charging_simulation(battery_data, charger_power)

    print(f"""
{get_separator(30)}
[SISTEMA] Setup finalizado para o operador.
[SISTEMA] Estação preparada: {charger_power}kW
[SISTEMA] Total carregado: {energy_to_add:.2f} kWh | Custo: R$ {estimated_cost:.2f}
[SISTEMA] Tempo de sessão: {charging_time_minutes:.0f} min
{get_separator(30)}
    """)
    input("\nPressione Enter para retornar ao menu...")
