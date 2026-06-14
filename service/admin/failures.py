from database.database import establishment_chargers, residencial_charger, ocpp_logs, sessions
from utils.system import reset_terminal
from utils.ui import header

CRITICAL_POWER_THRESHOLD = 0   # carregador em uso mas com potência zero = anomalia


def failure_monitor():
    reset_terminal()
    header("MONITOR DE FALHAS CRÍTICAS")

    all_chargers = establishment_chargers + residencial_charger
    failures = []
    warnings = []

    for c in all_chargers:
        # Falha crítica: em manutenção
        if c['status'] == 'manutencao':
            failures.append({
                "id": c['id'],
                "modelo": c['modelo'],
                "tipo": "FALHA",
                "motivo": "Carregador em manutenção",
                "acao": "Acionar equipe técnica"
            })

        # Anomalia: em_uso mas potência zero
        if c['status'] == 'em_uso' and c['potencia_atual'] == CRITICAL_POWER_THRESHOLD:
            warnings.append({
                "id": c['id'],
                "modelo": c['modelo'],
                "tipo": "AVISO",
                "motivo": "Em uso mas sem potência registrada",
                "acao": "Verificar telemetria OCPP"
            })

    # Anomalia em sessões: ativas sem fim mas com valor zero
    for s in sessions:
        if s['status'] == 'ativa' and s['valor'] == 0:
            warnings.append({
                "id": s['id'],
                "modelo": f"Sessão #{s['id']}",
                "tipo": "AVISO",
                "motivo": "Sessão ativa com valor zerado",
                "acao": "Verificar faturamento"
            })

    print(f"\nFalhas críticas: {len(failures)}")
    print(f"Avisos:          {len(warnings)}")

    if not failures and not warnings:
        print("\n✅ Nenhuma falha detectada. Rede operando normalmente.")
        input("\nAperte Enter para voltar...")
        return

    if failures:
        print(f"\n{'='*40}")
        print("  ❌ FALHAS CRÍTICAS")
        print(f"{'='*40}")
        for f in failures:
            print(f"\n  ID #{f['id']} — {f['modelo']}")
            print(f"  Tipo:   {f['tipo']}")
            print(f"  Motivo: {f['motivo']}")
            print(f"  Ação:   {f['acao']}")

    if warnings:
        print(f"\n{'='*40}")
        print("  ⚠  AVISOS")
        print(f"{'='*40}")
        for w in warnings:
            print(f"\n  ID #{w['id']} — {w['modelo']}")
            print(f"  Tipo:   {w['tipo']}")
            print(f"  Motivo: {w['motivo']}")
            print(f"  Ação:   {w['acao']}")

    # Últimos logs OCPP relevantes
    header("ÚLTIMOS LOGS OCPP")

    for log in ocpp_logs[-5:]:
        print(f"\n  [{log['timestamp']}] Carregador #{log['carregador_id']}")
        print(f"  {log['tipo']}: {log['mensagem']}")

    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")