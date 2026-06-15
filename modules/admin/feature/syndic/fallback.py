def syndic_fallback(question, ctx):
    q = question.lower()

    if any(w in q for w in ["saúde", "status", "rede", "geral"]):
        manut = ctx['em_manutencao']
        total = ctx['total_carregadores']
        taxa = round((total - manut) / total * 100, 1) if total else 0
        return (
            f"Saúde da rede: {taxa}% de disponibilidade.\n"
            f"{ctx['em_uso']} carregadores em uso, {manut} em manutenção.\n"
            f"Sessões ativas: {ctx['sessoes_ativas']}.\n"
            f"Recomendação: {'Rede estável.' if taxa >= 75 else 'Verificar carregadores em manutenção com urgência.'}"
        )

    if any(w in q for w in ["faturamento", "receita", "financeiro"]):
        return (
            f"Faturamento total da rede: R$ {ctx['faturamento_total']:.2f}.\n"
            f"Energia distribuída: {ctx['energia_total_kwh']:.1f} kWh.\n"
            f"Tarifa base atual: R$ {ctx['tarifas']['base']:.2f}/kWh.\n"
            f"Recomendação: Avaliar ajuste de tarifa no horário de pico."
        )

    if any(w in q for w in ["falha", "problema", "erro", "manutenção"]):
        manut = ctx['em_manutencao']
        return (
            f"{manut} carregador(es) em manutenção.\n"
            f"Últimos logs OCPP: {len(ctx['ultimos_logs_ocpp'])} eventos.\n"
            f"Recomendação: Acionar equipe técnica imediatamente."
        )

    return (
        f"Rede com {ctx['total_carregadores']} carregadores, "
        f"{ctx['sessoes_ativas']} sessões ativas, "
        f"faturamento de R$ {ctx['faturamento_total']:.2f}."
    )