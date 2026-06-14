from database.database import establishments, sessions
from utils.system import reset_terminal
from utils.ui import header

ROYALTY_RATE = 0.10  # 10% padrão


def royalties_report():
    reset_terminal()
    header("RELATÓRIO DE ROYALTIES")

    total_royalties = 0.0

    print(f"\nTaxa de royalty configurada: {int(ROYALTY_RATE * 100)}%\n")
    print("=" * 40)

    for est in establishments:
        est_sessions = [
            s for s in sessions
            if s['status'] == 'finalizada'
        ]
        revenue = sum(s['valor'] for s in est_sessions)
        royalty = round(revenue * ROYALTY_RATE, 2)
        total_royalties += royalty

        active_sessions = len([s for s in sessions if s['status'] == 'ativa'])
        active_revenue = sum(s['valor'] for s in sessions if s['status'] == 'ativa')
        projected_royalty = round((revenue + active_revenue) * ROYALTY_RATE, 2)

        print(f"\n{est['nome']}")
        print(f"  Empresa:            {est['empresa_responsavel']}")
        print(f"  Faturamento base:   R$ {revenue:.2f}")
        print(f"  Sessões ativas:     {active_sessions}")
        print(f"  Royalty gerado:     R$ {royalty:.2f}")
        print(f"  Projeção total:     R$ {projected_royalty:.2f}")

    print(f"\n{'='*40}")
    print(f"\n💰 Total de royalties GoodWe: R$ {total_royalties:.2f}")
    print(f"   (sobre sessões finalizadas)")
    print("\n" + "=" * 40)
    input("\nAperte Enter para voltar...")