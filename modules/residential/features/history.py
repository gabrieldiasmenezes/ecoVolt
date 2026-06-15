from database.database import sessions
from database.settings import LINE_SEPARATOR
from utils.helpers import get_list_item_by_status, get_user_active_session, get_user_sessions
from utils.system import reset_terminal
from utils.ui import enter, footer, header

KWH_PER_100KM = 15
PRICE_GASOLINE_PER_LITER = 6.20
KM_PER_LITER = 12


def residential_history(user):
    reset_terminal()
    header("HISTÓRICO DE CONSUMO")

    user_sessions = get_user_sessions(user['id'])
    finalizadas = get_list_item_by_status(user_sessions,'finalizada')
    ativas = get_list_item_by_status(user_sessions,'ativa')

    total_kwh = sum(s['energia_kwh'] for s in finalizadas)
    total_gasto = sum(s['valor'] for s in finalizadas)
    total_km = round(total_kwh / KWH_PER_100KM * 100)
    co2_total = round(total_kwh * 0.233, 2)

    print(f"\n--- Resumo Geral ---")
    print(f"Sessões realizadas:  {len(finalizadas)}")
    print(f"Sessões ativas:      {len(ativas)}")
    print(f"Energia total:       {total_kwh:.1f} kWh")
    print(f"Km equivalentes:     ~{total_km} km")
    print(f"Gasto total:         R$ {total_gasto:.2f}")
    print(f"🌿 CO₂ evitado:      {co2_total} kg")

    if not finalizadas:
        print("\nNenhuma sessão finalizada ainda.")
        enter()
        return

    print(f"\n--- Sessões ---\n")
    for i, s in enumerate(finalizadas):
        modo = s.get('modo', 'Residencial')
        co2 = round(s['energia_kwh'] * 0.233, 2)
        print(f"Sessão #{s['id']}  [{modo}]")
        print(f"  Energia:  {s['energia_kwh']} kWh")
        print(f"  Tarifa:   R$ {s['tarifa_kwh']:.2f}/kWh")
        print(f"  Custo:    R$ {s['valor']:.2f}")
        print(f"  CO₂:      {co2} kg evitados")
        print(f"  Início:   {s['inicio']}")
        print(f"  Fim:      {s['fim']}")
        if i < len(finalizadas) - 1:
            print(LINE_SEPARATOR)

    footer()