
from modules.admin.feature.syndic.api import call_syndic_api
from modules.admin.feature.syndic.context import build_network_context
from modules.admin.feature.syndic.fallback import syndic_fallback
from utils.system import reset_terminal, load
from utils.ui import header, separator
from utils.validation.common_validation import validate_int_value



def virtual_syndic():
    network_context = build_network_context()

    reset_terminal()
    header("SÍNDICO VIRTUAL — IA GOODWE")

    print("\nO Síndico Virtual analisa os dados da rede e responde")
    print("perguntas gerenciais em linguagem simples.\n")
    print("Exemplos:")
    print("  • Como está a saúde da rede?")
    print("  • Qual o faturamento atual?")
    print("  • Há falhas críticas?")
    print("  • O que otimizar na tarifação?\n")
    separator()

    while True:
        question = input("\nSua pergunta (ou 'sair'): ").strip()

        if not question or question.lower() == 'sair':
            break

        load("\nSíndico Virtual analisando")

        try:
            response = call_syndic_api(question, network_context)
        except:
            response = syndic_fallback(question, network_context)

        header("SÍNDICO VIRTUAL:")
        header(response)

        again = validate_int_value("\n1 - Nova pergunta\n0 - Voltar\n\nOpção: ")
        if again != 1:
            break