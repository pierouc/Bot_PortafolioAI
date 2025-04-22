def nodo_3_pedir_accion_usuario(state: dict) -> dict:
    """
    Node 3: Ask the user for the next action.
    This node prompts the user to choose an action from a list of options.
    Depending on the user's choice, it will return the corresponding action.
    If the user chooses to exit, it will return an exit action.
    """

    mensaje = (
        "What would you like to do next?\n"
        "1. Update news\n"
        "2. Ask questions\n"
        "3. Rebalance portfolio\n"
        "4. Exit\n"
        "Please enter the number or the action name (e.g., 'update news', 'ask questions', 'rebalance portfolio', 'exit').\n"
        )
        

    
    while 1:
        user_action = str(input(mensaje))

        if user_action == "1" or user_action.lower() == "actualizar noticias" or user_action == "update news":
            action = "actualizar noticias"
            break
        elif user_action == "2" or user_action.lower() == "conversar" or user_action == "ask questions":
            action = "hacer preguntas"
            break
        elif user_action == "3" or user_action.lower() == " rebalancear portafolio" or user_action == "rebalance portfolio":
            action = "sugerir rebalanceo"
            break
        elif user_action.lower() == "salir" or user_action.lower() == "exit" or user_action == "4":
            action = "salir"
            break
        else:
            action = None
            print("Invalid action. Please try again.")
            
        # print("action", action)
    return {
        **state,
        'portfolio_history': [],
        "messages":[],
        "next_action": action,  # next_action indica siguiente paso
    }