from utils.helpers import get_list_item_by_status
from utils.ui import header

def count_chargers(status, chargers):
    return len(get_list_item_by_status(chargers,status))

def get_dashboard_data(establishment, chargers, sessions):
    active_sessions = len(get_list_item_by_status(sessions,'ativa'))

    power_in_use = sum(
        charger.get("potencia_atual", 0)
        for charger in chargers
    )

    max_demand = establishment.get("demanda_maxima_kw", 0)

    available_power = max_demand - power_in_use

    network_usage = (
        (power_in_use / max_demand) * 100
        if max_demand > 0 else 0
    )

    return {
        "active_sessions": active_sessions,
        "max_demand": max_demand,
        "power_in_use": power_in_use,
        "available_power": available_power,
        "network_usage": network_usage,
    }


def operational_dashboard(establishment, chargers, sessions):

    data = get_dashboard_data(establishment, chargers, sessions)

    header("DASHBOARD OPERACIONAL")

    print(f"""
================ ESTABELECIMENTO ================
Nome: {establishment.get('nome')}
Empresa: {establishment.get('empresa_responsavel')}
Status: {establishment.get('status')}

================ CARREGADORES ====================
Total: {len(chargers)}
Em uso: {count_chargers('em_uso', chargers)}
Livres: {count_chargers('livre', chargers)}
Manutenção: {count_chargers('manutencao', chargers)}

================ SESSÕES ========================
Sessões ativas: {data['active_sessions']}

================ DEMANDA ========================
Demanda contratada: {data['max_demand']} kW
Potência em uso: {data['power_in_use']} kW
Potência disponível: {data['available_power']} kW
Utilização da rede: {data['network_usage']:.1f}%

================ RESULTADOS =====================
Energia distribuída: {establishment.get('energia_total_distribuida_kwh', 0)} kWh
Faturamento acumulado: R$ {establishment.get('faturamento', 0.0):.2f}

================ ENERGIA SOLAR ==================
Sistema fotovoltaico: {"ATIVO" if establishment.get("possui_energia_solar") else "INATIVO"}

========================================
    """)