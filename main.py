from auth.auth import auth
from database.database import users

from modules.comercial.comercial import comercial_service
from modules.establishment.establishment import establishment_service
from modules.residential.residential import residencial_service
from utils.system import reset_terminal,load
from utils.ui import enter

def welcome():
    reset_terminal()
    print("""
========================================
    CHARGEGRID INTELLIGENCE
Sistema Inteligente de Recarga Elétrica
========================================
""")
    enter()
    load("Inicializando sistema")

def main():
    try:
        # welcome()
        while True:
            # user = auth()
            for u in users:
                if u['id'] == 1002:
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
                # case 'administrador':
                #     admin_service(user)
    except ModuleNotFoundError as e:
        print("[ERRO] Aplicação falhando: ",e)
        

if __name__ == "__main__":
    main()