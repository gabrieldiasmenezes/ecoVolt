from auth.auth import auth
from database.database import users

from modules.admin.admin import admin_service
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
"""
MODO DE TESTE (SEM AUTENTICAÇÃO)

Para facilitar a validação da aplicação, é possível executar o sistema
sem precisar realizar login repetidamente.

Para isso:
1. Comente a linha: user = auth()
2. Descomente o bloco abaixo que busca o usuário diretamente no banco de dados.

Cada ID representa um perfil diferente para testes:

1000 e 1001 -> cliente comercial  
1002        -> cliente residencial  
1003        -> dono de estabelecimento  
1004        -> administrador GoodWe  

  IMPORTANTE:
Este modo deve ser usado apenas para testes e desenvolvimento.
Em produção, a autenticação deve permanecer ativa.
"""
def main():
    try:
        welcome()
        while True:
            # user = auth()
            for u in users:
                if u['id'] == 1001:
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
    except ModuleNotFoundError as e:
        print("[ERRO] Aplicação falhando: ",e)
        

if __name__ == "__main__":
    main()