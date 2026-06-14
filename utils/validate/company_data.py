import re
from database.database import users

def validate_cnpj(cnpj):

    clean_cnpj = re.sub(r'\D', '', cnpj)

    if len(clean_cnpj) != 14:
        print("Erro: O CNPJ precisa ter exatamente 14 números!")
        return False

    if clean_cnpj == clean_cnpj[0] * 14:
        print("Erro: CNPJ inválido! Não é permitido um CNPJ com todos os dígitos iguais.")
        return False

    weights_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_1 = sum(int(clean_cnpj[i]) * weights_1[i] for i in range(12))
    remainder_1 = sum_1 % 11
    digit_1 = 0 if remainder_1 < 2 else 11 - remainder_1

    if int(clean_cnpj[12]) != digit_1:
        print("Erro: CNPJ inválido! Falha na validação do primeiro dígito verificador.")
        return False

    weights_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    sum_2 = sum(int(clean_cnpj[i]) * weights_2[i] for i in range(13))
    remainder_2 = sum_2 % 11
    digit_2 = 0 if remainder_2 < 2 else 11 - remainder_2

    if int(clean_cnpj[13]) != digit_2:
        print("Erro: CNPJ inválido! Falha na validação do segundo dígito verificador.")
        return False
    
    for user in users:
        stored_cnpj = re.sub(r'\D', '', user.get('cnpj', ''))
        if stored_cnpj == clean_cnpj:
            print("Erro: CNPJ já existente no banco de dados!!")
            return False

    return True

def validate_company_name(name):
    clean_name = name.strip()

    padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9 '&-]{3,}$"

    if not re.fullmatch(padrao, clean_name):
        print("[Erro] Nome de empresa inválido.")
        return False

    return True


def validate_address(address):

    clean_address = address.strip()
    
    padrao = r"^[A-Za-z0-9À-ÖØ-öø-ÿ\s\.\'-]+,\s*\d+$"
    
    if not re.fullmatch(padrao, clean_address):
        print("Endereço inválido: O formato correto deve ser 'Nome da Rua, Número' (Ex: Av. Paulista, 1000)!")
        return False

    return True

