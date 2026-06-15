"""demo.py

Script que demonstra multiplos cenarios:
- inicia 3 sessões (não interativo)
- mostra controle DLM / simulação de sobrecarga
- gera relatório do estabelecimento

Use: python demo.py
"""
from datetime import datetime

from database import database as db
from utils.helpers import get_user_vehicle, get_establishment_data_by_id
from modules.comercial.feature.pricing import calculate_fare
from modules.sessions.features.comercial.session_create import create_session
from modules.establishment.features.demand_control import simulate_overload


def estimate_time(kwh_to_charge, charger_power_kw):
    if charger_power_kw == 0:
        return 0
    return round((kwh_to_charge / charger_power_kw) * 60)


def find_user(user_id):
    for u in db.users:
        if u['id'] == user_id:
            return u
    return None


def start_demo_session(user_id, kwh):
    user = find_user(user_id)
    if not user:
        print(f"Usuário {user_id} não encontrado")
        return

    vehicle = get_user_vehicle(user_id)
    if not vehicle:
        print(f"Usuário {user_id} sem veículo cadastrado")
        return

    # escolher primeiro carregador livre
    available = [c for c in db.establishment_chargers if c['status'] == 'livre']
    if not available:
        print("Nenhum carregador livre disponível para demo")
        return

    charger = available[0]
    is_premium = charger.get('reservado_premium', False)
    hora = datetime.now().hour
    is_peak = db.fares['inicio_horario_pico'] <= hora < db.fares['fim_horario_pico']

    fare, session_type, reason = calculate_fare(is_premium, is_peak, False)
    minutes = estimate_time(kwh, charger['potencia_maxima'])
    total_price = round(kwh * fare, 2)

    result = {
        'charger': charger,
        'tarifa': fare,
        'tipo_sessao': session_type,
        'motivo': reason,
        'total_price': total_price,
        'minutes': minutes
    }

    create_session(user, vehicle, result, kwh, f"Demo: {kwh} kWh")


def main():
    print("== Demo: iniciar 3 sessões (usuários 1000,1001,1002) ==")

    print("\nEstado inicial: sessões ativas", len([s for s in db.sessions if s['status'] == 'ativa']))

    start_demo_session(1000, 10)
    start_demo_session(1001, 10)
    start_demo_session(1002, 10)

    print("\nApós iniciar sessões:")
    print(f"Sessões ativas: {len([s for s in db.sessions if s['status'] == 'ativa'])}")
    total_power = sum(c['potencia_atual'] for c in db.establishment_chargers)
    print(f"Potência total em uso (estabelecimento): {total_power} kW")

    # Simular sobrecarga usando o módulo de controle de demanda
    data = get_establishment_data_by_id(1003)
    print("\n== Simulação DLM ==")
    simulate_overload(data['chargers'])

    # Gerar relatório
    print("\n== Relatório do estabelecimento ==")
    from modules.establishment.features.reports import reports
    reports(data['establishment'], data['sessions'])


if __name__ == '__main__':
    main()
