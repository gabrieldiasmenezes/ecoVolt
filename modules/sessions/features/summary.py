from utils.helpers import get_list_item_by_status
from utils.ui import header, separator


def sum_values(items, content):
    return sum(i.get(content, 0) for i in items if isinstance(i, dict))


def session_summary(sessions):
    active = get_list_item_by_status(sessions, 'ativa')
    finished = get_list_item_by_status(sessions, 'finalizada')
    energy_in_use = sum_values(active, 'potencia_kw')
    revenue = sum_values(sessions, 'valor')

    header("CENTRO DE SESSÕES")
    print(f"\nSessões Ativas:      {len(active)}")
    print(f"Sessões Finalizadas: {len(finished)}")
    print(f"\nEnergia em Uso:      {energy_in_use} kW")
    print(f"Receita Gerada:      R$ {revenue:.2f}")
    separator()