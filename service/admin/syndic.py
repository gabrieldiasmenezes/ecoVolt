import json
from database.database import (
    establishments, establishment_chargers, residencial_charger,
    sessions, users, fares, ocpp_logs
)
from utils.system import reset_terminal, load
from utils.ui import header
from utils.validate.mutual_data import validate_option



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


def call_syndic_api(user_question, network_context):
    try:
        import urllib.request

        context_str = json.dumps(network_context, ensure_ascii=False, indent=2)

        system_prompt = (
            "Você é o Síndico Virtual da GoodWe, um assistente de IA especializado em gestão "
            "de infraestrutura de carregadores elétricos. Sua função é traduzir dados técnicos "
            "complexos em relatórios gerenciais simples e claros para o Administrador Master. "
            "Responda sempre em português, de forma objetiva e estruturada. "
            "Ao identificar problemas, sugira ações concretas. "
            "Ao analisar dados financeiros, destaque oportunidades de melhoria. "
            f"\n\nDados atuais da rede:\n{context_str}"
        )

        payload = json.dumps({
            "model": "claude-sonnet-4-6",
            "max_tokens": 1000,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]

    except Exception:
        # Fallback sem API
        return _syndic_fallback(user_question, network_context)


def _syndic_fallback(question, ctx):
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
            f"Recomendação: Avaliar ajuste de tarifa no horário de pico para maximizar receita."
        )
    if any(w in q for w in ["falha", "problema", "erro", "manutenção"]):
        manut = ctx['em_manutencao']
        return (
            f"{manut} carregador(es) em manutenção detectado(s).\n"
            f"Últimos logs OCPP registrados: {len(ctx['ultimos_logs_ocpp'])} eventos.\n"
            f"Recomendação: Acionar equipe técnica imediatamente para os dispositivos offline."
        )

    return (
        f"Rede com {ctx['total_carregadores']} carregadores, "
        f"{ctx['sessoes_ativas']} sessões ativas, "
        f"faturamento de R$ {ctx['faturamento_total']:.2f}. "
        f"Para análises específicas, pergunte sobre saúde da rede, faturamento ou falhas."
    )


def virtual_syndic():
    network_context = build_network_context()

    print("\n")
    reset_terminal()
    header("SÍNDICO VIRTUAL — IA GOODWE")

    print("\nO Síndico Virtual analisa os dados da rede e responde")
    print("perguntas gerenciais em linguagem simples.\n")
    print("Exemplos:")
    print("  • Como está a saúde da rede?")
    print("  • Qual o faturamento atual?")
    print("  • Há falhas críticas?")
    print("  • O que otimizar na tarifação?\n")
    print("=" * 40)

    while True:
        print()
        question = input("Sua pergunta (ou 'sair'): ").strip()

        if not question or question.lower() == 'sair':
            break

        load("\nSíndico Virtual analisando")
        response = call_syndic_api(question, network_context)

        print(f"\n{'='*40}")
        print("SÍNDICO VIRTUAL:")
        print(f"{'='*40}")
        print(f"\n{response}")
        print(f"\n{'='*40}")

        again = validate_option("\n1 - Nova pergunta\n0 - Voltar\n\nOpção: ")
        if again != 1:
            break