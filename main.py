from auth.auth import auth
from service.admin.admin import admin_service
from service.comercial.comercial import comercial_service
from service.establishment.establishment import establishment_service
from service.residencial.residencial import residencial_service
from utils.system import load, reset_terminal
from database.database import users


def main():
    reset_terminal()

    print("""
========================================
    CHARGEGRID INTELLIGENCE
Sistema Inteligente de Recarga Elétrica
========================================
""")

    # input("Aperte Enter para começar...")
    load("Inicializando sistema")

    # user = auth()
    for u in users:
        if u['id'] == 1004:
            user=u

    if not user:
        return
    
    type_account=user['perfil']
    match type_account:
        case 'dono_estabelecimento':
            establishment_service(user['id'])
        case 'cliente_comercial':
            comercial_service(user)
        case 'cliente_residencial':
            residencial_service(user)
        case 'administrador':
            admin_service(user)
        



if __name__ == "__main__":
    main()