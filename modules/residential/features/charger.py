from database.settings import DLM_CIRCUIT_BREAKER_LIMIT_KW
from utils.helpers import get_user_charger, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import enter, footer, header, progress_bar

def show_charge_model(charger,power_in_use):
    print(f"\nModelo: {charger['modelo']}")
    print(f"Status: {charger['status'].upper()}")
    print(f"Potência máxima: {charger['potencia_maxima']} kW")
    print(f"Potência atual: {power_in_use} kW")
    print(f"Total de sessões: {charger['total_sessoes']}")
    print(f"Energia fornecida:{charger['energia_fornecida_kwh']} kWh")

def show_dlm_control(power_in_use):
    home_load_kw = round(DLM_CIRCUIT_BREAKER_LIMIT_KW - power_in_use, 1)
    bar,pct=progress_bar(power_in_use,DLM_CIRCUIT_BREAKER_LIMIT_KW)

    print(f"\n--- Controle DLM (Disjuntor) ---")
    print(f"Limite do disjuntor: {DLM_CIRCUIT_BREAKER_LIMIT_KW} kW")
    print(f"Carga residencial:   {home_load_kw} kW disponível")

    print(f"\nCarga: [{bar}] {pct}%")

    if power_in_use >= DLM_CIRCUIT_BREAKER_LIMIT_KW * 0.9:
        print("\n⚠  ALERTA: Próximo do limite do disjuntor!")
        print("   DLM reduzindo potência automaticamente.")

def show_vehicle_data(vehicle):
    if vehicle:
        print(f"\n--- Veículo Conectado ---")
        print(f"Modelo:   {vehicle['modelo']}")
        print(f"Bateria:  {vehicle['nivel_bateria']}%")
    else:
        print("Sem veículo cadastrado!")

def residential_charger_view(user):
    reset_terminal()
    header("MEU CARREGADOR RESIDENCIAL")

    charger = get_user_charger(user['id'])
    if not charger:
        print("\nNenhum carregador residencial encontrado.")
        enter()
        return

    vehicle = get_user_vehicle(user['id'])

    power_in_use = charger['potencia_atual']

    show_charge_model(charger,power_in_use)

    show_dlm_control(power_in_use)

    show_vehicle_data(vehicle)

    footer()