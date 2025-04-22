from agents.agentChat_react import agentChat
from agents.agenPortfolio_react import agentPortfolio


def initialize_agents(state: dict) -> dict:
    """
    Inicializa los agentes.
    """

    if not state.get("agents_initialized", False):  # Verificar si los agentes ya fueron creados
        chat = agentChat()  # Crear el agente executor
        executor = agentPortfolio()  # Crear el agente portfolio
        state["agents_initialized"] = True  # Marcar como inicializado
        return {
            **state,
            'agent_portfolio': executor,
            'agent_chat': chat,
            "next_node": "nodo_3_pedir_accion_usuario",
            "mensaje": "Agentes inicializados exitosamente.",
        }
    else:
        print("Los agentes ya han sido inicializados xd.")
        return {
            **state,
            "next_node": "nodo_3_pedir_accion_usuario",
            "mensaje": "Los agentes ya han sido inicializados.",
        }