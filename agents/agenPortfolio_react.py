from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from tools.searchTool import search_tool
from datetime import date
from langchain_core.prompts import PromptTemplate


def agentPortfolio():
    """
    This function creates a React agent that proposes a new investment portfolio distribution based on recent financial news and trends.
    It uses the Langchain library and OpenAI's GPT-3.5-turbo model to analyze the current portfolio and suggest adjustments.
    The agent has access to a search tool for gathering information and a time tool for date-related queries.
    The agent's prompt template is designed to guide the model in generating a new portfolio distribution while ensuring that the total allocation sums to 100%.
    The agent also provides a brief explanation of its reasoning after the proposed distribution.
    """
    # Initialize the search tool 
    tool_search = search_tool()

    # Initialize the LLM (Language Model)
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)


    # Define the prompt template for the agent
    today = date.today()

    # Define the prompt template for the agent
    # in english the bot will be more precise and less verbose

    prompt_portfolio = PromptTemplate.from_template(
        template=f"""
    You are a financial assistant. Your task is to propose a new investment portfolio distribution based on recent financial news and trends.

    Your task is:
    - Propose a new portfolio distribution based on the current market trends.
    - Return a Python dictionary where the asset allocations must sum **exactly to 100%**.
    - For example, if you increse 10% in some asset, you must decrease other assets by 10% to keep the total at 100%.
    - The portfolio should include a "Cash Reserve".
    - Provide a brief explanation after the separator `$$` explaining your reasoning.

    You have access to the following tool:
    {{tools}}

    current date: {today}
    ---

    **Use the following reasoning and output format exactly:**
    Question: {{input}}
    Thought: (What do you need to find or consider about the current portfolio or market?)
    Action: (Pick one tool from [{{tool_names}}])
    Observation: (The result of the tool)
    ... (Repeat Thought / Action / Action Input / Observation as needed)
    Thought: (Summarize what you've learned and how it affects the portfolio and rebalance investment strategy.)
    Final Answer: 
    {{{{
        "Asset 1": ...,
        "Asset 2": ...,
        ...
    }}}} $$ (Explain any increase/decrease, what the news said, and why the new balance is smart. Please include real news urls.)

    ---

    **Rules**
    - DON'T FORGET THE $$ SEPARATOR.
    - you cant have more than a 100% of money in the portfolio.

    Begin.

    Question: {{input}}
    {{agent_scratchpad}}
   

    
    """) 

    # Define the prompt template for the agent
    react_agent = create_react_agent(
        llm=llm,
        tools=[tool_search],
        prompt=prompt_portfolio,
    )

    # Create the agent executor
    agent_executor__ = AgentExecutor(
        agent=react_agent,
        tools=[tool_search],
        handle_parsing_errors=True,
        max_iterations=15,
        # verbose=True
    )
    return agent_executor__