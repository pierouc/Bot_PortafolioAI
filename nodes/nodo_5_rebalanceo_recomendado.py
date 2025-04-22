import ast
from core.agent_registry import AGENTS
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def nodo_5_rebalanceo_recomendado(state: dict) -> dict:
    """
    Node 5: Rebalance recommended portfolio.
    This node suggests rebalancing the portfolio based on news and user input.
    It uses the agent_portfolio to analyze the news and provide recommendations.
    The user is then prompted to confirm whether they want to rebalance the portfolio or not.
    """

    # old and new agent portfolio

    # agent_portfolio = state["agent_portfolio"]  # Obtener el agente executor
    agent_portfolio = AGENTS["new_agent_portfolio"]  # Obtener el agente executor
    result = agent_portfolio.invoke({'messages' : "analyze the news to rebalance my investment portfolio" + str(state["portfolio"])})


    print("Recomended Portfolio:")
    print(result["messages"][-1].content)
    extract_portfolio = (result["messages"][-1].content).split('$$')[0].strip().replace("%", "")
    new_portfolio = ast.literal_eval(extract_portfolio[extract_portfolio.index('{'):])
    reason = result["messages"][-1].content.split('$$')[1].strip()

    to_output = []
    to_output.append(HumanMessage(content="Rebalance my portfolio based on news:"))
    to_output.append(AIMessage(content='Your New Portfolio: ' + str(agent_portfolio)))


    #convert values from string to float to check if the sum is 100%
    for key in new_portfolio.keys():
        new_portfolio[key] = float(new_portfolio[key])
    
    #quality check to see if the sum of the portfolio is 100%
    if sum(new_portfolio.values()) != 100:
        print("La suma de los porcentajes no es igual a 100%. Intenta de nuevo.")
        return {
            **state,
            "messages": [],
            "portfolio_history": [],
            "next_action": "rechazar",
        }
    
    inital_usd = 10000  # initial investment in USD

    #split the money in the portfolio to see how much money is in each stock
    for key in new_portfolio.keys():
        new_portfolio[key] = round((inital_usd * new_portfolio[key]) / 100, 2)


    print('Nuevo portafolio:\n', new_portfolio)
    print('--'*50)
    print('Razón:\n', reason)
    # print()

    #user input to confirm rebalance
    input_message = input("Do you want to rebalance your portfolio? (yes/no): ")
    # if user input is yes, rebalance the portfolio and return the new state
    if input_message.lower() == "yes" or input_message.lower() == "y" or input_message.lower() == "si":
        print("Rebalancing portfolio...")
        return {
            **state,
            "messages": [to_output],
            "portfolio": new_portfolio,
            "portfolio_history": [([new_portfolio],reason)],
            "next_action": "aplicar",
        }

    #if user input is no, do not rebalance and return to the previous state
    elif input_message.lower() == "no" or input_message.lower() == "n":
        print("No change will be made to the portfolio.")
        return {
            **state,
            "messages": [],
            'portfolio_history': [],
            "next_action": "rechazar",
        }

    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return {
            **state,
            'portfolio_history': [],
            "messages": [],
            "next_action": "rechazar",
    }