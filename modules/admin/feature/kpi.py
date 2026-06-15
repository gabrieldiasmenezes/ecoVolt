from database.database import establishments, establishment_chargers, residencial_charger, sessions, users
from utils.helpers import get_list_item_by_status,find_list_item_by_field
from utils.system import reset_terminal
from utils.ui import footer, header, progress_bar


def kpis_dashboard():
    reset_terminal()
    header("KPIs — DISPONIBILIDADE DA REDE")

    # Carregadores
    all_chargers = establishment_chargers + residencial_charger
    total = len(all_chargers)
    online = len([c for c in all_chargers if c['status'] != 'manutencao'])
    in_use = len(get_list_item_by_status(all_chargers,'em_uso'))
    free = len(get_list_item_by_status(all_chargers,'livre'))
    maintenance = len(get_list_item_by_status(all_chargers,'manutencao'))

    # Sessões
    active_sessions = get_list_item_by_status(sessions,'ativa')
    finished_sessions = get_list_item_by_status(sessions,'finalizada')
    total_revenue = sum(s['valor'] for s in sessions)
    total_energy = sum(s['energia_kwh'] for s in sessions)
    total_power_now = sum(s['potencia_kw'] for s in active_sessions)

    # Usuários
    active_users = len(get_list_item_by_status(users,'ativo'))
    commercial_users = len(find_list_item_by_field(users,'cliente_comercial','perfil'))
    residential_users = len(find_list_item_by_field(users,'cliente_residencial','perfil'))


    header("SAÚDE DA FROTA")
    bar, percentage = progress_bar(online, total, width=20)
    health = "✅ BOA" if percentage >= 75 else "⚠ AVISO" if percentage >= 50 else "❌ CRÍTICA"

    print(f"\nDisponibilidade:  [{bar}] {percentage}%  {health}")
    print(f"\nTotal carregadores:  {total}")
    print(f"  Online:            {online}")
    print(f"  Em uso:            {in_use}")
    print(f"  Livres:            {free}")
    print(f"  Manutenção:        {maintenance}")

    header("OPERAÇÃO EM TEMPO REAL")
    print(f"\nSessões ativas:      {len(active_sessions)}")
    print(f"Potência em uso:     {total_power_now} kW")
    print(f"Sessões finalizadas: {len(finished_sessions)}")
    print(f"Energia distribuída: {total_energy:.1f} kWh")
    print(f"Faturamento total:   R$ {total_revenue:.2f}")

    header("USUÁRIOS")

    print(f"\nUsuários ativos:     {active_users}")
    print(f"  Comerciais:        {commercial_users}")
    print(f"  Residenciais:      {residential_users}")

    header("ESTABELECIMENTOS")
    
    for est in establishments:
        chargers_est = [c for c in establishment_chargers if c['estabelecimento_id'] == est['id']]
        in_use_est = len([c for c in chargers_est if c['status'] == 'em_uso'])
        print(f"\n  {est['nome']}")
        print(f"  Carregadores: {len(chargers_est)}  |  Em uso: {in_use_est}")
        print(f"  Faturamento:  R$ {est['faturamento']:.2f}")
        print(f"  Energia:      {est['energia_total_distribuida_kwh']} kWh")

    footer()