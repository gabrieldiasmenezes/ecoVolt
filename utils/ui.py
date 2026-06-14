from utils.system import reset_terminal


def enter():
    input("Pressione Enter para voltar...")

def header(content):
    print("\n" + "="*40)
    print(f"{content:^40}")
    print("="*40)



def error_option():
    print("[ERRO] Opção inválida!Digite novamente")
    enter()
    reset_terminal()

