from typing import List
from langchain_openai import OpenAIEmbeddings
import dotenv
import hashlib, os
from uuid import uuid4
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


# This function indexes news articles using FAISS and OpenAI embeddings.
def index_news(news: List[dict], 
               path_indice: str = "./data/faiss_news_index", 
               check_dups: bool = True) -> None:
    """
    Indexes news articles using FAISS and OpenAI embeddings.
    """

    # Load environment variables from .env file
    dotenv.load_dotenv('../.env')
    api_key = os.getenv("API_KEY_OPENAI")
    
    print("Indexing news...")
    #embedding_model instance
    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small",  
        openai_api_key=api_key,  
    )

    # The RecursiveCharacterTextSplitter is used to split the text into smaller chunks for better indexing.
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)

    def hash_text(text: str) -> str:
        """
        Hashes the text to create a unique identifier for it.
        """
        # Use MD5 hash for simplicity.
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    if not news:
        # If no news articles are provided, load the existing index and return it.
        print("non relevant news")
        vectorstore = FAISS.load_local(path_indice, embedding_model, allow_dangerous_deserialization=True)
        return vectorstore


    # Extract content and metadata from the news articles.
    contents, metadatas = [], []
    for noticia in news:
        content = noticia.get("content", "") or ""
        if content.strip() == "":
            continue
        contents.append(content)
        # Extract metadata from the news article for indexing.
        metadatas.append({
            "title": noticia.get("title", ""),
            "source": noticia.get("source", ""),
            "url": noticia.get("url", ""),
        })

    print("splitting news in chunks...")
    new_docs = splitter.create_documents(contents, metadatas=metadatas)

    if not new_docs:
        print("there's not news to index")
        return

    content_existente = set()

    # Check if the index already exists.
    if os.path.exists(path_indice):
        print("loading existing FAISS index...")
        #FAISS is the vector store used for indexing the vector representation or embedding.
        vectorstore = FAISS.load_local(path_indice, embedding_model, allow_dangerous_deserialization=True)
        if check_dups:
            documentos_existentes = vectorstore.docstore._dict.values()
            content_existente = set(hash_text(doc.page_content) for doc in documentos_existentes)
    else:
        # otherwise, create a new index.
        print("Creating new FAISS index...")
        vectorstore = FAISS.from_documents(new_docs, embedding_model)

    print("Filtering duplicates...")
    if check_dups:
        docs_to_add = [doc for doc in new_docs if hash_text(doc.page_content) not in content_existente]
    else:
        docs_to_add = new_docs

    if not docs_to_add:
        print("News was already indexed. No new news to add.")
        return vectorstore

    # Generate unique IDs for the new documents.
    ids = [str(uuid4()) for _ in docs_to_add]

    print(f"adding {len(docs_to_add)} documents to the index...")
    vectorstore.add_documents(documents=docs_to_add, ids=ids)
    #save the updated index to the specified path to avoid re-processing the same data.
    vectorstore.save_local(path_indice)
    print(f"Index updated with {len(docs_to_add)} new news.")
    return vectorstore
