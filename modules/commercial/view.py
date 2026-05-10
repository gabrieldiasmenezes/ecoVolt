import time
from core.utils import get_numeric_input, get_menu_option

def get_charge_power():
    """
    Recebe a escolha do usuário para potência do carregador e retorna o valor em kW.
    Retorna None se o usuário escolher sair.
    """
    station_menu = """
Defina qual carregador deseja utilizar:
  1 - 7kW  (Carga Lenta)
  2 - 11kW (Carga Padrão)
  3 - 22kW (Carga Rápida)
  4 - Saiba qual o melhor para você
  5 - Voltar ao Menu Anterior

Opção: """

    while True:
        choice = get_menu_option("SELEÇÃO DE CARREGADOR", station_menu)
        match choice:
            case 1:
                print("\n[INFO] Carregador 7kW selecionado.")
                return 7
            case 2:
                print("\n[INFO] Carregador 11kW selecionado.")
                return 11
            case 3:
                print("\n[INFO] Carregador 22kW selecionado.")
                return 22
            case 4:
                print("\n[INFO] Para carregamento comercial rápido, escolha 22kW; para equilíbrio, 11kW.")
            case 5:
                print("\n[!] Retornando ao menu anterior.")
                return None
            case _:
                print("\n[!] Opção inválida. Tente novamente.")

def get_battery_data():
    """
    Solicita ao usuário os dados de bateria, validando capacidade,
    nível atual e meta de carga.
    """
    print("\n--- CONFIGURAÇÃO DA RECARGA ---")

    capacity = get_numeric_input(
        "Capacidade total da bateria (kWh): ",
        min_val=0.1,
        error_msg="A capacidade deve ser maior que zero."
    )

    current = get_numeric_input(
        "Nível atual da bateria (0-99%): ",
        min_val=0,
        max_val=99,
        error_msg="Informe um valor entre 0 e 99."
    )

    while True:
        target = get_numeric_input(
            "Meta de carga da bateria (1-100%): ",
            min_val=current + 1,
            max_val=100,
            error_msg=f"A meta deve ser maior que o SOC atual ({current}%)."
        )
        if target > current:
            break
        print(f"[!] A meta deve ser maior que o nível atual ({current}%).")

    return {
        "capacity": capacity,
        "current": current,
        "target": target
    }

def start_charging_simulation(battery_data, charger_power):
    """
    Simula a recarga com uma barra de progresso e exibe status até o fim.
    """
    print("\n[RECARGA EM ANDAMENTO]")
    print(f"Nível inicial: {battery_data['current']}% | Meta: {battery_data['target']}%")
    print(f"Potência do carregador: {charger_power} kW")

    for percent in range(int(battery_data["current"]), int(battery_data["target"]) + 1, 5):
        bar = "#" * (percent // 5) + "-" * ((100 - percent) // 5)
        print(f"Progresso: [{bar}] {percent}%   ", end="\r")
        time.sleep(0.2)
    print("\n[SISTEMA] Recarga finalizada com sucesso.")