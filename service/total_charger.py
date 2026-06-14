from database.database import POTENCIA_ESTABELECIMENTO

def get_total_chargers():

    while True:
        try:
            demanda_kw = int(input("Informe a demanda contratada (kW): "))

            if demanda_kw <= 0:
                print("A demanda deve ser maior que zero!")
                continue

            max_carregadores = demanda_kw // POTENCIA_ESTABELECIMENTO

            if max_carregadores < 1:
                max_carregadores = 1

            print("\n=== DIMENSIONAMENTO DO SISTEMA ===")
            print(f"Demanda contratada: {demanda_kw} kW")
            print(f"Potência por carregador: {POTENCIA_ESTABELECIMENTO} kW")
            print(f"Carregadores máximos suportados: {max_carregadores}")

            while True:
                try:
                    contratados = int(input("\nQuantos carregadores deseja instalar? "))

                    if contratados <= 0:
                        print("O número deve ser maior que zero!")
                        continue

                    if contratados > max_carregadores:
                        print(
                            f"Não é possível instalar {contratados} carregadores. "
                            f"Máximo suportado: {max_carregadores}"
                        )
                        continue

                    print("\nCarregadores aprovados com sucesso!")
                    return demanda_kw,contratados

                except ValueError:
                    print("Digite um número válido.")

        except ValueError:
            print("Valor inválido! Digite um número inteiro.")