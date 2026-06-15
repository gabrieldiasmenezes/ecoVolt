from database.database import sessions, establishment_chargers
from database.settings import ICON_TYPE
from utils.system import reset_terminal
from utils.ui import footer, header
from utils.ui import error_option
from utils.validation.common_validation import validate_int_value

from utils.helpers import (
    get_list_item_by_status,
    get_user_sessions
)



def calculate_session_stats(user_sessions):
    finalizadas = get_list_item_by_status(user_sessions, "finalizada")
    ativas = get_list_item_by_status(user_sessions, "ativa")

    total_energia = sum(s['energia_kwh'] for s in finalizadas)
    total_gasto = sum(s['valor'] for s in finalizadas)
    co2_total = round(total_energia * 0.233, 2)

    return {
        "finalizadas": finalizadas,
        "ativas": ativas,
        "total_energia": total_energia,
        "total_gasto": total_gasto,
        "co2_total": co2_total
    }


# ==========================
# MENU PRINCIPAL
# ==========================

MENU="""
1 - Ver Sessão Ativa
2 - Ver Sessões Finalizadas
0 - Voltar

Opção: """
def session_history(user):
    while True:
        reset_terminal()
        header("HISTÓRICO DE SESSÕES")

        user_sessions = get_user_sessions(user['id'])
        stats = calculate_session_stats(user_sessions)

        print(f"\nSessões ativas:      {len(stats['ativas'])}")
        print(f"Sessões finalizadas: {len(stats['finalizadas'])}")
        print(f"Energia total:       {stats['total_energia']:.1f} kWh")
        print(f"Gasto total:         R$ {stats['total_gasto']:.2f}")
        print(f"CO₂ evitado:         {stats['co2_total']} kg")

        options = validate_int_value(MENU)

        match options:
            case 1:
                show_active(stats["ativas"])
            case 2:
                show_finished(stats["finalizadas"])
            case 0:
                break
            case _:
                error_option()


# ==========================
# VISUALIZAÇÃO: ATIVA
# ==========================

def show_active(ativas):
    reset_terminal()
    header("SESSÃO ATIVA")

    if not ativas:
        print("\nNenhuma sessão ativa no momento.")
        input("\nAperte Enter para voltar...")
        return

    s = ativas[0]

    charger = next(
        (
            c for c in establishment_chargers
            if c["id"] == s["carregador_id"]
        ),
        None
    )

    tipo = ICON_TYPE['premium'] if s["tipo"] == "premium" else ICON_TYPE["comum"]

    print(f"\nSessão #{s['id']}  {tipo}")
    print(f"Carregador: #{charger['numero'] if charger else s['carregador_id']}")
    print(f"Potência:   {s['potencia_kw']} kW")
    print(f"Tarifa:     R$ {s['tarifa_kwh']:.2f}/kWh")
    print(f"Início:     {s['inicio']}")
    print(f"Status:     EM ANDAMENTO")

    footer()


# ==========================
# VISUALIZAÇÃO: FINALIZADAS
# ==========================

def show_finished(finalizadas):
    reset_terminal()
    header("SESSÕES FINALIZADAS")

    if not finalizadas:
        print("\nNenhuma sessão finalizada encontrada.")
        input("\nAperte Enter para voltar...")
        return

    for i, s in enumerate(finalizadas):
        tipo = "🔶 Premium" if s['tipo'] == 'premium' else "🔷 Comum"
        co2 = round(s['energia_kwh'] * 0.233, 2)

        print(f"\nSessão #{s['id']}  {tipo}")
        print(f"  Energia:  {s['energia_kwh']} kWh")
        print(f"  Valor:    R$ {s['valor']:.2f}")
        print(f"  CO₂:      {co2} kg evitados")
        print(f"  Início:   {s['inicio']}")
        print(f"  Fim:      {s['fim']}")

        if i < len(finalizadas) - 1:
            print("\n" + "-" * 40)

    footer()