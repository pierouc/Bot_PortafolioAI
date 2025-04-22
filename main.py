
from graphs.main_graph import init_graph
import dotenv
import os
# from agents.agenPortfolio_react import agentPortfolio
# from agents.agentChat_react import agentChat
from agents.new_agent_chat import new_agent_chat
from agents.new_agent_portfolio import new_agent_portfolio
from core.agent_registry import AGENTS


def initialize_agents():
    """	
    Initialize the agents with the given portfolio.
    This function sets up the agents and adds them to the AGENTS dictionary.
    """
    # Add the initialized agents to the AGENTS dictionary
    # AGENTS["agent_chat"] = agentChat(portfolio=portfolio)
    # AGENTS["agent_portfolio"] = agentPortfolio()
    AGENTS["new_agent_chat"] = new_agent_chat()
    AGENTS["new_agent_portfolio"] = new_agent_portfolio()


def main():
    dotenv.load_dotenv('.env')
    api_key_openai = os.getenv("API_KEY_OPENAI")
    api_key_langsmith = os.getenv("API_KEY_LANGSMITH")
    os.environ["OPENAI_API_KEY"] = api_key_openai
    os.environ["LANGSMITH_TRACING"]='true'
    os.environ["LANGSMITH_ENDPOINT"]='https://api.smith.langchain.com'
    os.environ["LANGSMITH_API_KEY"]=api_key_langsmith
    os.environ["LANGSMITH_PROJECT"]='clay'



    portfolio = {
    "Equity Tech Fund": "20%",
    "Green Energy ETF": "15%",
    "Health Bio Stocks": "10%",
    "Global Bonds Fund": "10%",
    "CryptoIndex": "10%",
    "Real Estate REIT": "10%",
    "Emerging Markets Fund": "10%",
    "AI & Robotics ETF": "5%",
    "Commodities Basket": "5%",
    "Cash Reserve": "5%"
}
    
    initial_money =  10000  # initial investment in USD

    portfolio_usd = portfolio.copy()
    # Split the money in the portfolio to see how much money is in each stock
    for key in portfolio.keys():
        portfolio_usd[key] = round((initial_money * float(portfolio[key].replace("%", ""))) / 100, 2)

    initial_state = {
        "portfolio": portfolio,
        'portfolio_history': [(portfolio_usd,'Initial Portfolio')],
        "messages": [],
        "next_action": None, 
    }
    initialize_agents()
    graph = init_graph()
    final_state = graph.invoke(initial_state)



    # Print the potfolio history
    for i, (portfolio, reason) in enumerate(final_state['portfolio_history']):
        print(f"Portfolio {i}: {portfolio}")
        print(f"Reason: {reason}")
        print()
 
    
if __name__ == "__main__":
    main()