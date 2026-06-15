from datetime import datetime
from database.database import establishment_chargers, sessions, establishments
from modules.ocpp_event import register_ocpp_event
from utils.helpers import get_user_active_session, get_user_vehicle, current_power_usage
from utils.system import reset_terminal, load
from utils.ui import footer, header, enter
from database.settings import LIMIT_SIMULATION


def create_session(user, vehicle, result, kwh_to_charge, charge_desc):
    charger = result['charger']
    fare = result['tarifa']
    session_type = result['tipo_sessao']
    total_price = result['total_price']
    minutes = result['minutes']
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    load("\nRegistrando sessão no gateway OCPP")
    print()
    register_ocpp_event(charger['id'], "BootNotification", "Carregador autenticado")
    register_ocpp_event(charger['id'], "StartTransaction", f"Sessão iniciada — {kwh_to_charge} kWh solicitados")

    # Verifica impacto na demanda e aplica limitação DLM se necessário
    est = next((e for e in establishments if e['id'] == charger.get('estabelecimento_id')), None)
    est_limit = est['demanda_maxima_kw'] if est else LIMIT_SIMULATION

    current_total = current_power_usage(establishment_chargers)
    allowed_limit = min(est_limit, LIMIT_SIMULATION)
    allowed_additional = max(0, allowed_limit - current_total)

    # Decide potência alocada para a sessão (pode ser reduzida pelo DLM)
    if allowed_additional <= 0:
        allocated_power = 0
    else:
        allocated_power = min(charger['potencia_maxima'], allowed_additional)

    if allocated_power < charger['potencia_maxima']:
        register_ocpp_event(charger['id'], "MeterValues", f"Potência reduzida para {allocated_power} kW devido a DLM")
    else:
        register_ocpp_event(charger['id'], "MeterValues", f"Potência: {allocated_power} kW")

    new_session = {
        "id": max(s['id'] for s in sessions) + 1,
        "usuario_id": user['id'],
        "veiculo_id": vehicle['id'],
        "carregador_id": charger['id'],
        "tipo": session_type,
        "potencia_kw": allocated_power,
        "energia_kwh": kwh_to_charge,
        "tarifa_kwh": fare,
        "valor":  total_price,
        "inicio": now,
        "fim":    None,
        "status": "ativa"
    }

    sessions.append(new_session)
    charger['status'] = 'em_uso'
    charger['potencia_atual'] = allocated_power
    charger['total_sessoes']  += 1

    reset_terminal()
    header("RECARGA INICIADA")
    print(f"\n✅ Sessão #{new_session['id']} iniciada!")
    print(f"\nConecte seu veículo ao Carregador #{charger['numero']}")
    print(f"\n{charge_desc}")
    print(f"Tempo estimado: ~{minutes} min")
    print(f"Valor pago:     R$ {total_price:.2f}")
    footer()


def end_session_flow(user):
    reset_terminal()
    header("ENCERRAR RECARGA")

    session = get_user_active_session(user)
    if not session:
        print("\nNenhuma sessão ativa encontrada.")
        enter()
        return

    vehicle = get_user_vehicle(user)
    charger = next((c for c in establishment_chargers if c['id'] == session['carregador_id']), None)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    co2_avoided = round(session['energia_kwh'] * 0.233, 2)

    load("Comunicando encerramento ao gateway OCPP")
    print()
    register_ocpp_event(session['carregador_id'], "StopTransaction", f"Sessão #{session['id']} encerrada")
    register_ocpp_event(session['carregador_id'], "MeterValues",     f"Energia fornecida: {session['energia_kwh']} kWh")

    session['fim']    = now
    session['status'] = 'finalizada'

    if charger:
        charger['status'] = 'livre'
        charger['potencia_atual'] = 0
        charger['energia_fornecida_kwh'] += session['energia_kwh']

    if vehicle:
        ganho_pct = round((session['energia_kwh'] / vehicle['bateria_kwh']) * 100)
        vehicle['nivel_bateria'] = min(100, vehicle['nivel_bateria'] + ganho_pct)

    reset_terminal()
    header("SESSÃO ENCERRADA")
    print(f"\n✅ Sessão #{session['id']} finalizada.")
    print(f"\nEnergia carregada: {session['energia_kwh']} kWh")
    print(f"Tarifa: R$ {session['tarifa_kwh']:.2f}/kWh")
    print(f"Valor:  R$ {session['valor']:.2f}")
    if vehicle:
        print(f"\nBateria atual: {vehicle['nivel_bateria']}%")
    print(f"\n🌿 CO₂ evitado: {co2_avoided} kg")
    print(f"\nInício: {session['inicio']}")
    print(f"Fim: {now}")
    footer()