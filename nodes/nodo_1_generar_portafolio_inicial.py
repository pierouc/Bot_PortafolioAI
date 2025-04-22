from langchain_core.messages import SystemMessage

def nodo_1_generar_portafolio_inicial(state: dict = None) -> dict:
    """
    Node 1: Welcome message and initial portfolio generation.
    """
    welcome_message = (
        "Welcome to the investment portfolio assistant! "
        "I will help you create a personalized investment portfolio. "
    )

    print(welcome_message)
    print("\n")

    return{
        **state,
        'portfolio_history': [],
        "messages": [SystemMessage(content=welcome_message)]
        
    }
