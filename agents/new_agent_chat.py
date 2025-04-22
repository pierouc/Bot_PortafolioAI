# First we initialize the model we want to use.
from langchain_openai import ChatOpenAI
import dotenv
import os
# from tools.searchTool_new import search_tool_new
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from tools.searchTool_new import search_tool_new
from langchain_core.tools import tool
store = {}

def new_agent_chat():
        
    dotenv.load_dotenv('.env')
    api_key = os.getenv("API_KEY_OPENAI")
    os.environ["OPENAI_API_KEY"] = api_key
    model = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
    tools = [search_tool_new]

    memory = InMemorySaver()

    # Define the graphh
    agent = create_react_agent(model,tools=tools,checkpointer=memory)
        
    return agent

