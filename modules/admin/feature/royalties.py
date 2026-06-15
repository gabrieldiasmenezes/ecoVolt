from database.database import establishments, sessions
from database.settings import ROYALTY_RATE
from utils.helpers import get_list_item_by_status
from utils.system import reset_terminal
from utils.ui import footer, header, separator



def royalties_report():
    reset_terminal()
    header("RELATÓRIO DE ROYALTIES")

    total_royalties = 0.0

    print(f"\nTaxa de royalty configurada: {int(ROYALTY_RATE * 100)}%\n")
    separator()

    for est in establishments:
        est_sessions = get_list_item_by_status(sessions,'finalizada')
        revenue = sum(s['valor'] for s in est_sessions)
        royalty = round(revenue * ROYALTY_RATE, 2)
        total_royalties += royalty

        active_sessions_list=get_list_item_by_status(sessions,'ativa')
        active_sessions = len(active_sessions_list)
        active_revenue = sum(s['valor'] for s in active_sessions_list)
        projected_royalty = round((revenue + active_revenue) * ROYALTY_RATE, 2)

        print(f"\n{est['nome']}")
        print(f"  Empresa:            {est['empresa_responsavel']}")
        print(f"  Faturamento base:   R$ {revenue:.2f}")
        print(f"  Sessões ativas:     {active_sessions}")
        print(f"  Royalty gerado:     R$ {royalty:.2f}")
        print(f"  Projeção total:     R$ {projected_royalty:.2f}")

    separator()
    print(f"\n💰 Total de royalties GoodWe: R$ {total_royalties:.2f}")
    print(f"   (sobre sessões finalizadas)")
    footer()