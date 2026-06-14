from database.database import establishment_chargers, residencial_charger, settings
from utils.system import reset_terminal, load
from utils.ui import header, error_option
from utils.validate.mutual_data import validate_option


CURRENT_FIRMWARE = "2.4.1"
LATEST_FIRMWARE  = "2.5.0"

firmware_versions = {}  # carregador_id: versao


def get_charger_firmware(charger_id):
    return firmware_versions.get(charger_id, CURRENT_FIRMWARE)


def firmware_manager():
    while True:
        reset_terminal()
        header("GESTÃO DE FIRMWARE")

        all_chargers = establishment_chargers + residencial_charger
        outdated = [c for c in all_chargers if get_charger_firmware(c['id']) != LATEST_FIRMWARE]

        print(f"\nVersão atual da rede: {CURRENT_FIRMWARE}")
        print(f"Versão mais recente:  {LATEST_FIRMWARE}")
        print(f"OCPP:                 {settings['versao_ocpp']}")
        print(f"\nCarregadores desatualizados: {len(outdated)}/{len(all_chargers)}\n")

        print("--- Status por Carregador ---\n")
        for c in all_chargers:
            version = get_charger_firmware(c['id'])
            status_fw = "✅ Atualizado" if version == LATEST_FIRMWARE else "⬆  Atualização disponível"
            print(f"  ID #{c['id']} — {c['modelo']:<20} v{version}  {status_fw}")

        options = validate_option("""
1 - Atualizar todos os carregadores
2 - Atualizar carregador específico
0 - Voltar

Opção: """)

        match options:
            case 1:
                update_all(all_chargers)
            case 2:
                update_single(all_chargers)
            case 0:
                break
            case _:
                error_option()


def update_all(all_chargers):
    reset_terminal()
    header("ATUALIZAÇÃO EM LOTE")

    outdated = [c for c in all_chargers if get_charger_firmware(c['id']) != LATEST_FIRMWARE]
    if not outdated:
        print("\n✅ Todos os carregadores já estão na versão mais recente.")
        input("\nAperte Enter para voltar...")
        return

    print(f"\nAtualizando {len(outdated)} carregador(es) para v{LATEST_FIRMWARE}...\n")
    for c in outdated:
        load(f"  Enviando firmware para ID #{c['id']}")
        firmware_versions[c['id']] = LATEST_FIRMWARE
        print(f"  ✅ ID #{c['id']} — {c['modelo']} → v{LATEST_FIRMWARE}")

    print(f"\n✅ Atualização concluída. {len(outdated)} dispositivo(s) atualizados.")
    input("\nAperte Enter para voltar...")


def update_single(all_chargers):
    reset_terminal()
    header("ATUALIZAR CARREGADOR")

    for c in all_chargers:
        version = get_charger_firmware(c['id'])
        print(f"  [{c['id']}] ID #{c['id']} — {c['modelo']}  v{version}")

    try:
        charger_id = int(input("\nID do carregador (0 para voltar): ").strip())
    except ValueError:
        return

    if charger_id == 0:
        return

    target = next((c for c in all_chargers if c['id'] == charger_id), None)
    if not target:
        print("\nCarregador não encontrado.")
        input("\nAperte Enter para voltar...")
        return

    current = get_charger_firmware(charger_id)
    if current == LATEST_FIRMWARE:
        print(f"\n✅ ID #{charger_id} já está na versão mais recente (v{LATEST_FIRMWARE}).")
        input("\nAperte Enter para voltar...")
        return

    load(f"\nEnviando firmware v{LATEST_FIRMWARE} para ID #{charger_id}")
    firmware_versions[charger_id] = LATEST_FIRMWARE
    print(f"\n✅ ID #{charger_id} atualizado: v{current} → v{LATEST_FIRMWARE}")
    input("\nAperte Enter para voltar...")