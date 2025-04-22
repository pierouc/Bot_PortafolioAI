# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI
import dotenv
import os
# from tools.searchTool_new import search_tool_new
from langgraph.prebuilt import create_react_agent
from tools.searchTool_new import search_tool_new
#RunnableWithMessageHistory is used to keep track of the chat history
from langchain_core.prompts import PromptTemplate


store = {}

def new_agent_portfolio():
    
    dotenv.load_dotenv('.env')
    api_key = os.getenv("API_KEY_OPENAI")
    os.environ["OPENAI_API_KEY"] = api_key
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    tools = [search_tool_new]


    prompt_portfolio_simple = (
        """
    You are a financial assistant. Your job is to analyze recent financial news and propose a new investment portfolio distribution.

    Instructions:
    - Begin your response **immediately** with a Python dictionary. Do not include any introductory text.
    - The dictionary cannot be equivalent to the previous portfolio. It must be a new distribution.
    - All values must be strings representing percentages with a `%` sign (e.g., "25%").
    - The **total of all allocations, including "Cash Reserve", must sum to exactly 100%**.
    - Ensure numerical precision. The sum must be **mathematically correct** — not approximated or rounded in a way that causes drift.
    - After the dictionary, include a brief explanation of your reasoning, separated by `$$`.

    Output format:
    {{
        "Asset 1": "XX%",
        "Asset 2": "YY%",
        "Cash Reserve": "ZZ%",
        ...
    }}$$
    (Brief explanation: summarize your reasoning based on current market conditions.)
    """
    )


    #Define the graphh
    agent = create_react_agent(model,tools=tools,prompt=prompt_portfolio_simple)
    
    
    return agent

