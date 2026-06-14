import re
from pydantic import BaseModel, EmailStr, ValidationError
from database.database import users
def validate_option(text):
    while True:
        try:
            return int(input(text))
        except ValueError:
            print("Digite apenas números.")

def validate_name(name):
    clean_name=name.strip()
    padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(\s[A-Za-zÀ-ÖØ-öø-ÿ]+)+$'

    if re.fullmatch(padrao, clean_name) and clean_name.istitle(): 
        return True
    print("[Erro] Nome inválido,escreva o nome completo!")
    return False


class Usuario(BaseModel):
    email: EmailStr

def validate_email(email):
    try:
        clean_email=email.strip().lower()
        Usuario(email=clean_email)
    except ValidationError:
        print('Formato de e-mail inválido!')
        return False            
    for user in users:
        if user['email'] == clean_email:
            print('Email ja cadastrado no banco de dados!!')
            return False
    return True


def validade_telephone(telephone):
    clean_phone = re.sub(r'\D', '', telephone)
    
    if len(clean_phone) != 11:
        print("Telefone inválido: Deve conter exatamente 11 dígitos (DDD + número)!")
        return False
        
    for user in users:
        if user.get('telefone') == clean_phone:
            print("Telefone inválido: Este telefone já está cadastrado no banco de dados!!")
            return False
            
    return True

def validate_password(password):
    clean_password= password.strip()
    
    if len(clean_password) < 6:
        print("Erro: A senha precisa ter no mínimo 6 caracteres!")
        return False
        
    return True


def validate_city(city):
    city_clean = city.strip()

    padrao = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s-]+$'
    
    if not city_clean or not re.fullmatch(padrao, city_clean):
        return False
        
    return True