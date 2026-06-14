from utils.ui import enter, header


def chargers_service(chargers):
    header("CARREGADORES")

    for c in chargers:
        print(f"ID: {c['id']}")
        print(f"Número: {c['numero']}")
        print(f"Modelo: {c['modelo']}")
        print(f"Status: {c['status']}")
        print(f"Potência máxima: {c['potencia_maxima']} kW")
        print(f"Potência atual: {c['potencia_atual']} kW")
        print(f"Sessões totais: {c['total_sessoes']}")
        print(f"Energia fornecida: {c['energia_fornecida_kwh']} kWh")
        print("-" * 40)

    enter()