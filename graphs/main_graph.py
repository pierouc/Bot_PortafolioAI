from nodes.nodo_1_generar_portafolio_inicial import nodo_1_generar_portafolio_inicial
from nodes.nodo_2_indexar_noticias import nodo_2_indexar_noticias
from nodes.nodo_3_pedir_accion_usuario import nodo_3_pedir_accion_usuario
from nodes.nodo_4_responder_dudas import nodo_4_responder_dudas
from nodes.nodo_5_rebalanceo_recomendado import nodo_5_rebalanceo_recomendado
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage
from typing import Annotated
import operator
from typing_extensions import TypedDict



# definicion de los nodos del grafo
def init_graph():
    """
    this function initializes a state graph for a financial assistant agent using the Langchain library.
    It defines the nodes and edges of the graph, representing different states and actions the agent can take during its interaction with the user.
    The graph is designed to help the agent generate an initial portfolio, index news, ask for user actions, respond to questions, and suggest rebalancing based on user input.
    """
    
    class State(TypedDict):
        portfolio: dict
        messages: Annotated[list[BaseMessage], operator.add]
        portfolio_history: Annotated[list[BaseMessage], operator.add]
        next_action: str

    # Initialize the state graph
    # The state graph is a directed graph where each node represents a state in the conversation.
    workflow = StateGraph(State)

    # Define the nodes of the graph
    # Each node is a function that represents a specific action or state in the conversation.
    # The nodes are defined in separate modules and imported here.
    # The nodes are responsible for generating the initial portfolio, indexing news, asking for user actions, responding to questions, and suggesting rebalancing.
    # The nodes are connected by edges, which represent the flow of the conversation.
    # The edges are defined using the add_edge and add_conditional_edges methods of the StateGraph class.
    # The edges are used to connect the nodes and define the flow of the conversation.
    workflow.add_node("nodo_1_generar_portafolio_inicial", nodo_1_generar_portafolio_inicial)
    workflow.add_node("nodo_2_indexar_noticias", nodo_2_indexar_noticias)
    workflow.add_node("nodo_3_pedir_accion_usuario", nodo_3_pedir_accion_usuario)
    workflow.add_node("nodo_4_responder_dudas", nodo_4_responder_dudas)
    workflow.add_node("nodo_5_rebalanceo_recomendado", nodo_5_rebalanceo_recomendado)

    # Define the edges of the graph
    # The edges are used to connect the nodes and define the flow of the conversation.
    workflow.add_edge(START, "nodo_1_generar_portafolio_inicial")
    workflow.add_edge("nodo_1_generar_portafolio_inicial", "nodo_2_indexar_noticias")
    workflow.add_edge("nodo_2_indexar_noticias", "nodo_3_pedir_accion_usuario")
    # conditional edges are used to define the flow of the conversation based on user input or other conditions.
    # The conditional edges are defined using the add_conditional_edges method of the StateGraph class.
    # The conditional edges are used to connect the nodes and define the flow of the conversation based on user input or other conditions.
    workflow.add_conditional_edges(
        "nodo_3_pedir_accion_usuario",
        lambda state: state["next_action"],  # next_action indica siguiente paso
        {
            "actualizar noticias": "nodo_2_indexar_noticias",
            "hacer preguntas": "nodo_4_responder_dudas",
            "sugerir rebalanceo": "nodo_5_rebalanceo_recomendado",
            "salir": END
        },
    )
    workflow.add_conditional_edges(
        "nodo_4_responder_dudas",
        lambda state: state["next_action"],
        {
            "hacer preguntas": "nodo_4_responder_dudas",
            "opciones": "nodo_3_pedir_accion_usuario",
        },

    )
    workflow.add_edge("nodo_5_rebalanceo_recomendado", "nodo_3_pedir_accion_usuario")

    # Define memory management for the graph
    # memory = MemorySaver()
    # The memory management is used to save and load the state of the conversation if is needed
    # for example, if the user wants to save the conversation and continue later.
    # or if you reach a sensitive point in the conversation and you want to save the state of the conversation.
    graph = workflow.compile()
    return graph
