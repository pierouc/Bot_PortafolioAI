from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from tools.searchTool import search_tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from datetime import date
from langchain_core.prompts import PromptTemplate


# store variable to keep track of the chat history for each session
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Retrieve the chat history for a given session ID. If it doesn't exist, create a new one.
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def agentChat(portfolio: dict):
    """
    This function creates a React agent that helps users understand their investment portfolio and stay updated with relevant financial news.
    It uses the Langchain library and OpenAI's GPT-3.5-turbo model to analyze the portfolio and provide insights.
    The agent has access to a search tool for gathering information and a time tool for date-related queries.
    The agent's prompt template is designed to guide the model in generating responses while ensuring that the conversation remains coherent and relevant.
    The agent also provides a brief explanation of its reasoning after the proposed distribution.
    """
    # Initialize the search tool
    searchTool = search_tool()
    
    # Initialize the LLM (Language Model)
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)

    # Define the prompt template for the agent, brackets are used to avoid parsing errors
    portfolio = '{'+str(portfolio)+'}'

    # todays date is used to avoid llm outdated information
    today = date.today()

    # Define the prompt template for the agent
    # in english the bot will be more precise and less verbose
    prompt = PromptTemplate.from_template(f"""
        You are a helpful and knowledgeable financial assistant.

        Your job is to stay updated with relevant financial news and answer every user questions. you can find news in tools [{{tool_names}}]. 

        Tools available: {{tools}}

        Current date: {today}
        First portfolio: {portfolio}
        ---

        you must this format for your answers:
        **Use the following reasoning and output format exactly:**
        Question: {{input}}  
        Thought: (What are you thinking?)  
        Action: (One tool from [{{tool_names}}])  
        Action Input: (Input for the tool)
        Observation: (Tool result)  
        ... (Repeat Thought / Action / Input / Observation if needed)  
        Thought: (Summarize your findings)  
        Final Answer: (Answer the user's question)
        ---


        Example:
        1.Question: What's the latest news about AAPL?
        2.Thought: I should use the news tool to get the latest information.
        3.Action: news_tool
        4.Action Input: AAPL
        5.Observation: Apple shares rise after earnings report.
        6.Thought: I now have the latest news.
        7.Final Answer: Apple shares rose due to strong earnings.

        restrictions:
        - AVOID Invalid Format: Missing 'Action:' after 'Thought:'
        - if user ask for portfolio distribution, you must give him {portfolio} unless you have a new one.
        - If user say Hello, Hi or Hi there, you say something friendly.
        - If user talks non-sense, just be polite.
        - if you don't know the answer, reply politely.
        - Don't get stuck in past conversations, always focus on the current question.


        begin always following Question/Thought/Action/Observation/Thought/Final Answer format.

        Question: {{input}}  
        Chat History: {{chat_history}}  
        {{agent_scratchpad}}
        """)

    
    # Initialize the checkpointer to save the chat history
    checkpointer=InMemorySaver()
    # Initialize the agent with the LLM, tools, and prompt
    react_agent = create_react_agent(
        llm=llm,
        tools=[searchTool],
        prompt=prompt,
    )

    # Set the agent's memory to store the chat history
    agent_executor_ = AgentExecutor(
        agent=react_agent,
        tools=[searchTool],
        handle_parsing_errors=True,
        max_iterations=10,
        verbose=True,
    )

    # Create a RunnableWithMessageHistory to manage the chat history automatically
    # checkpointer allows to save the chat history in memory without persisting it to disk
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor_,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        checkpointer=checkpointer,
    )

    return agent_with_chat_history