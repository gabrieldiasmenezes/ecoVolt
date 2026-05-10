from core.utils import clear_terminal, show_system_info, get_menu_option
from core.auth import welcome
from modules.commercial.controller import run_commercial_module
from modules.establishment.controller import run_establishment_module
from modules.admin.controller import run_admin_module
from modules.residencial.controller import run_residential_module


def main():
    # Variável referente ao menu de opções:
    menu_perfil = """
    Selecione o perfil de acesso:
    1 - Cliente Comercial
    2 - Dono do Estabelecimento
    3 - Cliente Residencial
    4 - GoodWe Admin
    5 - Saiba mais
    6 - Sair
    
    Digite a opção: """

    # --- Main Program ---
    clear_terminal()
    current_user = welcome()

    while True:
        profile_selection = get_menu_option("PORTAL DE IDENTIFICAÇÃO", menu_perfil)
            
        match profile_selection:
            case 1:
                clear_terminal()
                run_commercial_module()  # Apenas chamada da função, sem lógica interna
                
            case 2:
                run_establishment_module()
                input("Press Enter para continuar...")
                
            case 3:
                run_residential_module(current_user)
                
            case 4:
                run_admin_module()
                
            case 5:
                show_system_info()
                
            case 6:
                print("\nEncerrando conexão com ChargeGrid Intelligence...")
                print("Até logo!")
                break
                
            case _:
                print("\n[!] Opção inválida. Escolha um número entre 1 e 6.")
                input("Pressione Enter para tentar novamente.")
                continue


if __name__ == "__main__":
    main()