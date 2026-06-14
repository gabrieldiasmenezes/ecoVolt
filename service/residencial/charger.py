from utils.helpers import get_user_charger, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import header

DLM_CIRCUIT_BREAKER_LIMIT_KW = 5.0  # limite do disjuntor residencial simulado


def residential_charger_view(user):
    reset_terminal()
    header("MEU CARREGADOR RESIDENCIAL")

    charger = get_user_charger(user)
    if not charger:
        print("\nNenhum carregador residencial encontrado.")
        input("\nAperte Enter para voltar...")
        return

    vehicle = get_user_vehicle(user)

    power_in_use = charger['potencia_atual']
    home_load_kw = round(DLM_CIRCUIT_BREAKER_LIMIT_KW - power_in_use, 1)

    print(f"\nModelo:            {charger['modelo']}")
    print(f"Status:            {charger['status'].upper()}")
    print(f"Potência máxima:   {charger['potencia_maxima']} kW")
    print(f"Potência atual:    {power_in_use} kW")
    print(f"Total de sessões:  {charger['total_sessoes']}")
    print(f"Energia fornecida: {charger['energia_fornecida_kwh']} kWh")

    print(f"\n--- Controle DLM (Disjuntor) ---")
    print(f"Limite do disjuntor: {DLM_CIRCUIT_BREAKER_LIMIT_KW} kW")
    print(f"Carga residencial:   {home_load_kw} kW disponível")

    bar_fill = int((power_in_use / DLM_CIRCUIT_BREAKER_LIMIT_KW) * 20)
    bar = "█" * bar_fill + "░" * (20 - bar_fill)
    pct = int(power_in_use / DLM_CIRCUIT_BREAKER_LIMIT_KW * 100)
    print(f"\nCarga: [{bar}] {pct}%")

    if power_in_use >= DLM_CIRCUIT_BREAKER_LIMIT_KW * 0.9:
        print("\n⚠  ALERTA: Próximo do limite do disjuntor!")
        print("   DLM reduzindo potência automaticamente.")

    if vehicle:
        print(f"\n--- Veículo Conectado ---")
        print(f"Modelo:   {vehicle['modelo']}")
        print(f"Bateria:  {vehicle['nivel_bateria']}%")

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")