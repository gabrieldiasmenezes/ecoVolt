from core.utils import header,get_menu_option

def display_financial_report(data):
    header("RELATÓRIO FINANCEIRO", 35)
    for period, value in data.items(): 
        print(f"{period.capitalize():<12}: R$ {value:>10.2f}")

def display_devices_status(devices_list):
    header("MONITORAMENTO DE DISPOSITIVOS - GOODWE", 60)
    print(f"{'ID':<10} | {'MODELO':<8} | {'STATUS':<12} | {'ÚLT. MANUTENÇÃO'}")
    print("-" * 60)
    for dev in devices_list:
        status = dev['status']
        status_fmt = f"!!! {status}" if status == "Falha" else (f"! {status}" if status == "Aviso" else status)
        print(f"{dev['id']:<10} | {dev['modelo']:<8} | {status_fmt:<12} | {dev['ultima_manutencao']}")
    print("-" * 60)



def update_device_status(devices_list):
    """
    Interface para o administrador localizar um dispositivo e alterar seu estado.
    """
    header("SISTEMA DE MANUTENÇÃO - GOODWE", 55)

    #1. Pedir o ID do carregador
    search_id=input("\nDigite o ID do dispositivo (ex: GW-001) ou 'S' para sair: ").upper().strip()

    if search_id == 'S': return 

    device_found=None

    for dev in devices_list:
        if dev['id'] == search_id:
            device_found = dev
            break

    if device_found:
        while True:
            op=get_menu_option("ESCOLHA DO NOVO STATUS",f"""
    [!] Dispositivo localizado: {device_found['modelo']}
    [!] Status Atual: {device_found['status']}
    Escolha o novo status:
        1 - Bom
        2 - Aviso
        3 - Falha
    Opção: """,)
            new_status=None
            match op:
                case 1:
                    new_status= 'Bom'
                case 2:
                    new_status= 'Aviso'
                case 3:
                    new_status = 'Falha'
                case _:
                    print("ESCOLHA UMA OPÇÃO VÁLIDA")
                    input("Press Enter para continuar...")
                    continue
            break
        device_found['status']=new_status
        print(f"\n[OK] Status do dispositivo {search_id} atualizado para {new_status}!")
    else:
        print("\n[!] Erro: Dispositivo não encontrado.")

