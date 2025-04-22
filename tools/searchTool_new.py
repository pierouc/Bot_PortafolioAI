
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

import dotenv

@tool
def search_tool_new(query: str) -> str:
    """Use this to get context information about finantial news."""
    #LOAD ENVIRONMENT VARIABLES
    dotenv.load_dotenv('../.env')
    api_key = os.getenv("API_KEY_OPENAI")
    os.environ["OPENAI_API_KEY"] = api_key
    # Load the vectorstore as a search tool to search for news articles distantly related to the query.
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")  # o "text-embedding-ada-002"
    # Load the FAISS index from the local directory (basically db embeddings)
    db = FAISS.load_local("./data/faiss_news_index/", embeddings=embeddings, allow_dangerous_deserialization=True)
    # Create a retriever from the vectorstore
    retriever = db.as_retriever()
    # Use the retriever to search for relevant documents based on the query
    docs = retriever.invoke(query,k=7)
    #return with metadata and content of the documents
    return "\n\n".join([
        f"Título: {doc.metadata.get('title', 'N/A')}\n"
        f"Fuente: {doc.metadata.get('source', 'N/A')}\n"
        f"URL: {doc.metadata.get('url', 'N/A')}\n"
        f"Contenido: {doc.page_content}"
        for doc in docs
    ])
