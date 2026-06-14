from database.database import sessions, fares
from utils.helpers import get_user_charger, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import header

PRICE_GASOLINE_PER_LITER = 6.20   # R$ por litro simulado
KM_PER_LITER = 12                  # consumo médio carro a gasolina
KWH_PER_100KM = 15                 # consumo médio elétrico
PRICE_KWH_RESIDENTIAL = fares['base']




def residential_dashboard(user):
    reset_terminal()
    header("DASHBOARD DE ECONOMIA")

    vehicle = get_user_vehicle(user)
    charger = get_user_charger(user)
    user_sessions = [s for s in sessions if s['usuario_id'] == user['id'] and s['status'] == 'finalizada']

    total_kwh = sum(s['energia_kwh'] for s in user_sessions)
    total_spent_electric = round(sum(s['valor'] for s in user_sessions), 2)
    total_km_equivalent = round(total_kwh / KWH_PER_100KM * 100)

    # Quanto teria gasto com gasolina para rodar os mesmos km
    liters_needed = round(total_km_equivalent / KM_PER_LITER, 2)
    total_spent_gasoline = round(liters_needed * PRICE_GASOLINE_PER_LITER, 2)
    savings = round(total_spent_gasoline - total_spent_electric, 2)
    co2_avoided = round(total_kwh * 0.233, 2)

    print(f"\n--- Veículo ---")
    if vehicle:
        battery_kwh_now = round(vehicle['bateria_kwh'] * vehicle['nivel_bateria'] / 100, 1)
        autonomy = round(battery_kwh_now / KWH_PER_100KM * 100)
        print(f"Modelo:          {vehicle['modelo']}")
        print(f"Bateria atual:   {vehicle['nivel_bateria']}%  ({battery_kwh_now} kWh)")
        print(f"Autonomia atual: ~{autonomy} km")
    else:
        print("Nenhum veículo cadastrado.")

    print(f"\n--- Carregador Residencial ---")
    if charger:
        print(f"Modelo:   {charger['modelo']}")
        print(f"Status:   {charger['status'].upper()}")
        print(f"Potência: {charger['potencia_maxima']} kW")
        print(f"Total de sessões: {charger['total_sessoes']}")
        print(f"Energia fornecida: {charger['energia_fornecida_kwh']} kWh")
    else:
        print("Nenhum carregador encontrado.")

    print(f"\n--- Comparativo Financeiro ---")
    print(f"Energia carregada:       {total_kwh:.1f} kWh")
    print(f"Equivalente em km:       ~{total_km_equivalent} km")
    print(f"\nGasto elétrico:          R$ {total_spent_electric:.2f}")
    print(f"Gasto estimado gasolina: R$ {total_spent_gasoline:.2f}")
    print(f"\n💰 Economia total:       R$ {savings:.2f}")
    print(f"🌿 CO₂ evitado:          {co2_avoided} kg")

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")