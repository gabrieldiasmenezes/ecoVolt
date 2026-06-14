from utils.system import reset_terminal, load
from utils.ui import header, error_option
from utils.validate.mutual_data import validate_option


PAYMENT_METHODS = {
    1: "Cartão de Crédito",
    2: "Cartão de Débito",
    3: "Pix",
    4: "Carteira ChargeGrid"
}


def billing_service(user, total_price, session_type):
    reset_terminal()
    header("PAGAMENTO")

    print(f"\nValor a pagar:  R$ {total_price:.2f}")
    print(f"Tipo de sessão: {session_type.capitalize()}\n")
    print("Forma de pagamento:\n")

    for key, method in PAYMENT_METHODS.items():
        print(f"  [{key}] {method}")

    print()
    option = validate_option("Escolha (0 para cancelar): ")

    if option == 0:
        print("\nPagamento cancelado.")
        input("\nAperte Enter para voltar...")
        return False

    if option not in PAYMENT_METHODS:
        error_option()
        return False

    chosen_method = PAYMENT_METHODS[option]
    load(f"\nProcessando pagamento via {chosen_method}")

    if option in (1, 2):
        return _card_payment(total_price, chosen_method)
    elif option == 3:
        return _pix_payment(total_price, user)
    elif option == 4:
        return _wallet_payment(total_price, user)

    return False


def _card_payment(total_price, method):
    reset_terminal()
    header(f"PAGAMENTO — {method.upper()}")

    print(f"\nValor: R$ {total_price:.2f}\n")
    card_number = input("Últimos 4 dígitos do cartão: ").strip()

    if not card_number.isdigit() or len(card_number) != 4:
        print("\n❌ Número inválido.")
        input("\nAperte Enter para voltar...")
        return False

    load("\nComunicando com a operadora")
    load("Validando transação")

    reset_terminal()
    header("PAGAMENTO APROVADO")
    print(f"\n✅ R$ {total_price:.2f} aprovado!")
    print(f"Método: {method}")
    print(f"Cartão: **** **** **** {card_number}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para continuar...")
    return True


def _pix_payment(total_price, user):
    reset_terminal()
    header("PAGAMENTO — PIX")

    pix_key = f"chargegrid-{user['id']}@pagamento.com"

    print(f"\nValor:     R$ {total_price:.2f}")
    print(f"\nChave Pix: {pix_key}")
    print("\n  ████████████████")
    print("  ██  QR CODE   ██")
    print("  ████████████████")
    print("\nEscaneie o QR Code ou copie a chave acima.")

    confirm = validate_option("\n1 - Confirmar pagamento realizado\n0 - Cancelar\n\nOpção: ")
    if confirm != 1:
        return False

    load("\nValidando Pix")

    reset_terminal()
    header("PAGAMENTO APROVADO")
    print(f"\n✅ Pix de R$ {total_price:.2f} confirmado!")
    print(f"Chave:  {pix_key}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para continuar...")
    return True


def _wallet_payment(total_price, user):
    reset_terminal()
    header("PAGAMENTO — CARTEIRA CHARGEGRID")

    simulated_balance = round(user.get('total_recargas', 0) * 8.5, 2)

    print(f"\nSaldo disponível: R$ {simulated_balance:.2f}")
    print(f"Valor da recarga: R$ {total_price:.2f}")

    if simulated_balance < total_price:
        print(f"\n❌ Saldo insuficiente.")
        print(f"   Faltam: R$ {round(total_price - simulated_balance, 2):.2f}")
        input("\nAperte Enter para voltar...")
        return False

    new_balance = round(simulated_balance - total_price, 2)
    load("\nDebitando da carteira")

    reset_terminal()
    header("PAGAMENTO APROVADO")
    print(f"\n✅ R$ {total_price:.2f} debitado!")
    print(f"Saldo anterior: R$ {simulated_balance:.2f}")
    print(f"Saldo atual:    R$ {new_balance:.2f}")
    print("\n" + "=" * 40)
    input("\nAperte Enter para continuar...")
    return True