import re
from pydantic import BaseModel, EmailStr, ValidationError
from utils.helpers import field_exists


# ========================================
# HELPERS
# ========================================

def validate_int_value(text):
    while True:
        try:

            value = int(input(text))
            
            if value >= 0:
                return value
            else:
                print("[Erro] O número deve ser positivo. Tente novamente.")

            
        except ValueError:
            print("[ERRO] Digite apenas números inteiros válidos.")

def validate_float_value(text):
    while True:
        try:

            value = float(input(text))
            
            if value > 0:
                return value
            else:
                print("[Erro] O número deve ser positivo. Tente novamente.")

            
        except ValueError:
            print("[ERRO] Digite apenas números inteiros válidos.")


def get_valid_input(message, validator):
    while True:
        value = input(message)

        if validator(value):
            return value

def clean_numbers(text):
    return re.sub(r"\D", "", text)


# ========================================
# NOME
# ========================================

def validate_name(name):
    clean_name = name.strip()

    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(\s[A-Za-zÀ-ÖØ-öø-ÿ]+)+$'

    if not re.fullmatch(pattern, clean_name):
        print("Nome inválido. Digite nome e sobrenome.")
        return False

    if not clean_name.istitle():
        print("Utilize iniciais maiúsculas.")
        return False

    return True


# ========================================
# EMAIL
# ========================================

class UserEmail(BaseModel):
    email: EmailStr


def validate_email(email):
    clean_email = email.strip().lower()

    try:
        UserEmail(email=clean_email)
    except ValidationError:
        print("Formato de e-mail inválido.")
        return False

    if field_exists("email", clean_email):
        print("E-mail já cadastrado.")
        return False

    return True


# ========================================
# TELEFONE
# ========================================

def validate_telephone(telephone):
    clean_phone = clean_numbers(telephone)

    if len(clean_phone) != 11:
        print("Telefone inválido. Deve conter 11 dígitos.")
        return False

    if field_exists("telefone", clean_phone):
        print("Telefone já cadastrado.")
        return False

    return True


# ========================================
# SENHA
# ========================================

def validate_password(password):
    clean_password = password.strip()

    if len(clean_password) < 6:
        print("A senha deve possuir no mínimo 6 caracteres.")
        return False

    return True


# ========================================
# CIDADE
# ========================================

def validate_city(city):
    clean_city = city.strip()

    pattern = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s-]+$'

    if not clean_city:
        print("Cidade não pode estar vazia.")
        return False

    if not re.fullmatch(pattern, clean_city):
        print("Cidade inválida.")
        return False

    return True