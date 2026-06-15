from datetime import datetime
from database.database import ocpp_logs, settings


def register_ocpp_event(charger_id, event_type, message):
    if not settings.get('ocpp_ativo'):
        return
    new_log = {
        "id": max(log['id'] for log in ocpp_logs) + 1 if ocpp_logs else 1,
        "carregador_id": charger_id,
        "tipo": event_type,
        "mensagem": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ocpp_logs.append(new_log)
    print(f"  [OCPP] {event_type} → {message}")