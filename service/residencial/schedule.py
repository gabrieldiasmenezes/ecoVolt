from utils.system import reset_terminal
from utils.ui import header, error_option
from database.database import fares
from utils.validate.mutual_data import validate_option

scheduled_sessions = []  # agendamentos em memória

OFF_PEAK_WINDOWS = [
    {"janela": "22h – 00h", "desconto": "30%", "hora_inicio": 22},
    {"janela": "00h – 06h", "desconto": "35%", "hora_inicio": 0},
]


def schedule_service(user):
    while True:
        reset_terminal()
        header("AGENDAMENTO INTELIGENTE")

        user_schedules = [s for s in scheduled_sessions if s['usuario_id'] == user['id']]

        print(f"\nAgendamentos ativos: {len(user_schedules)}")
        if user_schedules:
            print()
            for s in user_schedules:
                print(f"  #{s['id']} — {s['janela']}  |  Meta: {s['soc_alvo']}%  |  Tarifa: R$ {s['tarifa']:.2f}/kWh")

        options = validate_option("""
1 - Novo Agendamento
2 - Cancelar Agendamento
0 - Voltar

Opção: """)

        match options:
            case 1:
                new_schedule(user)
            case 2:
                cancel_schedule(user)
            case 0:
                break
            case _:
                error_option()


def new_schedule(user):
    reset_terminal()
    header("NOVO AGENDAMENTO")

    print("\nJanelas de tarifa reduzida disponíveis:\n")
    for i, w in enumerate(OFF_PEAK_WINDOWS):
        tarifa_desc = round(fares['base'] * (1 - int(w['desconto'].replace('%', '')) / 100), 2)
        print(f"  [{i+1}] {w['janela']}  —  {w['desconto']} desconto  →  R$ {tarifa_desc:.2f}/kWh")

    option = validate_option("\nEscolha a janela (0 para voltar): ")
    if option == 0:
        return
    if option < 1 or option > len(OFF_PEAK_WINDOWS):
        error_option()
        return

    chosen_window = OFF_PEAK_WINDOWS[option - 1]
    discount_pct = int(chosen_window['desconto'].replace('%', ''))
    tarifa = round(fares['base'] * (1 - discount_pct / 100), 2)

    while True:
        try:
            soc_target = int(input("\nMeta de carga (SOC) [10–100]%: ").strip())
            if 10 <= soc_target <= 100:
                break
            print("Informe um valor entre 10 e 100.")
        except ValueError:
            print("Digite apenas números.")

    new_id = max((s['id'] for s in scheduled_sessions), default=0) + 1
    scheduled_sessions.append({
        "id": new_id,
        "usuario_id": user['id'],
        "janela": chosen_window['janela'],
        "hora_inicio": chosen_window['hora_inicio'],
        "soc_alvo": soc_target,
        "tarifa": tarifa,
        "desconto": chosen_window['desconto']
    })

    reset_terminal()
    header("AGENDAMENTO CONFIRMADO")
    print(f"\n✅ Agendamento #{new_id} criado!")
    print(f"\nJanela:  {chosen_window['janela']}")
    print(f"Meta:    {soc_target}%")
    print(f"Tarifa:  R$ {tarifa:.2f}/kWh  ({chosen_window['desconto']} desconto)")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")


def cancel_schedule(user):
    reset_terminal()
    header("CANCELAR AGENDAMENTO")

    user_schedules = [s for s in scheduled_sessions if s['usuario_id'] == user['id']]
    if not user_schedules:
        print("\nNenhum agendamento encontrado.")
        input("\nAperte Enter para voltar...")
        return

    for s in user_schedules:
        print(f"  [{s['id']}] {s['janela']}  |  Meta: {s['soc_alvo']}%")

    try:
        schedule_id = int(input("\nDigite o ID para cancelar (0 para voltar): ").strip())
    except ValueError:
        return

    if schedule_id == 0:
        return

    target = next((s for s in scheduled_sessions if s['id'] == schedule_id and s['usuario_id'] == user['id']), None)
    if not target:
        print("\nAgendamento não encontrado.")
        input("\nAperte Enter para voltar...")
        return

    scheduled_sessions.remove(target)
    print(f"\n✅ Agendamento #{schedule_id} cancelado.")
    input("\nAperte Enter para voltar...")