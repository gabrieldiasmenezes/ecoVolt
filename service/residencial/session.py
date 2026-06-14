from datetime import datetime
from database.database import sessions, fares
from utils.helpers import get_user_active_session, get_user_charger, get_user_vehicle
from utils.system import reset_terminal
from utils.ui import header, error_option
from utils.validate.mutual_data import validate_option

KWH_PER_100KM = 15
DLM_CIRCUIT_BREAKER_LIMIT_KW = 5.0

CHARGE_MODES = {
    1: {
        "nome": "Prioridade Solar (Eco) ☀",
        "descricao": "Carrega apenas com excedente solar — custo zero",
        "potencia_kw": 3.5,
        "tarifa_override": 0.0
    },
    2: {
        "nome": "FV + Bateria 🔋",
        "descricao": "Solar + bateria da casa — evita rede elétrica",
        "potencia_kw": 5.0,
        "tarifa_override": fares['cortesia_solar']
    },
    3: {
        "nome": "Carga Rápida (Fast) ⚡",
        "descricao": "Potência máxima — rede + solar + bateria",
        "potencia_kw": 7.0,
        "tarifa_override": None   
    }
}



def choose_soc_target(vehicle):
    """Escolha do SOC alvo com validação (mínimo 10% acima do atual, máximo 100%)."""
    current = vehicle['nivel_bateria']
    min_target = current + 10

    print(f"\nBateria atual:    {current}%")
    print(f"Mínimo permitido: {min_target}%")
    print(f"Máximo:           100%\n")

    while True:
        try:
            target = int(input(f"Meta de carga (SOC) [{min_target}–100]%: ").strip())
            if target < min_target:
                print(f"Mínimo {min_target}% (10% acima do atual).")
                continue
            if target > 100:
                print("Não pode ultrapassar 100%.")
                continue
            return target
        except ValueError:
            print("Digite apenas números inteiros.")


def residential_session(user, action):
    if action == 'iniciar':
        start_residential_session(user)
    elif action == 'encerrar':
        end_residential_session(user)


def start_residential_session(user):
    reset_terminal()
    header("INICIAR RECARGA RESIDENCIAL")

    active = get_user_active_session(user)
    if active:
        print(f"\nSessão #{active['id']} já está ativa.")
        print("Encerre-a antes de iniciar uma nova.")
        input("\nAperte Enter para voltar...")
        return

    charger = get_user_charger(user)
    if not charger:
        print("\nNenhum carregador residencial encontrado.")
        input("\nAperte Enter para voltar...")
        return

    if charger['status'] == 'em_uso':
        print("\nO carregador já está em uso.")
        input("\nAperte Enter para voltar...")
        return

    vehicle = get_user_vehicle(user)
    if not vehicle:
        print("\nNenhum veículo cadastrado.")
        input("\nAperte Enter para voltar...")
        return

    # Escolha do modo de carga
    reset_terminal()
    header("MODO DE CARGA")
    print()
    for key, mode in CHARGE_MODES.items():
        print(f"  [{key}] {mode['nome']}")
        print(f"       {mode['descricao']}")
        print(f"       Potência: {mode['potencia_kw']} kW")
        print()

    mode_option = validate_option("Escolha o modo (0 para voltar): ")
    if mode_option == 0:
        return
    if mode_option not in CHARGE_MODES:
        error_option()
        return

    chosen_mode = CHARGE_MODES[mode_option]
    power_kw = chosen_mode['potencia_kw']

    # DLM — verifica disjuntor
    if power_kw > DLM_CIRCUIT_BREAKER_LIMIT_KW:
        power_kw = DLM_CIRCUIT_BREAKER_LIMIT_KW
        print(f"\n⚠  DLM: Potência limitada a {power_kw} kW pelo disjuntor.")

    # Meta de SOC
    reset_terminal()
    header("META DE CARGA (SOC)")
    soc_target = choose_soc_target(vehicle)

    kwh_to_charge = round((soc_target - vehicle['nivel_bateria']) / 100 * vehicle['bateria_kwh'], 2)
    minutes = round(kwh_to_charge / power_kw * 60)

    # Tarifa
    hora = datetime.now().hour
    is_peak = fares['inicio_horario_pico'] <= hora < fares['fim_horario_pico']
    is_off_peak = hora >= 22 or hora < 6  # madrugada

    if chosen_mode['tarifa_override'] is not None:
        tarifa = chosen_mode['tarifa_override']
        motivo_tarifa = chosen_mode['nome']
    elif is_off_peak:
        tarifa = round(fares['base'] * 0.7, 2)  # 30% desconto madrugada
        motivo_tarifa = "Tarifa reduzida (madrugada)"
    elif is_peak:
        tarifa = fares['horario_pico']
        motivo_tarifa = "Horário de pico"
    else:
        tarifa = fares['base']
        motivo_tarifa = "Tarifa base"

    total_price = round(kwh_to_charge * tarifa, 2)

    # Resumo
    reset_terminal()
    header("RESUMO DA RECARGA")
    print(f"\nModo:             {chosen_mode['nome']}")
    print(f"Potência:         {power_kw} kW")
    print(f"Bateria:          {vehicle['nivel_bateria']}% → {soc_target}%")
    print(f"Energia:          {kwh_to_charge} kWh")
    print(f"Tempo estimado:   ~{minutes} min")
    print(f"Tarifa:           R$ {tarifa:.2f}/kWh  ({motivo_tarifa})")
    print(f"Custo estimado:   R$ {total_price:.2f}")

    if is_off_peak:
        print("\n🌙 Tarifa de madrugada ativa — 30% de desconto!")
    if chosen_mode['tarifa_override'] == 0.0:
        print("\n☀  Modo solar — sem custo de energia!")

    print("\n" + "=" * 40)
    confirm = validate_option("\n1 - Confirmar\n0 - Cancelar\n\nOpção: ")
    if confirm != 1:
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_session = {
        "id": max(s['id'] for s in sessions) + 1,
        "usuario_id": user['id'],
        "veiculo_id": vehicle['id'],
        "carregador_id": charger['id'],
        "tipo": "residencial",
        "potencia_kw": power_kw,
        "energia_kwh": kwh_to_charge,
        "tarifa_kwh": tarifa,
        "valor": total_price,
        "soc_alvo": soc_target,
        "modo": chosen_mode['nome'],
        "inicio": now,
        "fim": None,
        "status": "ativa"
    }

    sessions.append(new_session)
    charger['status'] = 'em_uso'
    charger['potencia_atual'] = power_kw

    reset_terminal()
    header("RECARGA INICIADA")
    print(f"\n✅ Sessão #{new_session['id']} iniciada!")
    print(f"\nModo:           {chosen_mode['nome']}")
    print(f"Meta (SOC):     {soc_target}%")
    print(f"Tempo estimado: ~{minutes} min")
    print(f"Custo:          R$ {total_price:.2f}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")


def end_residential_session(user):
    reset_terminal()
    header("ENCERRAR RECARGA RESIDENCIAL")

    session = get_user_active_session(user)
    if not session:
        print("\nNenhuma sessão ativa encontrada.")
        input("\nAperte Enter para voltar...")
        return

    charger = get_user_charger(user)
    vehicle = get_user_vehicle(user)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    co2_avoided = round(session['energia_kwh'] * 0.233, 2)

    session['fim'] = now
    session['status'] = 'finalizada'

    if charger:
        charger['status'] = 'livre'
        charger['potencia_atual'] = 0
        charger['total_sessoes'] += 1
        charger['energia_fornecida_kwh'] += session['energia_kwh']

    if vehicle:
        ganho_pct = int((session['energia_kwh'] / vehicle['bateria_kwh']) * 100)
        vehicle['nivel_bateria'] = min(100, vehicle['nivel_bateria'] + ganho_pct)

    reset_terminal()
    header("SESSÃO ENCERRADA")
    print(f"\n✅ Sessão #{session['id']} finalizada.")
    print(f"\nModo:              {session.get('modo', 'Residencial')}")
    print(f"Energia carregada: {session['energia_kwh']} kWh")
    print(f"Tarifa:            R$ {session['tarifa_kwh']:.2f}/kWh")
    print(f"Custo:             R$ {session['valor']:.2f}")
    if vehicle:
        print(f"\nBateria atual:     {vehicle['nivel_bateria']}%")
    print(f"\n🌿 CO₂ evitado:    {co2_avoided} kg")
    print(f"\nInício: {session['inicio']}")
    print(f"Fim:    {now}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")