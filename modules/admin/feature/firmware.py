from database.database import establishment_chargers, residencial_charger, settings
from database.settings import CURRENT_FIRMWARE, LATEST_FIRMWARE
from utils.helpers import find_charger_by_input, format_charger_id, get_charger_key
from utils.system import reset_terminal, load
from utils.ui import enter, header, error_option
from utils.validation.common_validation import validate_int_value

firmware_versions = {}  # charger_key (str): version


def get_charger_firmware(charger):
    key = get_charger_key(charger)
    return firmware_versions.get(key, CURRENT_FIRMWARE)


MENU = """
1 - Atualizar todos os carregadores
2 - Atualizar carregador específico
0 - Voltar

Opção: """


def firmware_manager():
    while True:
        reset_terminal()
        header("GESTÃO DE FIRMWARE")

        all_chargers = establishment_chargers + residencial_charger

        outdated = [
            c for c in all_chargers
            if get_charger_firmware(c) != LATEST_FIRMWARE
        ]

        print(f"\nVersão atual da rede: {CURRENT_FIRMWARE}")
        print(f"Versão mais recente:  {LATEST_FIRMWARE}")
        print(f"OCPP:                 {settings['versao_ocpp']}")
        print(f"\nDesatualizados: {len(outdated)}/{len(all_chargers)}\n")

        print("--- Status por Carregador ---\n")
        for c in all_chargers:
            version = get_charger_firmware(c)
            status_fw = "✅ Atualizado" if version == LATEST_FIRMWARE else "⬆ Atualização disponível"

            print(f"  [{format_charger_id(c)}] {c['modelo']:<20} v{version} {status_fw}")

        options = validate_int_value(MENU)

        match options:
            case 1:
                update_all(all_chargers)
            case 2:
                update_single(all_chargers)
            case 0:
                break
            case _:
                error_option()


# =========================
# UPDATE ALL
# =========================
def update_all(all_chargers):
    reset_terminal()
    header("ATUALIZAÇÃO EM LOTE")

    outdated = [
        c for c in all_chargers
        if get_charger_firmware(c) != LATEST_FIRMWARE
    ]

    if not outdated:
        print("\n✅ Todos já estão atualizados.")
        enter()
        return

    print(f"\nAtualizando {len(outdated)} carregadores...\n")

    for c in outdated:
        load(f"Atualizando {format_charger_id(c)}...")
        firmware_versions[get_charger_key(c)] = LATEST_FIRMWARE
        print(f"  ✔ {format_charger_id(c)} → v{LATEST_FIRMWARE}")

    print("\n✅ Atualização em lote concluída.")
    enter()


# =========================
# UPDATE SINGLE
# =========================
def update_single(all_chargers):
    while True:
        reset_terminal()
        header("ATUALIZAR CARREGADOR")

        print("\n📌 Identificação dos carregadores:")
        print("   🏢 E = Estabelecimento")
        print("   🏠 R = Residencial\n")

        for c in all_chargers:
            version = get_charger_firmware(c)
            prefix = "E" if "estabelecimento_id" in c else "R"

            print(f"  [{prefix}{c['id']}] {c['modelo']} v{version}")

        raw = input("\nDigite E ou R + ID (ex: E1, R1 | 0 para voltar): ").strip().upper()

        if raw == "0":
            return

        target = find_charger_by_input(all_chargers, raw)

        if not target:
            print("\n❌ Carregador não encontrado.")
            enter()
            continue

        current = get_charger_firmware(target)

        if current == LATEST_FIRMWARE:
            print("\n✅ Já está atualizado.")
            enter()
            continue

        load(f"\nAtualizando {raw}...")

        firmware_versions[get_charger_key(target)] = LATEST_FIRMWARE

        print(f"\n✔ {raw}: v{current} → v{LATEST_FIRMWARE}")
        enter()
        return