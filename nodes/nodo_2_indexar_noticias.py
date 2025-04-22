
from langchain_core.messages import HumanMessage, SystemMessage
from utils.index_news import index_news
from utils.get_news import get_news
def nodo_2_indexar_noticias(state: dict) -> dict:

    """
    Node 2: Indexing news articles.
    """

    tickers = list(state["portfolio"].keys())[:-1]  # Get the tickers from the portfolio
    # Check if the news data is already indexed
    # then index the news data
    news_data = get_news(tickers, from_days=20)
    print("news_data", news_data)
    index_news(news=news_data)

    return {
        **state,
        'portfolio_history': [],
        "messages": [SystemMessage(content="Noticias indexadas exitosamente. Puedes revisar el portafolio o buscar información adicional.")],

        "next_action": "",  # next_action indica siguiente paso
    }
