"""
FAISS usage in LangChain.

Reference:
https://python.langchain.com/docs/integrations/vectorstores/faiss/

Created: 2024-09-30
Updated: 2024-09-30
"""

from langchain_core.embeddings import FakeEmbeddings
embeddings = FakeEmbeddings(size=4096)

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)
