from database.database import ocpp_logs
from utils.ui import enter, header


def ocpp_integration(sessions):
    header("INTEGRAÇÃO OCPP (SIMULAÇÃO)")

    print("📡 LOGS DO SISTEMA:\n")

    for log in ocpp_logs:
        print(f"[{log['timestamp']}] Charger {log['carregador_id']}")
        print(f"Tipo: {log['tipo']}")
        print(f"Mensagem: {log['mensagem']}")
        print("-" * 40)

    header("SIMULAÇÃO DE SESSÕES → OCPP PAYLOAD")

    for s in sessions:
        payload = {
            "transactionId": s["id"],
            "userId": s["usuario_id"],
            "chargerId": s["carregador_id"],
            "energy": s["energia_kwh"],
            "status": s["status"]
        }

        print(payload)
        print("-" * 40)

    enter()