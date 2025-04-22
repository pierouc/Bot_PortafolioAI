# Bot_PortafolioAI
Auxiliar bot, created to analyze finantial news.

Steps to run the project:

1. Create a new virtual enviroment with python 

``` python -m venv /path/to/new/virtual/environment ```

2. Install libraries

```pip install -r requierements.txt```

3. Create a file called .env with your api keys from:
   - NewsAPI: Free but with quota. [Register Here Free](https://newsapi.org/register)
   - LangSmith: Free. used for debug the graph. [Register Here Free](https://smith.langchain.com/)
   - OpenAI: Paid, i'm using model gpt-3.5-turbo-1106 the cheapest one right now. With $5 i tested the whole project for 4 days and remains like $0.5 yet [OpenAI Register](https://platform.openai.com/)
  
   Example file
   ```.env
    API_KEY_OPENAI=sk-xxxxxxxx
    API_KEY_NEWSAPI=xxxxxxxxxxx
    API_KEY_LANGSMITH=lsv2_xxxxxxxxx
   ```
4. Run
    ```cmd
      python main.py
    ```
  and follow the instruccions! Enjoy!!!!


------------------------------------------------------------------------
   
Folder Map

```
.
└── Bot_PortafolioAI/
    ├── agents/
    │   ├── new_agent_chat.py
    │   ├── new_agent_portfolio.py 
    │   ├── agentChat_react.py (deprecated)
    │   └── agentPortfolio_react.py (deprecated)
    ├── core/
    │   └── agent_registry.py
    ├── data/
    │   └── data_faiss_index (auto generated)/
    │       ├── foo.faiss
    │       └── foo.pkl
    ├── graphs/
    │   └── main_graph.py
    ├── nodes  /
    │   ├── initialize_agents.py (deprecated)
    │   ├── nodo_1_generar_portafolio_inicial.py
    │   ├── nodo_2_indexar_noticias.py
    │   ├── nodo_3_pedir_accion_usuario.py
    │   ├── nodo_4_responder_dudas.py
    │   └── nodo_5_rebalanceo_recomendado.py
    ├── tools/
    │   ├── searchTool.py (deprecated)
    │   └── searchTool_new.py
    └── utils/
        ├── get_news.py
        └── index_news.py
```
------------------------------------------------------------------------

project function graph made with langgraph

![image](https://github.com/user-attachments/assets/fba32118-19a7-44a2-b77f-7cdbb75740f6)

