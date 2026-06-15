from datetime import datetime
from database.database import sessions
from database.settings import CHARGE_MODES, DLM_CIRCUIT_BREAKER_LIMIT_KW
from utils.helpers import get_user_active_session,get_user_charger,get_user_vehicle
from utils.system import choose_soc_target, load, reset_terminal
from utils.ui import enter, footer, header, error_option
from utils.validation.common_validation import validate_int_value
from modules.sessions.features.residential.pricing import calculate_price


def start_residential_session(user):
    reset_terminal()
    header("INICIAR RECARGA RESIDENCIAL")

    if get_user_active_session(user):
        print("\nSessão já ativa.")
        enter()
        return

    charger = get_user_charger(user['id'])
    vehicle = get_user_vehicle(user['id'])

    if not charger or charger['status'] == 'em_uso':
        print("\nProblema com carregador.")
        enter()
        return

    if not vehicle:
        print("\nNenhum veículo cadastrado.")
        enter()
        return
    while True:
        reset_terminal()
        header("MODO DE CARGA")

        for key, mode in CHARGE_MODES.items():
            print(f"[{key}] {mode['nome']} - {mode['potencia_kw']} kW")
        
        mode_option = validate_int_value("Escolha o modo: ")
        if mode_option not in CHARGE_MODES:
            error_option()
            continue
        break

    chosen_mode = CHARGE_MODES[mode_option]
    power_kw = min(chosen_mode['potencia_kw'], DLM_CIRCUIT_BREAKER_LIMIT_KW)

    soc_target = choose_soc_target(vehicle)

    price_info = calculate_price(chosen_mode, power_kw, vehicle, soc_target)

    while True:
        reset_terminal()
        header("RESUMO")

        print(f"Modo: {chosen_mode['nome']}")
        print(f"Potência: {power_kw} kW")
        print(f"De {vehicle['nivel_bateria']}% → {soc_target}%")
        print(f"Energia: {price_info['kwh']} kWh")
        print(f"Tempo: ~{price_info['minutes']} min")
        print(f"Tarifa: R$ {price_info['tarifa']}/kWh ({price_info['motivo']})")
        print(f"Total: R$ {price_info['total']}")

        confirm = validate_int_value("\n1 Confirmar / 0 Cancelar: ")
        if confirm == 0:
            return
        elif confirm != 1:
            error_option()
            continue
        break

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    new_session = {
        "id": max(s['id'] for s in sessions) + 1,
        "usuario_id": user['id'],
        "veiculo_id": vehicle['id'],
        "carregador_id": charger['id'],
        "tipo": "residencial",
        "potencia_kw": power_kw,
        "energia_kwh": price_info['kwh'],
        "tarifa_kwh": price_info['tarifa'],
        "valor": price_info['total'],
        "soc_alvo": soc_target,
        "modo": chosen_mode['nome'],
        "inicio": now,
        "fim": None,
        "status": "ativa"
    }
    load('Enviando dados ao sistema')
    sessions.append(new_session)

    charger['status'] = 'em_uso'
    charger['potencia_atual'] = power_kw

    reset_terminal()
    header("RECARGA INICIADA")

    print(f"\nSessão #{new_session['id']} iniciada!")
    footer()