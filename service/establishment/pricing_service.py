from utils.ui import enter,header


def pricing_service(sessions):
    header("TARIFAÇÃO E FATURAMENTO")

    total = 0

    for s in sessions:
        print(f"Session ID: {s['id']}")
        print(f"Tipo: {s['tipo']}")
        print(f"Energia: {s['energia_kwh']} kWh")
        print(f"Tarifa: R$ {s['tarifa_kwh']}")

        valor = s['energia_kwh'] * s['tarifa_kwh']
        total += valor

        print(f"Valor calculado: R$ {valor:.2f}")
        print("-" * 30)

    print(f"\n💵 FATURAMENTO TOTAL: R$ {total:.2f}")

    enter()