from utils.ui import header

def most_operational_dashboard(establishment, chargers, sessions):

    def count_chargers(status):
        return sum(
            1 for charger in chargers
            if charger["status"] == status
        )

    sessoes_ativas = sum(
        1 for session in sessions
        if session["status"] == "ativa"
    )

    potencia_em_uso = sum(
        charger["potencia_atual"]
        for charger in chargers
    )

    demanda_maxima = establishment["demanda_maxima_kw"]

    potencia_disponivel = (
        demanda_maxima - potencia_em_uso
    )

    utilizacao = (
        potencia_em_uso / demanda_maxima
    ) * 100

    header("DASHBOARD OPERACIONAL")

    print(f"""
Estabelecimento:
{establishment['nome']}

Empresa:
{establishment['empresa_responsavel']}

Status:
{establishment['status']}

========================================
CARREGADORES
========================================

Total:
{len(chargers)}

Em Uso:
{count_chargers('em_uso')}

Livres:
{count_chargers('livre')}

Manutenção:
{count_chargers('manutencao')}

========================================
SESSÕES DE RECARGA
========================================

Sessões Ativas:
{sessoes_ativas}

========================================
CONTROLE DE DEMANDA
========================================

Demanda Contratada:
{demanda_maxima} kW

Potência em Uso:
{potencia_em_uso} kW

Potência Disponível:
{potencia_disponivel} kW

Utilização da Rede:
{utilizacao:.1f}%

========================================
RESULTADOS OPERACIONAIS
========================================

Energia Distribuída:
{establishment['energia_total_distribuida_kwh']} kWh

Faturamento Acumulado:
R$ {establishment['faturamento']:.2f}

========================================
ENERGIA SOLAR
========================================

Sistema Fotovoltaico:
{"ATIVO" if establishment["possui_energia_solar"] else "INATIVO"}

========================================
""")