from core.utils import header, get_separator,get_menu_option,get_numeric_input
from modules.common.database import global_stats,system_settings,devices_mock
def display_global_dashboard():
    """Exibe os indicadores macro da rede de carregadores GoodWe."""
    header("DASHBOARD GLOBAL DE ATIVOS - GOODWE MASTER", 65)

    stats=global_stats

    #Cálculo de KPI(Indicador de Performace)
    online_rate= (stats['dispositivos_online'] / stats['total_dispositivos']) * 100
    
    print(f"""
ESTADO DA REDE:
- Dispositivos Totais: {stats['total_dispositivos']}    
- Dispositivos Online: {stats['dispositivos_online']}
"- Taxa de Disponibilidade: {online_rate:.1f}%
""")
    
    # Barra de progresso visual para a taxa online
    bar_size = 20
    filled= int(bar_size * online_rate / 100)
    print(f"Status: [{'#' * filled}{'-' * (bar_size - filled)}]")

    print(get_separator(65))

    print(f"""
INDICADORES FINANCEIROS (B2B):
- Energia Total Transmitida: {stats['total_energia_acumulada_mwh']} MWh 
- Dispositivos Online: {stats['dispositivos_online']}
- Receita Total de Royalties: R$ {stats['receita_royalties_total']:,.2f}
""")
    print(get_separator(65))
    print("MENSAGEM DO SISTEMA: Rede operando dentro dos parâmetros nominais.")




def get_new_fare():
    """Lógica interna para escolher e editar uma tarifa específica."""
    while True:
        # Criamos o texto aqui dentro para mostrar os valores SEMPRE atualizados
        menu_edicao = (
            f"\n1. Tarifa Base: R$ {system_settings['tarifa_base']:.2f}\n"
            f"2. Tarifa Pico: R$ {system_settings['tarifa_pico']:.2f}\n"
            f"3. Cancelar e Voltar\n\n"
            "Escolha qual deseja alterar: "
        )
        
        fare = get_menu_option('EDITANDO VALORES DE TARIFA', menu_edicao)
        
        if fare == 1:
            new_val = get_numeric_input("Novo valor Tarifa Base: R$ ", 0.1, 10.0)
            system_settings['tarifa_base'] = new_val
            print(f"\n[OK] Atualizado para R$ {new_val:.2f}")
            return # Sai da edição e volta para a pergunta Sim/Não
            
        elif fare == 2:
            new_val = get_numeric_input("Novo valor Tarifa Pico: R$ ", 0.1, 10.0)
            system_settings['tarifa_pico'] = new_val
            print(f"\n[OK] Atualizado para R$ {new_val:.2f}")
            return # Sai da edição e volta para a pergunta Sim/Não
            
        elif fare == 3:
            break # Apenas volta
        else:
            print("\n[!] Opção Inválida!")

def update_global_fees():
    """Interface principal de tarifação para o Admin."""
    while True:
        header("AJUSTE DE TARIFAS GLOBAIS", 55)
        print(f"STATUS ATUAL:")
        print(f"- Base: R$ {system_settings['tarifa_base']:.2f}")
        print(f"- Pico: R$ {system_settings['tarifa_pico']:.2f}")
        print("-" * 55)
        
        op = input('\nDeseja alterar alguma tarifa? (S/N): ').upper().strip()
        
        if op == 'S':
            get_new_fare()
        elif op == 'N':
            print('Voltando...')
            break
        else:
            print('[ERRO] Digite apenas S ou N.')
        input("Pressione Enter para tentar novamente...")


def display_royalties_report():
    """Calcula e exibe a receita da GoodWe baseada no uso dos parceiros."""
    header("RELATÓRIO DE ROYALTIES (B2B) - RECEITA MASTER", 60)
    
    # 1. Pegamos a taxa de comissão do banco de dados (0.10 = 10%)
    rate = system_settings["comissao_goodwe"]
    
    # 2. Calculamos o faturamento total somando o rendimento de TODOS os dispositivos
    network_revenue = sum(dev['rendimento'] for dev in devices_mock)
    
    # 3. Calculamos a parte que pertence à GoodWe
    total_royalties = network_revenue * rate

    # Atualiza o dado global para manter o Dashboard Global coerente
    global_stats["receita_royalties_total"] = total_royalties

    print(f"""
ANÁLISE DE PARCEIROS COMERCIAIS:
- Faturamento Bruto da Rede: R$ {network_revenue:>12,.2f}
- Taxa de Royalties Fixada: {rate*100:>12.1f}%
{get_separator(60)}
RECEITA LÍQUIDA GOODWE: R$ {total_royalties:>15,.2f}
{get_separator(60)}

MENSAGEM: Este valor representa a soma das taxas de serviço
sobre o uso de hardware alugado/vendido para terceiros.
""")


def display_network_health():
    """Filtra e exibe dispositivos que apresentam falhas ou avisos em toda a rede."""
    header("RELATÓRIO DE SAÚDE DA REDE - SUPORTE GLOBAL", 65)

    alerts = [dev for dev in devices_mock if dev['status'] in ["Falha", "Aviso"]]

    if not alerts:
        print("\n[V] EXCELENTE: Todos os dispositivos da rede estão operando normalmente.")
    else:
        print(f"""
ATENÇÃO: Foram detectados {len(alerts)} dispositivos com irregularidades.
{get_separator(65)}
{'ID':<10} | {'MODELO':<8} | {'STATUS':<12} | {'AÇÃO SUGERIDA'}
{"-" * 65}
""")

        for dev in alerts:
            acao = "TROCA URGENTE" if dev['status'] == "Falha" else "VISITA TÉCNICA"
            # Destacando visualmente a falha
            status_fmt = f"!!! {dev['status']}" if dev['status'] == "Falha" else f"! {dev['status']}"
            
            print(f"{dev['id']:<10} | {dev['modelo']:<8} | {status_fmt:<12} | {acao}")

    print(get_separator(65))
    print("MENSAGEM: O suporte regional foi notificado automaticamente via log.")