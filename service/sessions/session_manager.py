from datetime import datetime
from database.database import (
    establishment_chargers, sessions,fares, ocpp_logs, settings
)
from service.comercial.billing import billing_service
from service.comercial.pricing import calculate_fare

from service.vehicle_menager import prompt_register_if_no_vehicle
from utils.helpers import get_user_active_session, get_user_vehicle
from utils.system import reset_terminal, load
from utils.ui import header, error_option
from utils.validate.mutual_data import validate_option


KWH_PER_100KM = 15


def estimate_time(kwh_to_charge, charger_power_kw):
    if charger_power_kw == 0:
        return 0
    return round((kwh_to_charge / charger_power_kw) * 60)


def register_ocpp_event(charger_id, event_type, message):
    if not settings.get('ocpp_ativo'):
        return
    new_log = {
        "id": max(log['id'] for log in ocpp_logs) + 1 if ocpp_logs else 1,
        "carregador_id": charger_id,
        "tipo": event_type,
        "mensagem": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ocpp_logs.append(new_log)
    print(f"  [OCPP] {event_type} → {message}")


def choose_charge_amount(vehicle):

    reset_terminal()
    header("QUANTO DESEJA CARREGAR?")

    battery_current_pct = vehicle['nivel_bateria']
    battery_kwh = vehicle['bateria_kwh']
    battery_available = round(battery_kwh * battery_current_pct / 100, 2)
    autonomy_now = round(battery_available / KWH_PER_100KM * 100)

    print(f"\nVeículo:        {vehicle['modelo']}")
    print(f"Bateria atual:  {battery_current_pct}%  ({battery_available} kWh)")
    print(f"Autonomia atual: ~{autonomy_now} km\n")

    option = validate_option("""
1 - Por nível de bateria desejado (%)
2 - Por distância desejada (km)
0 - Voltar

Opção: """)

    if option == 0:
        return None, None

    if option == 1:
        return _charge_by_battery(vehicle)
    elif option == 2:
        return _charge_by_distance(vehicle)
    else:
        error_option()
        return None, None


def _charge_by_battery(vehicle):
    battery_current_pct = vehicle['nivel_bateria']
    battery_kwh = vehicle['bateria_kwh']
    min_target = battery_current_pct + 10
    
    print(f"\nNível atual:  {battery_current_pct}%")
    print(f"Mínimo permitido: {min_target}%  (mínimo 10% acima do atual)")
    print(f"Máximo permitido: 100%\n")

    while True:
        try:
            target_pct = int(input(f"Nível desejado (%) [{min_target}–100]: ").strip())
            if target_pct < min_target:
                print(f"O nível deve ser pelo menos {min_target}% (10% acima do atual).")
                continue
            if target_pct > 100:
                print("O nível não pode ultrapassar 100%.")
                continue
            break
        except ValueError:
            print("Digite apenas números inteiros.")

    kwh_to_charge = round((target_pct - battery_current_pct) / 100 * battery_kwh, 2)
    autonomy_after = round(target_pct / 100 * battery_kwh / KWH_PER_100KM * 100)
    descricao = f"Bateria: {battery_current_pct}% → {target_pct}%  (~{autonomy_after} km de autonomia)"

    return kwh_to_charge, descricao


def _charge_by_distance(vehicle):
    battery_current_pct = vehicle['nivel_bateria']
    battery_kwh = vehicle['bateria_kwh']
    battery_available = round(battery_kwh * battery_current_pct / 100, 2)
    autonomy_now = round(battery_available / KWH_PER_100KM * 100)

    print(f"\nAutonomia atual: ~{autonomy_now} km\n")

    while True:
        try:
            extra_km = float(input("Quantos km extras deseja garantir?: ").strip())
            if extra_km <= 0:
                print("Informe um valor maior que zero.")
                continue

            kwh_needed_extra = round(extra_km * KWH_PER_100KM / 100, 2)
            kwh_total_needed = round(battery_available + kwh_needed_extra, 2)
            target_pct = round(kwh_total_needed / battery_kwh * 100)

            if target_pct > 100:
                max_extra = round((battery_kwh - battery_available) / KWH_PER_100KM * 100)
                print(f"Com a bateria cheia você consegue no máximo +{max_extra} km extras.")
                print(f"Informe um valor até {max_extra} km.")
                continue
            break
        except ValueError:
            print("Digite apenas números.")

    kwh_to_charge = kwh_needed_extra
    autonomy_after = autonomy_now + int(extra_km)
    descricao = f"Distância extra: +{int(extra_km)} km  (autonomia total: ~{autonomy_after} km)"

    return kwh_to_charge, descricao


def session_manager(user, action):
    if action == 'iniciar':
        start_session(user)
    elif action == 'encerrar':
        end_session(user)


def start_session(user):
    reset_terminal()
    header("INICIAR RECARGA")

    active = get_user_active_session(user)
    if active:
        print(f"\nVocê já possui uma sessão ativa (ID #{active['id']}).")
        print("Encerre-a antes de iniciar uma nova.")
        input("\nAperte Enter para voltar...")
        return

    vehicle = get_user_vehicle(user)
    if not vehicle:

        prompt_register_if_no_vehicle(user)
        return

    # Escolha de quanto carregar
    kwh_to_charge, charge_desc = choose_charge_amount(vehicle)
    if kwh_to_charge is None:
        return

    # Carregadores disponíveis
    available = [c for c in establishment_chargers if c['status'] == 'livre']
    if not available:
        print("\nNenhum carregador disponível no momento.")
        input("\nAperte Enter para voltar...")
        return

    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']

    reset_terminal()
    header("ESCOLHA O CARREGADOR")
    print(f"\n{charge_desc}")
    print(f"Energia a carregar: {kwh_to_charge} kWh\n")
    print("--- Carregadores Disponíveis ---\n")

    for i, c in enumerate(available):
        is_premium = c.get('reservado_premium', False)
        tarifa, tipo_sessao, motivo = calculate_fare(is_premium, is_peak, False)
        minutes = estimate_time(kwh_to_charge, c['potencia_maxima'])
        total_price = round(kwh_to_charge * tarifa, 2)
        tipo_label = "🔶 Premium" if is_premium else "🔷 Comum"

        print(f"  [{i+1}] Carregador #{c['numero']}  {tipo_label}")
        print(f"       Potência:   {c['potencia_maxima']} kW")
        print(f"       Tarifa:     R$ {tarifa:.2f}/kWh  ({motivo})")
        print(f"       Tempo est:  ~{minutes} min")
        print(f"       Total:      R$ {total_price:.2f}")
        print()

    option = validate_option("Escolha um carregador (0 para voltar): ")
    if option == 0:
        return
    if option < 1 or option > len(available):
        error_option()
        return

    chosen = available[option - 1]
    is_premium = chosen.get('reservado_premium', False)
    tarifa, tipo_sessao, motivo = calculate_fare(is_premium, is_peak, False)
    total_price = round(kwh_to_charge * tarifa, 2)
    minutes = estimate_time(kwh_to_charge, chosen['potencia_maxima'])

    # Resumo + confirmação de pagamento
    reset_terminal()
    header("RESUMO E CONFIRMAÇÃO")
    print(f"\n{charge_desc}")
    print(f"\nCarregador:       #{chosen['numero']}  {'🔶 Premium' if is_premium else '🔷 Comum'}")
    print(f"Energia:          {kwh_to_charge} kWh")
    print(f"Tarifa:           R$ {tarifa:.2f}/kWh  ({motivo})")
    print(f"Tempo estimado:   ~{minutes} min")
    print(f"\nValor total:      R$ {total_price:.2f}")
    if is_peak:
        print("\n⚡ Horário de pico ativo (18h–21h)")
    print("\n" + "=" * 40)

    confirm = validate_option("\n1 - Confirmar e pagar\n0 - Cancelar\n\nOpção: ")
    if confirm != 1:
        print("\nRecarga cancelada.")
        input("\nAperte Enter para voltar...")
        return

    # Cobrança
    paid = billing_service(user, total_price, tipo_sessao)
    if not paid:
        return

    # Registra no OCPP
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    load("\nRegistrando sessão no gateway OCPP")
    print()
    register_ocpp_event(chosen['id'], "BootNotification", "Carregador autenticado")
    register_ocpp_event(chosen['id'], "StartTransaction", f"Sessão iniciada — {kwh_to_charge} kWh solicitados")
    register_ocpp_event(chosen['id'], "MeterValues", f"Potência: {chosen['potencia_maxima']} kW")

    # Cria sessão
    new_session = {
        "id": max(s['id'] for s in sessions) + 1,
        "usuario_id": user['id'],
        "veiculo_id": vehicle['id'],
        "carregador_id": chosen['id'],
        "tipo": tipo_sessao,
        "potencia_kw": chosen['potencia_maxima'],
        "energia_kwh": kwh_to_charge,
        "tarifa_kwh": tarifa,
        "valor": total_price,
        "inicio": now,
        "fim": None,
        "status": "ativa"
    }

    sessions.append(new_session)
    chosen['status'] = 'em_uso'
    chosen['potencia_atual'] = chosen['potencia_maxima']
    chosen['total_sessoes'] += 1

    reset_terminal()
    header("RECARGA INICIADA")
    print(f"\n✅ Sessão #{new_session['id']} iniciada!")
    print(f"\nConecte seu veículo ao Carregador #{chosen['numero']}")
    print(f"\n{charge_desc}")
    print(f"Tempo estimado:  ~{minutes} min")
    print(f"Valor pago:      R$ {total_price:.2f}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")


def end_session(user):
    reset_terminal()
    header("ENCERRAR RECARGA")

    session = get_user_active_session(user)
    if not session:
        print("\nNenhuma sessão ativa encontrada.")
        input("\nAperte Enter para voltar...")
        return

    vehicle = get_user_vehicle(user)
    charger = next((c for c in establishment_chargers if c['id'] == session['carregador_id']), None)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    co2_evitado = round(session['energia_kwh'] * 0.233, 2)

    # Registra encerramento no OCPP
    load("Comunicando encerramento ao gateway OCPP")
    print()
    register_ocpp_event(session['carregador_id'], "StopTransaction", f"Sessão #{session['id']} encerrada")
    register_ocpp_event(session['carregador_id'], "MeterValues", f"Energia fornecida: {session['energia_kwh']} kWh")

    # Atualiza sessão
    session['fim'] = now
    session['status'] = 'finalizada'

    # Atualiza carregador
    if charger:
        charger['status'] = 'livre'
        charger['potencia_atual'] = 0
        charger['energia_fornecida_kwh'] += session['energia_kwh']

    # Atualiza bateria do veículo
    if vehicle:
        ganho_pct = int((session['energia_kwh'] / vehicle['bateria_kwh']) * 100)
        vehicle['nivel_bateria'] = min(100, vehicle['nivel_bateria'] + ganho_pct)

    reset_terminal()
    header("SESSÃO ENCERRADA")
    print(f"\n✅ Sessão #{session['id']} finalizada.")
    print(f"\nEnergia carregada:  {session['energia_kwh']} kWh")
    print(f"Tarifa:             R$ {session['tarifa_kwh']:.2f}/kWh")
    print(f"Valor:              R$ {session['valor']:.2f}")
    if vehicle:
        print(f"\nBateria atual:      {vehicle['nivel_bateria']}%")
    print(f"\n🌿 CO₂ evitado:     {co2_evitado} kg")
    print(f"\nInício:  {session['inicio']}")
    print(f"Fim:     {now}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")