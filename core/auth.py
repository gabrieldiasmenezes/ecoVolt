from core.utils import get_separator,header
import re

def welcome():
    """Exibe a mensagem de boas-vindas e captura o nome do usuário com validação Regex."""
    print("\n" + get_separator(55))
    print("      SISTEMA INTELIGENTE DE GESTÃO DE ENERGIA")
    print("           CHARGEGRID | Powered by GoodWe")
    print(get_separator(55))
    
    while True:
        user_name = input("\nOlá! Para iniciarmos sua experiência, digite seu nome: ").strip()
        
        # Regex: Permite letras (A-Z, a-z), acentuação latina e espaços.
        # Bloqueia números, símbolos e combinações sem sentido como "!!!" ou "a1b2".
        pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$"
        
        if len(user_name) < 3:
            print("[!] Por favor, digite um nome válido (mínimo 3 caracteres).")
        elif not re.match(pattern, user_name):
            print("[!] Nome inválido! Utilize apenas letras e espaços, sem números ou símbolos.")
        elif len(set(user_name)) == 1: 
            # Impede casos como "aaaaa" ou "     "
            print("[!] Por favor, digite um nome real, não apenas caracteres repetidos.")
        else:
            print(f"\nSeja bem-vindo, {user_name}! Conectando ao ecossistema GoodWe...")
            return user_name
    

def get_user_profile():
    """Solicita ao usuário que selecione seu perfil de acesso."""
    header("PORTAL DE IDENTIFICAÇÃO",60)
    try:
        profile_choice = int(input("""
Selecione o perfil de acesso:
  1 - Cliente Comercial (Venda de Recarga)
  2 - Dono do Estabelecimento (Gestão de Lucro/Hardware)
  3 - Cliente Residencial (Gestão Privada)
  4 - GoodWe Admin (Gestão de Ativos Alugados)
  5 - Saiba mais sobre os tipos de acesso
  6 - Sair do Sistema
  
  Digite a opção desejada: """))
        return profile_choice
    except ValueError:
        return None