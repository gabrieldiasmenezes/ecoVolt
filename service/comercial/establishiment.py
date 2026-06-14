from database.database import establishments, establishment_chargers
from utils.system import reset_terminal
from utils.ui import header,enter

from utils.ui import error_option
from utils.validate.mutual_data import validate_option

def detail_establishment(est):
    reset_terminal()
    header("DETALHES DO ESTABELECIMENTO")

    chargers = [c for c in establishment_chargers if c['estabelecimento_id'] == est['id']]

    print(f"\n{est['nome']}")
    print(f"Endereço:  {est['endereco']}")
    print(f"Empresa:   {est['empresa_responsavel']}")
    solar = "Sim ☀" if est.get('possui_energia_solar') else "Não"
    print(f"Solar:     {solar}")
    print(f"\n--- Carregadores ---\n")

    for c in chargers:
        tipo = "🔶 Premium" if c.get('reservado_premium') else "🔷 Comum"
        print(f"  Carregador #{c['numero']}  {tipo}")
        print(f"  Status:   {c['status'].upper()}")
        print(f"  Potência: {c['potencia_maxima']} kW")
        print()

    print("=" * 40)
    enter()

def find_establishments():
    reset_terminal()
    header("ESTABELECIMENTOS DISPONÍVEIS")

    ativos = [e for e in establishments if e['status'] == 'ativo']

    if not ativos:
        print("\nNenhum estabelecimento disponível no momento.")
        enter()
        return

    print()
    for i, est in enumerate(ativos):
        livres = sum(
            1 for c in establishment_chargers
            if c['estabelecimento_id'] == est['id'] and c['status'] == 'livre'
        )
        em_uso = sum(
            1 for c in establishment_chargers
            if c['estabelecimento_id'] == est['id'] and c['status'] == 'em_uso'
        )
        solar = "Solar" if est.get('possui_energia_solar') else ""

        print(f"[{i+1}] {est['nome']}  {solar}")
        print(f"    Endereço:    {est['endereco']}")
        print(f"    Carregadores disponíveis: {est['carregadores_disponiveis']}")
        print(f"    Em uso: {em_uso}  |  Livres: {livres}")
        print()

    print("=" * 40)
    option = validate_option("\nDigite o número para ver detalhes ou 0 para voltar\n\nOpção: ")

    if option == 0:
        return

    if option < 1 or option > len(ativos):
        error_option()
        return

    detail_establishment(ativos[option - 1])
