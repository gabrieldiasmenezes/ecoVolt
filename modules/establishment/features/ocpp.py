from database.database import ocpp_logs, settings
from database.settings import LINE_SEPARATOR, OCPP_TYPE_ICON
from utils.system import reset_terminal
from utils.ui import footer, header, separator
from datetime import datetime


def format_payload(session):
    return {
        "messageTypeId": 2,
        "uniqueId":      f"req-{session['id']}-{datetime.now().strftime('%H%M%S')}",
        "action":        "MeterValues",
        "payload": {
            "transactionId":  session["id"],
            "connectorId":    session["carregador_id"],
            "idTag":          f"USR-{session['usuario_id']}",
            "meterStart":     0,
            "energyDelivered": session["energia_kwh"],
            "powerNow":       session["potencia_kw"],
            "status":         session["status"].upper(),
            "timestamp":      datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    }


def ocpp_integration(sessions):
    reset_terminal()
    header("INTEGRAÇÃO OCPP")

    ocpp_active = settings.get('ocpp_ativo', False)
    ocpp_version = settings.get('versao_ocpp', '—')
    dlm_active = settings.get('modo_dlm', False)

    print(f"""
  Protocolo:  OCPP {ocpp_version}
  Status:     {"🟢 Ativo" if ocpp_active else "🔴 Inativo"}
  Modo DLM:   {"🟢 Ativo" if dlm_active else "🔴 Inativo"}
  Operadora:  {settings.get('empresa_operadora', '—')}
  {LINE_SEPARATOR}
""")
    
    header("LOGS DO GATEWAY")

    for log in ocpp_logs:
        icon = OCPP_TYPE_ICON.get(log['tipo'], "📋")
        print(f"  {icon} [{log['timestamp']}]  Carregador #{log['carregador_id']}")
        print(f"     Tipo:     {log['tipo']}")
        print(f"     Mensagem: {log['mensagem']}")
        print()

    header("PAYLOADS DAS SESSÕES ATIVAS")

    active = [s for s in sessions if s['status'] == 'ativa']

    if not active:
        print("  Nenhuma sessão ativa no momento.")
    else:
        for s in active:
            payload = format_payload(s)
            print(f"  Sessão #{s['id']} → Carregador #{s['carregador_id']}")
            print(f"  {LINE_SEPARATOR}")
            for key, value in payload['payload'].items():
                print(f"  {key:<20} {value}")
            print()

    separator()
    print(f"  Total de logs:     {len(ocpp_logs)}")
    print(f"  Sessões enviadas:  {len(active)}")
    footer()