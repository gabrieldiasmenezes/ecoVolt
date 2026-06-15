from utils.ui import header,separator


def about_account_type():
    header("INFORMAÇÕES SOBRE OS TIPOS DE PERFIS")
    print("""
CLIENTE COMERCIAL
• Localizar estações
• Iniciar recargas
• Acompanhar sessões
• Consultar custos

CLIENTE RESIDENCIAL
• Gerenciar carregador residencial
• Consultar histórico
• Simular economia de energia

DONO DE ESTABELECIMENTO
• Monitorar carregadores
• Visualizar faturamento
• Gerenciar demanda energética
• Acompanhar sessões ativas

ADMINISTRADOR GOODWE
• Perfil interno da plataforma
• Não disponível para cadastro
    """)
    separator()