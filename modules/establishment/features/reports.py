from database.database import users, fares
import database.settings as st
from utils.system import reset_terminal
from utils.ui import footer, header, separator, progress_bar




def get_session_stats(sessions):
    return {
        "total_kwh":          sum(s['energia_kwh'] for s in sessions),
        "total_revenue":      sum(s['energia_kwh'] * s['tarifa_kwh'] for s in sessions),
        "active":             [s for s in sessions if s['status'] == 'ativa'],
        "finished":           [s for s in sessions if s['status'] == 'finalizada'],
        "premium_sessions":   [s for s in sessions if s['tipo'] == 'premium'],
        "common_sessions":    [s for s in sessions if s['tipo'] == 'comum'],
    }


def reports(establishment, sessions):
    reset_terminal()
    header("RELATÓRIOS — CHARGEGRID")

    stats = get_session_stats(sessions)

    total_kwh     = stats['total_kwh']
    total_revenue = stats['total_revenue']
    royalty       = round(total_revenue * st.ROYALTY_RATE, 2)
    co2_avoided   = round(total_kwh * st.CO2_FACTOR, 2)
    peak_revenue  = sum(
        s['energia_kwh'] * s['tarifa_kwh']
        for s in sessions
        if s['tarifa_kwh'] == fares['horario_pico']
    )

    # Operacional
    print(f"""
  {st.LINE_SEPARATOR}
  OPERACIONAL
  {st.LINE_SEPARATOR}
  Sessões ativas:      {len(stats['active'])}
  Sessões finalizadas: {len(stats['finished'])}
  Sessões premium:     {len(stats['premium_sessions'])}
  Sessões comuns:      {len(stats['common_sessions'])}
""")

    bar, pct = progress_bar(len(stats['active']), len(sessions))
    print(f"  Ocupação atual: [{bar}] {pct}%")

    # Financeiro
    print(f"""
  {st.LINE_SEPARATOR}
  FINANCEIRO
  {st.LINE_SEPARATOR}
  Energia distribuída:   {total_kwh:.1f} kWh
  Faturamento total:     R$ {total_revenue:.2f}
  Receita horário pico:  R$ {peak_revenue:.2f}
  Royalty GoodWe (10%):  R$ {royalty:.2f}
  Faturamento líquido:   R$ {round(total_revenue - royalty, 2):.2f}

  Tarifa média:          R$ {round(total_revenue / total_kwh, 2) if total_kwh > 0 else 0:.2f}/kWh
""")

    # ESG
    print(f"""  {st.LINE_SEPARATOR}
  ESG — IMPACTO AMBIENTAL
  {st.LINE_SEPARATOR}
  CO₂ evitado:           {co2_avoided} kg
  Equiv. árvores/mês:    ~{round(co2_avoided / 10, 1)} árvores
  Energia limpa usada:   {"Sim ☀" if establishment.get('possui_energia_solar') else "Não"}
""")

    # Ranking usuários
    header("TOP 3 — USUÁRIOS POR CONSUMO")

    ranking = sorted(
        [u for u in users if u.get('energia_consumida_kwh')],
        key=lambda u: u.get('energia_consumida_kwh', 0),
        reverse=True
    )

    medals = ["🥇", "🥈", "🥉"]
    for i, u in enumerate(ranking[:3]):
        print(f"  {medals[i]} {u['nome']:<20} {u['energia_consumida_kwh']} kWh")

    # Sessões detalhadas
    header("DETALHAMENTO POR SESSÃO")

    for s in sessions:
        tipo_label   = st.ICON_TYPE.get(s['tipo'], s['tipo'].upper())
        status_label = st.SESSION_STATUS.get(s['status'], s['status'].upper())
        valor        = round(s['energia_kwh'] * s['tarifa_kwh'], 2)

        print(f"  Sessão #{s['id']}  {tipo_label}  {status_label}")
        print(f"  Energia: {s['energia_kwh']} kWh  |  Tarifa: R$ {s['tarifa_kwh']:.2f}  |  Valor: R$ {valor:.2f}")
        print()

    separator()
    print(f"  💰 Faturamento total:   R$ {total_revenue:.2f}")
    print(f"  ⚡ Energia total:       {total_kwh:.1f} kWh")
    print(f"  🌿 CO₂ evitado:        {co2_avoided} kg")
    footer()