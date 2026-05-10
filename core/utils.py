import os 
def clear_terminal():
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_separator(length):
    """Retorna uma linha separadora de '='."""
    return "=" * length

def header(text, length):
    """Limpa a tela e exibe um cabeçalho padronizado."""
    clear_terminal()
    print("\n" + get_separator(length))
    print(f"          {text}")
    print(get_separator(length))


def show_system_info():
    """Explica a hierarquia do sistema."""
    header("SISTEMA DE GESTÃO INTEGRADA GOODWE",65)

    print(">> COMERCIAL: Interface de venda para o usuário final.")
    print(">> ESTABELECIMENTO: Dono do ponto. Gere o lucro e os aparelhos.")
    print(">> RESIDENCIAL: Usuário doméstico. Gere seu consumo pessoal.")
    print(">> GOODWE: Gestão Master. Controla os dispositivos alugados (B2B).")
    print(get_separator(65))
    input("\nPressione Enter para voltar ao menu principal...")


def get_numeric_input(prompt, min_val=None, max_val=None, error_msg=None):
    """
    Função utilitária para garantir que o usuário digite um número válido 
    dentro de um intervalo específico antes de prosseguir.
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                msg = error_msg if error_msg else f"O valor deve ser no mínimo {min_val}."
                print(f"[!] Erro: {msg}")
                continue
            if max_val is not None and value > max_val:
                msg = error_msg if error_msg else f"O valor deve ser no máximo {max_val}."
                print(f"[!] Erro: {msg}")
                continue
            return value
        except ValueError:
            print("[ERRO] Por favor, insira apenas números.")


def get_menu_option(header_text, menu_text, length=60):
    """
    Função genérica para exibir um cabeçalho, um menu de opções 
    e validar a entrada numérica do usuário com loop de retry.
    """
    while True:
        header(header_text, length)
        try:
            choice = int(input(menu_text).strip())
            return choice
        except ValueError:
            print("[ERRO] Por favor, insira apenas números válidos.")
            input("Pressione Enter para tentar novamente...")
            continue