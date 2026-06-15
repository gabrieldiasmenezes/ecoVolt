from database.settings import CHARGER_STATUS
from database.database import users, vehicles
from utils.system import reset_terminal
from utils.helpers import get_user_name, get_vehicle_model


# ==========================
# ELEMENTOS BÁSICOS DE UI
# ==========================

def enter():
    input("Pressione Enter para voltar...")


def header(content):
    print("\n" + "=" * 40)
    print(f"{content:^40}")
    print("=" * 40)


def separator():
    print("\n" + "=" * 40)


def footer():
    separator()
    enter()


def error_option():
    print("[ERRO] Opção inválida! Digite novamente.")
    enter()
    reset_terminal()


# ==========================
# COMPONENTES REUTILIZÁVEIS
# ==========================

def progress_bar(current, maximum, width=20):
    """
    Retorna uma barra de progresso e sua porcentagem.
    """

    if maximum <= 0:
        return "░" * width, 0

    ratio = current / maximum

    filled = int(ratio * width)
    percentage = int(ratio * 100)

    bar = (
        "█" * filled +
        "░" * (width - filled)
    )

    return bar, percentage


# ==========================
# CARDS
# ==========================

def session_card(session, mode="list"):

    tipo = (
        "Premium"
        if session.get("tipo") == "premium"
        else "Comum"
    )

    status = (
        "ATIVA"
        if session.get("status") == "ativa"
        else "FINALIZADA"
    )

    print(f"\nID: {session.get('id')}")
    print(f"Cliente:    {get_user_name(session['usuario_id'])}")
    print(f"Veículo:    {get_vehicle_model(session['veiculo_id'])}")
    print(f"Carregador: {session.get('carregador_id')}")
    print(f"Tipo:       {tipo}")

    if mode in ("list", "detail"):
        print(f"Potência:   {session.get('potencia_kw')} kW")

    if mode == "detail":
        print(f"\nEnergia:    {session.get('energia_kwh')} kWh")
        print(f"Tarifa:     R$ {session.get('tarifa_kwh', 0):.2f}/kWh")
        print(f"Valor:      R$ {session.get('valor', 0):.2f}")
        print(f"Início:     {session.get('inicio')}")
        print(f"Fim:        {session.get('fim') or '—'}")
        print(f"Status:     {status}")


def charger_card(charger):

    is_premium = charger.get("reservado_premium", False)

    tipo = (
        "🔶 Premium"
        if is_premium
        else "🔷 Comum"
    )

    status = CHARGER_STATUS.get(
        charger["status"],
        charger["status"].upper()
    )

    bar, pct = progress_bar(
        charger["potencia_atual"],
        charger["potencia_maxima"]
    )

    print(f"\nCarregador #{charger['numero']}  {tipo}")

    separator()

    print(f"""
Modelo:             {charger['modelo']}
Status:             {status}
Potência máxima:    {charger['potencia_maxima']} kW
Carga:              [{bar}] {pct}%
Sessões realizadas: {charger['total_sessoes']}
Energia fornecida:  {charger['energia_fornecida_kwh']} kWh
""")

    separator()