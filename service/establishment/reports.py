
from database.database import users
from utils.ui import enter, header


def reports(sessions):
    header("RELATÓRIOS DO SISTEMA CHARGEGGRID")

    total_kwh = sum(s['energia_kwh'] for s in sessions)
    total_revenue = sum(s['energia_kwh'] * s['tarifa_kwh'] for s in sessions)

    active_sessions = len([s for s in sessions if s['status'] == "ativa"])
    finished_sessions = len([s for s in sessions if s['status'] == "finalizada"])

    print(f"⚡ Energia total consumida: {total_kwh} kWh")
    print(f"💰 Faturamento total: R$ {total_revenue:.2f}")
    print(f"🔋 Sessões ativas: {active_sessions}")
    print(f"✔ Sessões finalizadas: {finished_sessions}")

    # ESG simples
    co2 = total_kwh * 0.12
    print(f"CO₂ evitado: {co2:.2f} kg")

    # ranking simples de usuários
    print("Top usuários por consumo:")

    ranking = sorted(users, key=lambda u: u.get("energia_consumida_kwh", 0), reverse=True)

    for u in ranking[:3]:
        print(f"- {u['nome']} → {u.get('energia_consumida_kwh', 0)} kWh")

    enter()