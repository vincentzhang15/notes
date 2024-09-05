"""
2024-09-04
LangChain RAG sample usage with Ollama.

Notes:
RAG: two parts
1. Indexing: load data, split, embed, store.
2. Retrieve, generate.

References:
LangChain RAG:
https://python.langchain.com/v0.2/docs/tutorials/rag/

Ollama Embeddings:
https://python.langchain.com/v0.2/docs/integrations/text_embedding/ollama/

Embedding issue:
https://stackoverflow.com/questions/78162485/problems-with-python-and-ollama
The following import...
from langchain_ollama import OllamaEmbeddings
... produces this error ...
ollama._types.ResponseError: 404 page not found
... on this line ...
vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model=MODEL))
... which is fixed by using this import instead ...
from langchain_community.embeddings.ollama import OllamaEmbeddings
"""

import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.llms import OllamaLLM

MODEL = "qwen2:72b-instruct"
MODEL = "mistral:7b-instruct"

llm = OllamaLLM(model=MODEL)

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model=MODEL))


# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke("What is Task Decomposition?"))
