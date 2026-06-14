from auth.auth import auth
from utils.system import load, reset_terminal
from database.database import establishment_chargers,establishments
from utils.ui import header

def main():
    reset_terminal()

    print("""
========================================
    CHARGEGRID INTELLIGENCE
Sistema Inteligente de Recarga Elétrica
========================================
""")

    input("Aperte Enter para começar...")
    load("Inicializando sistema")

    user = auth()

    if not user:
        return

    header("USUÁRIO")

    for k, v in user.items():
        print(f"{k}: {v}")

    if user["perfil"] == "dono_estabelecimento":

        for est in establishments:

            if est["id_dono"] == user["id"]:

                header("ESTABELECIMENTO")

                for k, v in est.items():
                    print(f"{k}: {v}")

                header("CARREGADORES")

                encontrou = False

                for ch in establishment_chargers:

                    if ch["estabelecimento_id"] == est["id"]:

                        encontrou = True

                        print("-" * 40)

                        for k, v in ch.items():
                            print(f"{k}: {v}")

                if not encontrou:
                    print("Nenhum carregador cadastrado.")
        



if __name__ == "__main__":
    main()