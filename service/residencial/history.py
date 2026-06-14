from database.database import sessions
from utils.system import reset_terminal
from utils.ui import header

KWH_PER_100KM = 15
PRICE_GASOLINE_PER_LITER = 6.20
KM_PER_LITER = 12


def residential_history(user):
    reset_terminal()
    header("HISTÓRICO DE CONSUMO")

    user_sessions = [s for s in sessions if s['usuario_id'] == user['id']]
    finalizadas = [s for s in user_sessions if s['status'] == 'finalizada']
    ativas = [s for s in user_sessions if s['status'] == 'ativa']

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
        input("\nAperte Enter para voltar...")
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
            print("\n" + "-" * 40 + "\n")

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")