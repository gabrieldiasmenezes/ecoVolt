from datetime import datetime
from utils.helpers import get_user_active_session, get_user_charger, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import header


def end_residential_session(user):
    reset_terminal()
    header("ENCERRAR RECARGA")

    session = get_user_active_session(user)
    if not session:
        print("\nNenhuma sessão ativa.")
        input("\nEnter...")
        return

    charger = get_user_charger(user)
    vehicle = get_user_vehicle(user)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    session['fim'] = now
    session['status'] = 'finalizada'

    co2 = round(session['energia_kwh'] * 0.233, 2)

    if charger:
        charger['status'] = 'livre'
        charger['potencia_atual'] = 0

    if vehicle:
        gain = int((session['energia_kwh'] / vehicle['bateria_kwh']) * 100)
        vehicle['nivel_bateria'] = min(100, vehicle['nivel_bateria'] + gain)

    reset_terminal()
    header("SESSÃO ENCERRADA")

    print(f"\nSessão #{session['id']} finalizada")
    print(f"Energia: {session['energia_kwh']} kWh")
    print(f"Custo: R$ {session['valor']}")
    print(f"CO₂ evitado: {co2} kg")

    input("\nEnter...")