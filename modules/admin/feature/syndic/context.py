from database.database import (
    establishments, establishment_chargers, residencial_charger,
    sessions, users, fares, ocpp_logs
)


def build_network_context():
    all_chargers = establishment_chargers + residencial_charger
    active_sessions = [s for s in sessions if s['status'] == 'ativa']
    finished_sessions = [s for s in sessions if s['status'] == 'finalizada']

    return {
        "total_carregadores": len(all_chargers),
        "em_manutencao": len([c for c in all_chargers if c['status'] == 'manutencao']),
        "em_uso": len([c for c in all_chargers if c['status'] == 'em_uso']),
        "sessoes_ativas": len(active_sessions),
        "sessoes_finalizadas": len(finished_sessions),
        "potencia_total_kw": sum(s['potencia_kw'] for s in active_sessions),
        "energia_total_kwh": sum(s['energia_kwh'] for s in sessions),
        "faturamento_total": round(sum(s['valor'] for s in sessions), 2),
        "tarifas": fares,
        "total_usuarios": len(users),
        "estabelecimentos": [
            {
                "nome": e['nome'],
                "faturamento": e['faturamento'],
                "energia_distribuida_kwh": e['energia_total_distribuida_kwh']
            }
            for e in establishments
        ],
        "ultimos_logs_ocpp": [
            {"tipo": l['tipo'], "mensagem": l['mensagem'], "timestamp": l['timestamp']}
            for l in ocpp_logs[-5:]
        ]
    }