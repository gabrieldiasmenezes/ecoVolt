from database.database import establishments, establishment_chargers
from utils.system import reset_terminal
from utils.ui import footer, header, enter, separator, error_option
from utils.validation.common_validation import validate_int_value

from utils.helpers import (
    find_list_item_by_field,
    get_list_item_by_status,
    split_chargers
)


# ==========================
# DETALHES DO ESTABELECIMENTO
# ==========================

def detail_establishment(est):

    reset_terminal()
    header("DETALHES DO ESTABELECIMENTO")

    chargers = find_list_item_by_field(
        establishment_chargers,
        est["id"],
        "estabelecimento_id"
    )

    print(f"\n{est['nome']}")
    print(f"Endereço:  {est['endereco']}")
    print(f"Empresa:   {est['empresa_responsavel']}")

    solar = "Sim ☀" if est.get("possui_energia_solar") else "Não"
    print(f"Solar:     {solar}")

    print("\n--- Carregadores ---\n")

    for c in chargers:

        tipo = (
            "🔶 Premium"
            if c.get("reservado_premium")
            else "🔷 Comum"
        )

        print(f"Carregador #{c['numero']}  {tipo}")
        print(f"Status:   {c['status'].upper()}")
        print(f"Potência: {c['potencia_maxima']} kW")
        print()

    footer()


# ==========================
# LISTAGEM
# ==========================

def find_establishments():

    reset_terminal()
    while True:
        header("ESTABELECIMENTOS DISPONÍVEIS")

        ativos = get_list_item_by_status(establishments,"ativo")

        if not ativos:
            print("\nNenhum estabelecimento disponível no momento.")
            enter()
            return

        print()

        for i, est in enumerate(ativos):

            chargers = find_list_item_by_field(
                establishment_chargers,
                est["id"],
                "estabelecimento_id"
            )

            livres = get_list_item_by_status(chargers,"livre")

            em_uso = get_list_item_by_status(chargers,"em_uso")

            solar = (
                "Solar"
                if est.get("possui_energia_solar")
                else ""
            )

            print(f"[{i+1}] {est['nome']}  {solar}")
            print(f"    Endereço: {est['endereco']}")
            print(f"    Carregadores disponíveis: {est['carregadores_disponiveis']}")
            print(f"    Em uso: {len(em_uso)}  |  Livres: {len(livres)}")
            print()

        separator()

        option = validate_int_value(
            "\nDigite o número para ver detalhes ou 0 para voltar\n\nOpção: "
        )

        if option == 0:
            break

        if option < 1 or option > len(ativos):
            error_option()
            continue
        break

    detail_establishment(ativos[option - 1])