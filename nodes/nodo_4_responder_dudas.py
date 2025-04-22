
from core.agent_registry import AGENTS
from langgraph.checkpoint.memory import InMemorySaver


# Nodo de conversación
def nodo_4_responder_dudas(state: dict) -> dict:
    """
    Node 4: Respond to user questions.
    This node allows the user to ask questions and receive answers from the agent.
    It uses the agent_chat to handle the conversation.
    """

    # Check if the agent is initialized
    agent_chat = AGENTS["new_agent_chat"]  
    while 1:
        msg = str(input("Type 'options' or 'o' to go back | Type portfolio to see your portfolio and news about your portfolio | Or type your question: "))

        if msg.lower() in ["options","opciones","o"]:
            break

        elif msg.lower() == "portfolio":
            print("Your portfolio is: ", state["portfolio"])
            res = agent_chat.invoke(
                {'messages': f'news related to my portfolio: {state["portfolio"]}'}, 
                {'configurable': {'thread_id': '111'}}
            )    
            print("News about your portfolio: ", res['messages'][-1].content)
            continue

        else:
            res = agent_chat.invoke(
                # {'messages': [msg],}, 
                {'configurable': {'thread_id': '111'}}
            )    
            print()
            print(res['messages'][-1].content)
            print()

    return {
        **state,
        'portfolio_history': [],
        "next_action": "opciones"
    }
